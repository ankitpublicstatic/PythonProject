from transformers import AutoTokenizer
import threading

# Load once (global singleton)
_tokenizer_lock = threading.Lock()
_tokenizer = None

def get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        with _tokenizer_lock:
            if _tokenizer is None:
                _tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B-Instruct")
    return _tokenizer

def count_tokens(text: str) -> int:
    tokenizer = get_tokenizer()
    tokens = tokenizer.encode(text)
    return len(tokens)

def calculate_usage(prompt: str, completion: str):
    prompt_tokens = count_tokens(prompt)
    completion_tokens = count_tokens(completion)

    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": prompt_tokens + completion_tokens,
    }


