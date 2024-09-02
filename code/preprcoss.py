import os
import re

def process_assembly_file(input_file, output_file):
    # 读取原始汇编文件
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 创建一个新的列表来存储修改后的内容
    processed_lines = []

    # 遍历原文件的每一行
    for line in lines:
        # 将逗号替换为空格
        line = line.replace(',', ' ')

        # 去除每行的前后空格
        stripped_line = line.strip()

        # 跳过以 . 开头或以 : 结尾的行
        if stripped_line.startswith('.') or stripped_line.endswith(':'):
            continue

        # 按空格分割行内的内容，得到每个单词
        words = re.split(r'\s+', stripped_line)

        # 处理每个单词
        processed_words = []
        for word in words:
            # 查找是否有括号，并替换为括号内的内容
            match = re.search(r'\((%[a-zA-Z0-9]+)\)', word)
            if match:
                word = match.group(1)

            # 处理以 $ 开头的单词
            if word.startswith('$'):
                if re.match(r'\$\d+', word):  # 如果 $ 后跟数字
                    word = '$0'
                elif re.match(r'\$-', word):  # 如果 $ 后跟负号
                    word = '$0'
                elif word.startswith('$.'):  # 如果 $ 后跟 .
                    word = '$.'
                elif word.startswith('$g'):  # 如果 $ 后跟 g
                    word = '$g'

            processed_words.append(word)

        # 将处理后的单词重新组合成一行
        processed_line = ' '.join(processed_words)
        processed_lines.append(processed_line + '\n')  # 保持行的格式

    # 写入新的汇编文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.writelines(processed_lines)


def process_all_files(input_folder, output_folder):
    # 如果输出文件夹不存在，则创建
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        # 构造完整的文件路径
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename)

        # 处理每个文件
        process_assembly_file(input_file, output_file)


input_folders = ['8.4.0', '10.2.0', '11.3.0', '12.2.0', '13.2.0']
output_folders = [f"{folder}_processed" for folder in input_folders]

print(output_folders)

# 处理所有文件
for input_folder, output_folder in zip(input_folders, output_folders):
    process_all_files(input_folder, output_folder)

print("所有文件处理完毕。")
