from fastapi import APIRouter, HTTPException
from app.schemas.request import GenerateRequest, GenerateResponse, GenerationParameters, TokenUsage
from app.core.model_loader import ModelLoader
from vllm import SamplingParams

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate_text(request: GenerateRequest):
    """Generate text using the loaded LLM model."""
    try:
        # Get model instance
        model = ModelLoader().model
        
        # Create sampling parameters from request
        sampling_params = _create_sampling_params(request.parameters)
        
        # Generate text
        outputs = model.generate(request.prompt, sampling_params)
        if not outputs:
            raise HTTPException(status_code=500, detail="Generation failed")
            
        # Extract generated text and validate output structure
        if not outputs[0].outputs:
            raise HTTPException(status_code=500, detail="No output generated")
        generated_text = outputs[0].outputs[0].text
        if not generated_text:
            raise HTTPException(status_code=500, detail="Generated text is empty")
        
        # Calculate token usage
        usage = _calculate_token_usage(request.prompt, generated_text)
        
        return GenerateResponse(text=generated_text, usage=usage)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def _create_sampling_params(params: GenerationParameters) -> SamplingParams:
    """Create VLLM sampling parameters from request parameters."""
    return SamplingParams(
        max_tokens=params.max_tokens,
        temperature=params.temperature,
        top_p=params.top_p,
        stop=params.stop_sequences
    )

def _calculate_token_usage(prompt: str, generated_text: str) -> TokenUsage:
    """Calculate token usage statistics."""
    prompt_tokens = len(prompt.split())
    completion_tokens = len(generated_text.split())
    
    return TokenUsage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens
    )