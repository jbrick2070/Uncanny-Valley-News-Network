from __future__ import annotations
import abc

class VideoBackend(abc.ABC):
    """Base interface for video generation engines."""

    @abc.abstractmethod
    def generate_segment(self, prompt: str) -> Optional[str]:
        """
        Generate a video segment given the prompt.
        Returns the path to the generated MP4, or None if failed.
        """
        pass
