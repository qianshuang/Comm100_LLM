# -*- coding: utf-8 -*

from utils import *
import torch
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams

# 模型调用
model_path = "/opt/share/chatglm/models/finetune/Meta-Llama-3-8B-Instruct-Comm100"
llm = LLM(model=model_path, tensor_parallel_size=1, dtype=torch.bfloat16, trust_remote_code=True, gpu_memory_utilization=0.7)
tokenizer = AutoTokenizer.from_pretrained(model_path, use_fast=False, trust_remote_code=True)
sampling_params = SamplingParams(temperature=0, max_tokens=4096, stop_token_ids=[tokenizer.encode('<|eot_id|>')[0]])


def get_llm_res(question):
    messages = [{"role": "user", "content": question}]
    text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    output = llm.generate(text, sampling_params)
    pred_answer = output[0].outputs[0].text
    return pred_answer


train_data = load_json_file("data/Comm100_LLM.json_bak")
for case in load_json_file("data/add_kg.json"):
    train_data.insert(0, {"instruction": case["question"], "input": "", "output": case["answer"]})
# train_data = train_data[:100]

qa_dict_list = []
for index, row in enumerate(train_data):
    print("{} is processing...".format(index))
    llm_res = get_llm_res(row['instruction'])
    if llm_res.strip() == row["output"].strip():
        print("{} is the same...".format(index))
        continue

    qa_dict = {"conversations": [{"from": "human", "value": row['instruction']}],
               "chosen": {"from": "gpt", "value": row["output"]},
               "rejected": {"from": "gpt", "value": llm_res}}
    qa_dict_list.append(qa_dict)
write_json_file(qa_dict_list, "data/Comm100_LLM_dpo.json")
print("train length: {}".format(len(qa_dict_list)))
