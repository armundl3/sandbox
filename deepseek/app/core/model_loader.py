import torch
from vllm import LLM, SamplingParams
from app.core.config import settings

class ModelLoader:
    """Singleton class to manage LLM model loading and access."""
    
    _instance = None
    _model: LLM | None = None

    def __new__(cls) -> "ModelLoader":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def model(self) -> LLM:
        """Get the loaded model instance."""
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        return self._model

    async def load_model(self) -> LLM:
        """Load the LLM model if not already loaded."""
        if self._model is None:
            device = "mps" if torch.backends.mps.is_available() else "cpu"
            self._model = LLM(
                model=settings.MODEL_NAME,
                max_model_len=settings.MAX_MODEL_LEN,
                dtype="float16", 
                max_batch_size=settings.MAX_BATCH_SIZE,
                device=device
            )
        return self._model