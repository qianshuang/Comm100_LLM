# -*- coding: utf-8 -*

from openai_helper import *

prompt_messages = [{"role": "user", "content": "Hello"}]
print(get_gpt_res(prompt_messages))
