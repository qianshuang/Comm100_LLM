# -*- coding: utf-8 -*

import torch
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams
from prompt_helper import *

model_path = "/opt/share/chatglm/models/finetune/Qwen2.5-14B-Instruct-FHTC"
llm = LLM(model=model_path, tensor_parallel_size=1, dtype=torch.bfloat16, trust_remote_code=True, gpu_memory_utilization=0.7)
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False, trust_remote_code=True)
sampling_params = SamplingParams(temperature=0, max_tokens=4096, stop_token_ids=[tokenizer.encode('<|eot_id|>')[0]])

origin_step = """你好"""

messages = [{"role": "system", "content": sys_message}, {"role": "user", "content": instruction_template.format(origin_step)}]
text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
output = llm.generate(text, sampling_params)

pred_answer = output[0].outputs[0].text
print(pred_answer)
