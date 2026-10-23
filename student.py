messages = [
    {'role': 'system', 'content': '回复要使用中文'},
    {'role': 'user', 'content': '现在几点了，天气怎么样'}
    ]

def toy_model(messages):
    if messages[-1]['role'] == 'user' and '几点' in messages[-1]['content'] and '天气' in messages[-1]['content']:
        return {
            "role": "assistant",
            "content": None,
            "tool_call": [
                {
                    "name": "get_time",
                    "arguments": {}
                    }, 
                {
                    "name": "get_weather",
                    "arguments": {'city': '佛山'}
                    }
            ]
        }
    elif messages[-1]['role'] == 'user' and '天气' in messages[-1]['content']:
        return {
            "role": "assistant",
            "content": None,
            "tool_call":[{
                "name": "get_weather",
                "arguments": {'city': '佛山'}
            }]
        }
    elif messages[-1]["role"] == "user" and '几点' in messages[-1]['content']:
        return {
            "role": "assistant", 
            "content": None, 
            "tool_call": [{
                "name": "get_time", 
                "arguments": {}
                }]
            }
    else:
        return {
            "role": "assistant", 
            "content": "收到:" + messages[-1]['content']
            }

def get_time():
    return "现在是下午茶时间"

def get_weather(city):
    return f"{city}: 晴， 25°C "

tools = {
    "get_time": get_time,
    "get_weather": get_weather}

while True:
    reply = toy_model(messages)
    messages.append(reply)
    if reply.get('tool_call'):
        for tool_call in reply['tool_call']:
            tool_result = tools[tool_call['name']](**tool_call['arguments'])
            messages.append({   
                'role': 'tool',
                'name': tool_call['name'],  # 工具名称
                'content': tool_result  # 工具结果          
            })
        # tool_call = reply['tool_call']
        # tool_result = tools[tool_call['name']](**tool_call['arguments'])
        # messages.append({
        #     'role': 'tool',
        #     'name': tool_call['name'],
        #     'content': tool_result
        # })
    else:
        break

for msg in messages:
    print(msg)