from va_config import CONFIG
from va_assistant import assistant, context,Action
import random

context.intent = 'find_out_wiki'
# context.target = 'wikipedia'
action = Action(context)

print(action.__dict__)
