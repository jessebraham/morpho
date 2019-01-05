# Morpho

[![Build Status](https://travis-ci.org/jessebraham/morpho.svg?branch=master)](https://travis-ci.org/jessebraham/morpho) [![Coverage Status](https://coveralls.io/repos/github/jessebraham/morpho/badge.svg?branch=master)](https://coveralls.io/github/jessebraham/morpho?branch=master)

Convert audio and video files using [Python](https://www.python.org/) and [ffmpeg](https://ffmpeg.org/). 

**Morpho** consists of:
- a command-line interface for converting single files or entire directories  
- a service which monitors the filesystem for events and converts or renames files when appropriate

- - -

**Morpho** is built using the following packages:  
[click](https://click.palletsprojects.com/en/7.x/) | [colorama](https://github.com/tartley/colorama) | [inflect](https://github.com/jazzband/inflect) | [watchdog](https://pythonhosted.org/watchdog/index.html)  

The following packages are used for development and testing:  
[black](https://github.com/ambv/black) | [mypy](http://mypy-lang.org/) | [pytest](https://github.com/pytest-dev/pytest) | [pytest-cov](https://github.com/pytest-dev/pytest-cov)

- - -

## Usage

### Command-Line Interface

The command-line interface allows for the conversion of both audio and video files.

Audio files can be converted between the Apple Lossless Audio Codec (`.m4a`) and the Free Lossless Audio Codec (`.flac`). Audio files will be converted to whichever of the two supported formats is not provided, ie.) flac->alac, alac->flac.

Video files can be converted from the Audio Video Interleave (`.avi`), Matroska Video Stream (`.mkv`) and MPEG-4 (`.mp4`) formats. All video files will be convert to MPEG-4 at this time.

#### Supported Formats

**Audio:** ALAC (`.m4a`), FLAC (`.flac`)  
**Video:** AVI (`.avi`), MKV (`.mkv`), MPEG4 (`.mp4`)

#### Example

```bash
$ python -m morpho.cli audio /some/audio/file.m4a
$ # converts the above file to /some/audio/file.flac
$ pyhton -m morpho.cli video /some/video/file.mkv
$ # converts the above file to /some/video/file.mp4
```

### Filesystem Monitor

TODO: document me
