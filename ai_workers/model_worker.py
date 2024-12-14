from torch.cuda import OutOfMemoryError
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ModelWorker:
    def __init__(self, device_id: int):
        self.device_id = device_id
        self.logger = logging.getLogger(__name__)

    def _process_text(self, text: str) -> Optional[str]:
        """Process input text."""
        # Implementation
        return text

    def handle_inference(self, input_text: str) -> Optional[str]:
        """Handle model inference with proper error handling."""
        try:
            result = self._process_text(input_text)
            logger.info("Processed text: %s", input_text[:50])
            return result
        except OutOfMemoryError as e:
            logger.error("GPU error: %s", str(e))
            return None