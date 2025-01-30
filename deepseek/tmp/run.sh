#!/bin/bash
source venv/bin/activate
source .env

vllm serve deepseek-ai/DeepSeek-R1-Distill-Qwen-32B \
    --tensor-parallel-size 1 \
    --max-model-len 32768 \
    --enforce-eager
