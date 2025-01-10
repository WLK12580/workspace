
def extract_error(data:str):
    # 去掉前后刀括号
    data = data.strip("()")
    # 找到第一个逗号的位置
    comma_index = data.find(",")
    # 数字部分
    number = data[:comma_index].strip()
    # 文本部分
    text = data[comma_index + 1:].strip().strip()
    text = text[1:-1]
    return number, text
