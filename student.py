messages = [
    {'role': 'system', 'content': '回复要使用中文'},
    {'role': 'user', 'content': '现在几点了'}
    ]

def toy_model(messages):
    if messages[-1]["role"] == "user" and '几点' in messages[-1]['content']:
        return {
            "role": "assistant", 
            "content": None, 
            "tool_call": {
                "name": "get_time", 
                "arguments": {}
                }
            }
    else:
        return {
            "role": "assistant", 
            "content": "收到:" + messages[-1]['content']
            }

def get_time():
    return "现在是下午茶时间"

tools = {"get_time": get_time}

while True:
    reply = toy_model(messages)
    messages.append(reply)
    if reply.get('tool_call'):
        tool_call = reply['tool_call']
        tool_result = tools[tool_call['name']](**tool_call['arguments'])
        messages.append({
            'role': 'tool',
            'name': tool_call['name'],
            'content': tool_result
        })
    else:
        break

print(messages)