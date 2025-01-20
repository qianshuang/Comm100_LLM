# -*- coding: utf-8 -*

import os
import random

from sklearn.model_selection import train_test_split

from utils import *
from prompt_helper import *
from openai_helper import *

# 生成训练数据
# data_path = "data/kb_articles"
# files = os.listdir(data_path)
# train_data = []
# for i, file in enumerate(files):
#     print("{} of {} is processing...".format(i, len(files)))
#     txt = read_txt(os.path.join(data_path, file))
#     instruction = instruction_template.format(txt)
#     gpt_res = parse_json(get_gpt_res([{"role": "system", "content": sys_message}, {"role": "user", "content": instruction}]))
#     for qa in gpt_res["Q&A"]:
#         print(qa)
#         train_data.append({"instruction": qa["Question"], "input": "", "output": qa["Answer"]})
# write_json_file(train_data, "data/Comm100_LLM.json")
# print("qa_dict length：{}".format(len(train_data)))

# 生成测试数据
# test_data = []
# train_data = load_json_file("data/Comm100_LLM.json")
# sample_data = random.sample(train_data, 10)
# for sd in sample_data:
#     origin_question = sd["instruction"]
#
#     rephrase_instruction = rephrase_instruction_template.format(origin_question)
#     gpt_res = parse_json(get_gpt_res([{"role": "system", "content": rephrase_sys_message}, {"role": "user", "content": rephrase_instruction}]))
#     new_question = gpt_res["new_question"]
#
#     test_data.append({"origin_question": origin_question, "identical_question": new_question, "answer": sd["output"]})
# write_json_file(test_data, "data/Comm100_LLM_test.json")

# 补充训练数据
train_data = load_json_file("data/Comm100_LLM.json")
for case in load_json_file("data/add_kg.json"):
    train_data.insert(0, {"instruction": case["question"], "input": "", "output": case["answer"]})
write_json_file(train_data, "data/Comm100_LLM.json")
print("train length：{}".format(len(train_data)))

# 扩展训练数据
train_data = []
for i, case in enumerate(load_json_file("data/Comm100_LLM.json")):
    if i >= 100:
        break
    else:
        print("{} is processing...".format(i))
    origin_question = case["instruction"]
    expand_instruction = expand_instruction_template.format(origin_question)
    gpt_res = parse_json(get_gpt_res([{"role": "system", "content": rephrase_sys_message}, {"role": "user", "content": expand_instruction}]))
    new_questions = gpt_res["new_questions"]
    for nq in new_questions:
        train_data.append({"instruction": nq, "input": "", "output": case["output"]})
    train_data.append({"instruction": origin_question, "input": "", "output": case["output"]})

train_data_remaining, test_data = train_test_split(train_data, test_size=10, random_state=42)
write_json_file(train_data_remaining, "data/Comm100_LLM.json")
write_json_file(test_data, "data/Comm100_LLM_test.json")
print("train length：{}, test length: {}".format(len(train_data_remaining), len(test_data)))
