from collections import namedtuple

from .deepspeech import DeepSpeech

__version__ = "1.0.1"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(
    major=1, minor=0, micro=1, releaselevel="production", serial=0
)
