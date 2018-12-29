# -*- coding: utf-8 -*-

from morpho.core import (
    AudioFormat,
    Ffmpeg,
    VideoFormat,
    enum_value_exists,
    swap_extension,
)


def test_base_file_format_properties():
    fmt = AudioFormat.alac
    assert fmt.codec == "alac"
    assert fmt.extension == "m4a"

    fmt = VideoFormat.mp4
    assert fmt.codec == fmt.extension == "mp4"


def test_base_file_format_get():
    path = "/path/to/some/media/audio.flac"
    fmt = AudioFormat.get(path)
    assert fmt == AudioFormat.flac

    path = "/path/to/some/media/video.mkv"
    fmt = VideoFormat.get(path)
    assert fmt == VideoFormat.mkv


def test_audio_file_format_properties():
    fmt = AudioFormat.flac
    assert fmt.params == ["-c:a", fmt.codec]


def test_video_file_format_properties():
    # This will *always* convert videos to MP4. This may or may not change
    # in the future.
    audio_params = ["-c:a", "aac", "-b:a", "192k"]
    video_params = [
        "-f",
        "mp4",
        "-c:v",
        "libx264",
        "-profile:v",
        "main",
        "-preset",
        "fast",
    ]
    fmt = VideoFormat.mp4
    assert fmt.params == audio_params + video_params


def test_ffmpeg_build_command():
    path = "/path/to/some/media/audio.m4a"
    fmt = AudioFormat.flac

    command = Ffmpeg.build_command(path, fmt)

    assert command == [
        "ffmpeg",
        "-i",
        path,
        "-c:a",
        "flac",
        swap_extension(path, fmt),
    ]


def test_ffmpeg_run():
    command = ["/bin/true"]
    assert Ffmpeg.run(command) is True

    command = ["/bin/false"]
    assert Ffmpeg.run(command) is False


def test_ffmpeg_run_handles_exception():
    command = [""]
    assert Ffmpeg.run(command) is False


def test_enum_value_exists():
    assert enum_value_exists("/path/to/some/media.flac", AudioFormat)
    assert enum_value_exists("test.mp4", VideoFormat)

    assert not enum_value_exists("/path/to/some/media.mp3", AudioFormat)
    assert not enum_value_exists("test.mov", VideoFormat)
    assert not enum_value_exists("", AudioFormat)


def test_swap_extension_audio():
    path = "/path/to/some/media/audio.m4a"
    fmt = AudioFormat.flac

    new_path = swap_extension(path, fmt)

    assert new_path == "/path/to/some/media/audio.flac"


def test_swap_extension_video():
    path = "/path/to/some/media/video.avi"
    fmt = VideoFormat.mp4

    new_path = swap_extension(path, fmt)

    assert new_path == "/path/to/some/media/video.mp4"
