
# 读取输入文件
def read_input(input_file_path):
    txt_lines = open(input_file_path).readlines()

    input_data = {}

    rect = []

    for index, txt_line in enumerate(txt_lines):
        if index == 0:
            input_data['ALPHA'] = float(txt_line.strip('\n').split('=')[-1])
        elif index == 1:
            input_data['BETA'] = float(txt_line.strip('\n').split('=')[-1])
        elif index == 2:
            input_data['OMEGA'] = float(txt_line.strip('\n').split('=')[-1])
        else:
            rect.append([float(item) for item in txt_line.strip('\n').split(',')])

    input_data['rect'] = rect

    return input_data
