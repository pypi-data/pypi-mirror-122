import logging
import os
from pathlib import Path
import csv
from random import shuffle

from formatter.base_formatter import BaseFormatter
from formatter.deepspeech.item import Item
from formatter.exceptions import NoMedia, MissingTranscription, NonEmptyDir

log = logging.getLogger(__name__)


# TODO We should shuffle the file to produce more random results,
#   however reading massive files into memory to perform a shuffle is
#   not going to work for our use case
class DeepSpeech(BaseFormatter):
    """
    Designed to have a lot of file read/writes to save on
    needing to store everything in memory. This also means
    the process is essentially O(2) in terms of overall passes
    as we store everything initially before splitting up into
    train/test/dev.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.line_count = 0

    def run(self):
        """The runner for DeepSpeech formatting"""
        log.info("Beginning run")
        self.create_initial_files()
        with open(
            os.path.join(self.output_dir, "all.csv"),
            newline="",
            mode="a",
            encoding="utf-8",
        ) as f:
            writer = csv.writer(f)

            found_file = False
            with os.scandir(self.media_dir) as it:
                entry: os.DirEntry
                for entry in it:
                    if not entry.is_file():
                        continue

                    filename: str = entry.name
                    if not filename.endswith(self.media_type):
                        continue

                    # Strip filetype to use as a generic pointer
                    filename = filename[: (len(filename) - (len(self.media_type) + 1))]

                    found_file = True
                    # Okay its a valid media file, lets try find its transcription
                    transcript_path: str = os.path.join(
                        self.transcript_dir, f"{filename}.{self.transcript_type}"
                    )
                    transcript = Path(transcript_path)
                    if not transcript.is_file():
                        log.warning(
                            "%s.%s is missing a transcript",
                            filename,
                            f"{filename}.{self.transcript_type}",
                        )

                    item = Item(
                        media_file=entry.path,
                        transcript_file=transcript_path,
                        media_name=filename,
                    )

                    self.process_item(writer, item)
                    self.line_count += 1

        if not found_file:
            raise NoMedia()

        # Split em up
        self.split_into_runs()

    def create_initial_files(self) -> None:
        """Creates the initial files and sets up directories"""
        output_dir = Path(self.output_dir)
        if any(output_dir.iterdir()):
            raise NonEmptyDir

        # Make the media directory
        Path(os.path.join(self.output_dir, "media")).mkdir(parents=True)

        # Setup our csv files
        self._create_csv("train")
        self._create_csv("test")
        self._create_csv("dev")
        self._create_csv("all")

        log.info("Created initial files")

    def process_item(self, writer, item: Item) -> None:  # noqa
        """Process's an item and outputs it to a generic 'all' file"""
        path = self._hard_link(item)

        writer.writerow(
            [
                path,
                item.get_media_file_size(),
                item.get_transcription(),
            ]
        )
        log.debug("Processed %s", item.media_file)

    def split_into_runs(self) -> None:
        """Splits the 'initial_runs' file into runs using the provided split ratio"""
        log.info("Begin splitting files into runs")
        all_file = open(
            os.path.join(self.output_dir, "all.csv"),
            newline="",
            mode="r",
            encoding="utf-8",
        )
        dev_file = open(
            os.path.join(self.output_dir, "dev.csv"),
            newline="",
            mode="a",
            encoding="utf-8",
        )
        test_file = open(
            os.path.join(self.output_dir, "test.csv"),
            newline="",
            mode="a",
            encoding="utf-8",
        )
        train_file = open(
            os.path.join(self.output_dir, "train.csv"),
            newline="",
            mode="a",
            encoding="utf-8",
        )

        # Make readers n writers
        all_file_reader = csv.reader(all_file)
        next(all_file_reader)  # Skip headers
        dev_writer = csv.writer(dev_file)
        test_writer = csv.writer(test_file)
        train_writer = csv.writer(train_file)
        log.debug("Created readers")

        # Get dev / test / train splits
        total: int = self.line_count
        train: int = round(total * 0.7)
        test: int = round(total * 0.2)
        dev: int = round(total * 0.1)
        log.info("Total: %d Train: %d Test: %d Dev: %d", total, train, test, dev)

        # Args say we should shuffle this data before use
        if not self.dont_shuffle:
            all_file_reader = list(all_file_reader)
            shuffle(all_file_reader)

        for count, row in enumerate(all_file_reader):
            if count < dev:
                dev_writer.writerow(row)
                log.debug("Wrote to dev: %s", row[0])

            # We minus this because we don't reset count
            elif (count - dev) < test:
                test_writer.writerow(row)
                log.debug("Wrote to test: %s", row[0])

            else:
                train_writer.writerow(row)
                log.debug("Wrote to train: %s", row[0])

        # Make sure to close files
        all_file.close()
        dev_file.close()
        test_file.close()
        train_file.close()

    def _hard_link(self, item: Item) -> str:
        """Given a file, hardlink it into the output folder

        Returns
        -------
        The linked file path
        """
        src = item.get_absolute_media_path()
        dst: str = os.path.join(
            self.output_dir, "media", f"{item.media_name}.{self.media_type}"
        )
        os.link(src, dst)
        return dst

    def _create_csv(self, csv_name: str) -> None:
        """Creates and injects headers to the given csv file"""
        headers = ["wav_filename", "wav_filesize", "transcript"]
        with open(
            os.path.join(self.output_dir, f"{csv_name}.csv"), newline="", mode="w"
        ) as f:
            writer = csv.writer(f)
            writer.writerow(headers)
