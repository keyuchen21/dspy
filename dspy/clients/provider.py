from concurrent.futures import Future
from abc import abstractmethod
from threading import Thread
from typing import Any, Dict, List, Optional

from dspy.clients.utils_finetune import DataFormat
from dspy.utils.logging import logger


class TrainingJob(Future):
    def __init__(
        self,
        thread: Thread,
        model: str,
        train_data: List[Dict[str, Any]],
        train_kwargs: Optional[Dict[str, Any]] = None,
        data_format: Optional[DataFormat] = None,
    ):
        self.thread = thread
        self.model = model
        self.train_data = train_data
        self.train_kwargs = train_kwargs or {}
        self.data_format = data_format
        super().__init__()

    # Subclasses should override the cancel method to cancel the job; then call
    # the super's cancel method so that the future can be cancelled.
    def cancel(self):
        super().cancel()

    @abstractmethod
    def status(self):
        raise NotImplementedError


class Provider:
    
    def __init__(self):
        self.finetunable = False
        self.TrainingJob = TrainingJob

    @staticmethod
    def is_provider_model(model: str) -> bool:
        # Subclasses should actually check whether a model is supported if they
        # want to have the model provider auto-discovered.
        return False

    @staticmethod
    def launch(model: str, launch_kwargs: Optional[Dict[str, Any]]=None):
        msg = f"`launch()` is called for the auto-launched model {model}"
        msg += " -- no action is taken!"
        logger.info(msg)
    
    @staticmethod
    def kill(model: str, launch_kwargs: Optional[Dict[str, Any]]=None):
        msg = f"`kill()` is called for the auto-launched model {model}"
        msg += " -- no action is taken!"
        logger.info(msg)
    
    @staticmethod
    def finetune(
        job: TrainingJob,
        model: str,
        train_data: List[Dict[str, Any]],
        train_kwargs: Optional[Dict[str, Any]] = None,
        data_format: Optional[DataFormat] = None,
    ) -> str:
        raise NotImplementedError