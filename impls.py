def get_time():
    return "现在是下午茶时间"

def get_weather(city):
    return f"{city}: 晴， 25°C "

impls = {
    "get_time": get_time,
    "get_weather": get_weather}