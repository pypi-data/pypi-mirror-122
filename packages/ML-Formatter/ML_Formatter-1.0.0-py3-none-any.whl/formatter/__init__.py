from collections import namedtuple

from .deepspeech import DeepSpeech

__version__ = "1.0.0"

VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=1, minor=0, micro=0, releaselevel="beta", serial=0)
