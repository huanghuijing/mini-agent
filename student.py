messages = [
    {'role': 'system', 'content': '回复要使用中文'},
    {'role': 'user', 'content': '你好'}
    ]


def toy_model(messages):
    message = {}
    message['role'] = 'assistant'
    message['content'] = '收到:' + messages[-1]['content']
    return message

messages.append(toy_model(messages))
    

print(messages)
