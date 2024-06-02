#!/bin/bash
#python3 -m llama_cpp.server --hf_model_repo_id QuantFactory/Meta-Llama-3-8B-Instruct-GGUF --model 'Meta-Llama-3-8B-Instruct.Q8_0.gguf' --n_gpu_layers -1
python3 -m llama_cpp.server --config_file server_config.json