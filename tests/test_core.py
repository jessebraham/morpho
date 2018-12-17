# -*- coding: utf-8 -*-

from morpho.core import AudioFormat, VideoFormat


def test_base_file_format_properties():
    fmt = AudioFormat.alac
    assert fmt.codec == "alac"
    assert fmt.extension == "m4a"

    fmt = VideoFormat.mp4
    assert fmt.codec == fmt.extension == "mp4"


def test_base_file_format_update_extension_audio():
    path = "/path/to/some/media/audio.m4a"
    fmt = AudioFormat.flac

    new_path = fmt.update_extension(path)

    assert new_path == "/path/to/some/media/audio.flac"


def test_base_file_format_update_extension_video():
    path = "/path/to/some/media/video.avi"
    fmt = VideoFormat.mp4

    new_path = fmt.update_extension(path)

    assert new_path == "/path/to/some/media/video.mp4"


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
        "-pre",
        "fast",
    ]
    fmt = VideoFormat.mp4
    assert fmt.params == audio_params + video_params