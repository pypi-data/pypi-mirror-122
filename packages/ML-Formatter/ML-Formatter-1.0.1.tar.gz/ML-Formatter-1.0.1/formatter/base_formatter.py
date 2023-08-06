import logging

log = logging.getLogger(__name__)


class BaseFormatter:
    def __init__(
        self,
        media_dir,
        transcript_dir,
        output_dir,
        media_type,
        transcript_type,
        train,
        test,
        val,
        dont_shuffle,
    ):
        self.media_dir = media_dir
        self.transcript_dir = transcript_dir
        self.output_dir = output_dir
        self.media_type = media_type
        self.transcript_type = transcript_type
        self.train_percent = train
        self.test_percent = test
        self.val_percent = val
        self.dont_shuffle = dont_shuffle
        log.info("Initialized %s", self.__class__.__name__)

    def run(self):
        raise NotImplementedError
