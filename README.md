# How to run Qwen3 using vLLM locally for coding tasks

## What we need
- OS - Ubuntu 22/24 (_should work on Windows since we are using docker_)
- Nvidia GPU (tested on RTX 3080-10GB)
- Docker installed
- Docker configured to use NVidia GPU
- Visual Studio Code with roocode (for testing)

```bash
# Stats from testing on RTX 3080 with 10GB VRAM
- Model weights take 4.22GiB
- Non-torch memory takes 0.05GiB
- PyTorch activation peak memory takes 0.48GiB
- Rest of the memory reserved for KV Cache is 3.92GiB
```

## Test if GPU is configured with docker runtime

```bash
# Run the following command to test Docker + GPU setup
# You should see the nvidia-smi output
docker run --rm --gpus all nvidia/cuda:12.2.0-base-ubuntu22.04 nvidia-smi
```

## Setup vLLM + Open WebUI with docker and the model

```bash
# 1. Git Clone this folder
$ git https://github.com/sukesh-ak/Run-Qwen3-vLLM-Locally.git vllm
$ cd vllm
```

```bash
# 2. Run the container. Force recreate is for tweaking values and re-running if required
$ docker compose --env-file env-qwen3-4b up -d --force-recreate
```

```bash
# 3. Once the container is running, use the following command to monitor the logs
# You can see if everything is working fine or not (OOM?)
$ docker logs -f vllm-qwen3
```

## Time to test with python

```bash
# 4. Create and activate python env
$ python3 -m venv vllm-env
$ source vllm-env/bin/activate

# Use the pytest.py from this repo
$ python pytest.py

# You can also use the CLI parameters to override prompt
$ python pytest.py --prompt "write a websocket client in c++ using cpp-httplib" 

# Override prompt and system prompt
$ python pytest.py \
	--system-prompt "You are an expert in C & C++, if asked for python, just say Python is a snake" \
	--prompt "write a websocket server in python"
```

## Configure and use `Open WebUI`
_Make sure both containers are up and running.  
First run will take more time for downloading the model._
```bash
# 5. Configure and use Open WebUI
Open WebUI chat interface at http://localhost:3000  
You can use IP instead of localhost
```

1. Create an Admin account
2. Once logged-in, goto `Admin Panel`
3. Click `Settings > Connections`
4. Click + under `OpenAi API`
5. Add the following  
URL: http://host.docker.internal:8000/v1   
Key: abc  
Prefix ID: vllm  
Model IDs: Qwen/Qwen3-4B-Instruct-2507-FP8
6. Click `save`

No you can select the model and start chatting.

## Using with VS Code extension
- For `roocode`, you can select `OpenAI compatible` and use the docker url, api and model name

## Summary
- We are using `Qwen/Qwen3-4B-Instruct-2507-FP8` since the GPU being tested on has only 10GB VRAM.  
- GPU with larger VRAM? use larger model from here = >[Qwen3 models are here](https://huggingface.co/Qwen)

### Tweaking
Now you can tweak the values if required for different models from the environment file `env-qwen3-4b` or create a new env file if you change the model.

You can play with this value which is currently at `55K context size`.
- Max model length => `max-model-len`


## SPONSORING
[![Github sponsor](https://img.shields.io/static/v1?label=Click%20here%20to%20Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23FF007F&style=for-the-badge)](https://github.com/sponsors/sukesh-ak)  

Your sponsorship would help me not only to maintain projects but also to work on more Open source projects and other useful additions. If you're an individual user who has enjoyed my projects or benefited from my community work, please consider donating as a sign of appreciation. If you run a business that uses my work in your products, sponsoring my development makes good business sense: it ensures that the projects your product relies on stay healthy and actively maintained.

Thank you for considering supporting my work!