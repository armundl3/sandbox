from pydantic import BaseModel, Field
from typing import Optional, List

class GenerationParameters(BaseModel):
    """Parameters for controlling text generation."""
    max_tokens: int = Field(default=100, ge=1, le=32768, description="Maximum number of tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p sampling threshold") 
    stop_sequences: Optional[List[str]] = Field(default=None, description="Sequences that will stop generation")

class GenerateRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., description="Input text for generation")
    parameters: GenerationParameters = Field(default_factory=GenerationParameters)

class TokenUsage(BaseModel):
    """Token usage statistics."""
    prompt_tokens: int = Field(..., description="Number of tokens in the prompt")
    completion_tokens: int = Field(..., description="Number of tokens in the completion")
    total_tokens: int = Field(..., description="Total number of tokens used")

class GenerateResponse(BaseModel):
    """Response model for text generation."""
    text: str = Field(..., description="Generated text output")
    usage: TokenUsage