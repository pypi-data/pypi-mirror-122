class BaseFormatterException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = self.__doc__

    def __str__(self):
        return self.message


class NoMedia(BaseFormatterException):
    """The given media directory contained no media files with the expected file type."""


class MissingTranscription(BaseFormatterException):
    """A given media file is missing a corresponding transcription"""


class NonEmptyDir(BaseFormatterException):
    """Expected the output directory to be empty"""
