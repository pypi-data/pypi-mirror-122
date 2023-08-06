from pathlib import Path

import attr


@attr.s
class Item:
    """Represents a set of files"""

    media_name: str = attr.ib()  # Wav filename
    media_file: str = attr.ib()  # Path to media file
    transcript_file: str = attr.ib()  # Path to transcript file

    def get_absolute_media_path(self):
        """
        Returns
        -------
        str
            The absolute path to the media file
        """
        return Path(self.media_file).resolve()

    def get_absolute_transcript_path(self):
        """
        Returns
        -------
        str
            The absolute path to the transcript file
        """
        return Path(self.transcript_file).resolve()

    def get_media_file_size(self):
        """
        Returns
        -------
        bytes
            The size of the file in bytes
        """
        return Path(self.media_file).stat().st_size

    def get_transcription(self):
        """
        Returns
        -------
        str
            The transcription of this media file
        """
        text = Path(self.transcript_file).read_text(encoding="utf-8")
        return text.rstrip("\n")
