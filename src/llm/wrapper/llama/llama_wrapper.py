from typing import Tuple
import os
import sys
import torch
import fire
import time
import json

from pathlib import Path
from typing import Dict

from fairscale.nn.model_parallel.initialize import initialize_model_parallel

from llm.wrapper.llama.llama import ModelArgs, Transformer, Tokenizer, LLaMA

from llm.wrapper.llm_wrapper import LLMWrapper

def setup_model_parallel() -> Tuple[int, int]:
    local_rank = int(os.environ.get("LOCAL_RANK", -1))
    world_size = int(os.environ.get("WORLD_SIZE", -1))

    torch.distributed.init_process_group("nccl")
    initialize_model_parallel(world_size)
    torch.cuda.set_device(local_rank)

    # seed must be the same in all processes
    torch.manual_seed(1)
    return local_rank, world_size


def load(
    ckpt_dir: str,
    tokenizer_path: str,
    local_rank: int,
    world_size: int,
    max_seq_len: int,
    max_batch_size: int,
) -> LLaMA:
    start_time = time.time()
    checkpoints = sorted(Path(ckpt_dir).glob("*.pth"))
    assert world_size == len(
        checkpoints
    ), f"Loading a checkpoint for MP={len(checkpoints)} but world size is {world_size}"
    ckpt_path = checkpoints[local_rank]
    print("Loading")
    checkpoint = torch.load(ckpt_path, map_location="cpu")
    with open(Path(ckpt_dir) / "params.json", "r") as f:
        params = json.loads(f.read())

    model_args: ModelArgs = ModelArgs(
        max_seq_len=max_seq_len, max_batch_size=max_batch_size, **params
    )
    tokenizer = Tokenizer(model_path=tokenizer_path)
    model_args.vocab_size = tokenizer.n_words
    torch.set_default_tensor_type(torch.cuda.HalfTensor)
    model = Transformer(model_args)
    torch.set_default_tensor_type(torch.FloatTensor)
    model.load_state_dict(checkpoint, strict=False)

    generator = LLaMA(model, tokenizer)
    print(f"Loaded in {time.time() - start_time:.2f} seconds")
    return generator

def init_generator():

    ckpt_dir = os.getenv("LLAMA_CHECKPOINT_DIR")
    tokenizer_path = os.getenv("LLAMA_TOKENIZER_PATH")
    
    max_batch_size = 32
    max_seq_len = 512

    local_rank, world_size = setup_model_parallel()
    if local_rank > 0:
        sys.stdout = open(os.devnull, "w")

    generator = load(
        ckpt_dir, tokenizer_path, local_rank, world_size, max_seq_len, max_batch_size
    )

    return generator

def generate(prompt):
    print(generator.generate(
        [prompt], max_gen_len=256, temperature=temperature, top_p=top_p
    )[0])
    print()

class LLamaWrapper(LLMWrapper):

    def __init__(self):
        self.generator = init_generator()

    def generate_response(self, input_str : str, args : Dict):
        
        max_gen_len = int(args["max_new_tokens"]) if "max_new_tokens" in args.keys() else 256
        temperature = float(args["temperature"]) if "temperature" in args.keys() else 0.8
        top_p = 0.95

        response = self.generator.generate(
            [input_str], max_gen_len=max_gen_len, temperature=temperature, top_p=top_p
        )[0]
        return response

    