messages = [
    {'role': 'system', 'content': '回复要使用中文'},
    {'role': 'user', 'content': '现在几点了，天气怎么样'}
    ]

tool_schemas = [
    {
        "name": "get_time",
        "description": "获取当前时间",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    },
    {
        "name": "get_weather",
        "description": "获取天气",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "城市"}}
        }
    }
]

def toy_model(messages, tool_schemas):
    if messages[-1]['role'] == 'user' and '几点' in messages[-1]['content'] and '天气' in messages[-1]['content']:
        return {
            "role": "assistant",
            "content": None,
            "tool_call": [{"name": tool_schemas[0]['name'], "arguments": {}},
            {"name": tool_schemas[1]['name'], "arguments": {"city": "佛山"}}
            ]
        }
    elif messages[-1]['role'] == 'user' and '天气' in messages[-1]['content']:
        return {
            "role": "assistant",
            "content": None,
            "tool_call":[{"name": tool_schemas[1]['name'], "arguments": {"city": "佛山"}}]
        }
    elif messages[-1]["role"] == "user" and '几点' in messages[-1]['content']:
        return {
            "role": "assistant", 
            "content": None, 
            "tool_call": [{"name": tool_schemas[0]['name'], "arguments": {}}]
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

impls = {
    "get_time": get_time,
    "get_weather": get_weather}

max_step = 5
steps = 0
while steps < max_step:
    steps += 1
    reply = toy_model(messages, tool_schemas)
    messages.append(reply)
    if reply.get('tool_call'):
        for tool_call in reply['tool_call']:
            try:
                tool_result = impls[tool_call['name']](**tool_call['arguments'])
                messages.append({   
                    'role': 'tool',
                    'name': tool_call['name'],  
                    'content': tool_result        
                })
            except Exception as e:
                messages.append({
                    'role': 'tool',
                    'name': tool_call['name'], 
                    'content': f'Impl异常: {e}'
                })
    else:
        break

if steps >= max_step and messages[-1].get('tool_call'):
    messages.append({
        'role': 'assistant',
        'content': f'达到步数上限（max_step={max_step}），已停下'
    })

for msg in messages:
    print(msg)