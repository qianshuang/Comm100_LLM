# -*- coding: utf-8 -*

import os

from utils import *
from prompt_helper import *
from openai_helper import *

data_path = "data/kb_articles"
files = os.listdir(data_path)

train_data = []
for i, file in enumerate(files):
    print("{} of {} is processing...".format(i, len(files)))
    txt = read_txt(os.path.join(data_path, file))
    instruction = instruction_template.format(txt)
    gpt_res = parse_json(get_gpt_res([{"role": "system", "content": sys_message}, {"role": "user", "content": instruction}]))
    for qa in gpt_res["Q&A"]:
        print(qa)
        train_data.append({"instruction": qa["Question"], "input": "", "output": qa["Answer"]})
write_json_file(train_data, "data/Comm100_LLM.json")
print("qa_dict length：{}".format(len(train_data)))
