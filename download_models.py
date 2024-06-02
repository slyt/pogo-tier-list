import os
from huggingface_hub import snapshot_download

model_directory = "models"

# download reasoning model
# https://huggingface.co/QuantFactory/Meta-Llama-3-8B-Instruct-GGUF/tree/main
reasoning_model_repo_id = "QuantFactory/Meta-Llama-3-8B-Instruct-GGUF"
reasoning_model_name = "Meta-Llama-3-8B-Instruct.Q8_0.gguf"

# Make directory if it doesn't exist using reasoning_model_repo_id as name
reasoning_model_dir = os.path.join(model_directory, reasoning_model_repo_id)
os.makedirs(reasoning_model_dir, exist_ok=True)

snapshot_download(repo_id=reasoning_model_repo_id, allow_patterns=[reasoning_model_name, "*.json"], local_dir=reasoning_model_dir)


# download function calling model
# https://huggingface.co/meetkai/functionary-small-v2.4-GGUF/tree/main
function_model_repo_id = "meetkai/functionary-small-v2.4-GGUF"
# function_model_name = "functionary-small-v2.4.Q8_0.gguf"
function_model_name = "functionary-small-v2.4.Q4_0.gguf"

# Make directory if it doesn't exist using function_model_repo_id as name
function_model_dir = os.path.join(model_directory, function_model_repo_id)
os.makedirs(function_model_dir, exist_ok=True)


snapshot_download(repo_id=function_model_repo_id, allow_patterns=[function_model_name, "tokenizer.model", "*.json"], local_dir=function_model_dir)

