from tool_schemas import tool_schemas
from impls import impls

messages = [
    {'role': 'system', 'content': '回复要使用中文'},
    {'role': 'user', 'content': '现在几点了，天气怎么样'}
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

max_step = 5
steps = 0

def execute_tool_calls(tool_calls:list, impls:dict) -> list:
    results = []
    for tool in tool_calls:
        name = tool['name']
        args = tool.get('arguments',{})
        try:
            content = impls[name](**args)
        except Exception as e:
            content = f'Impl异常: {e}'
        results.append({
            'role' : 'tool',
            'name' : name,
            'content' : str(content)
        })
    return results

while steps < max_step:
    steps += 1
    reply = toy_model(messages, tool_schemas)
    messages.append(reply)
    if reply.get('tool_call'):
        for msg in execute_tool_calls(reply['tool_call'], impls):
            messages.append(msg)
    else:
        break

if steps >= max_step and messages[-1].get('tool_call'):
    messages.append({
        'role': 'assistant',
        'content': f'达到步数上限（max_step={max_step}），已停下'
    })

for msg in messages:
    print(msg)