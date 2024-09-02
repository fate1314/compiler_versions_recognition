import csv
import os
from collections import Counter

file_count = 0  # 初始化文件计数器


def process_folder(folder_name):
    data = []
    global file_count
    file_count += 1  # 每处理一个文件夹，计数器加一
    for filename in os.listdir(folder_name):
        print(f"Processing {filename}...")
        if 'test' not in filename:
            print(f"Skipping {filename}...")
            continue
        file_path = os.path.join(folder_name, filename)
        with open(file_path, 'r') as file:
            word_counter = Counter()
            bigram_counter = Counter()
            first_word_list = []

            for line in file:
                words = line.strip().split()
                if not words:
                    continue
                first_word_list.append(words[0])
                word_counter.update(words)
                bigram_counter.update(zip(words[:-1], words[1:]))

            # 计算四元组（四个连续单词）的频率
            quadgram_counter = Counter(
                zip(first_word_list[:-3], first_word_list[1:-2],
                    first_word_list[2:-1], first_word_list[3:]))

            # 筛选频率大于10的特征
            word_features = {
                word: count
                for word, count in word_counter.items() if count > 10
            }
            bigram_features = {
                " ".join(bigram): count
                for bigram, count in bigram_counter.items() if count > 10
            }
            quadgram_features = {
                " ".join(quadgram): count
                for quadgram, count in quadgram_counter.items() if count > 10
            }

            # 构建一行数据
            features = {
                **word_features,
                **bigram_features,
                **quadgram_features
            }
            features['label'] = file_count  # 标签为当前文件的编号

            data.append(features)

    return data


def save_to_csv(data, output_file):
    keys = set()
    for row in data:
        keys.update(row.keys())

    keys = sorted(keys)  # 按字母排序，确保一致性
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


# 定义已处理的文件夹列表
processed_folders = [
    '8.4.0_processed', '10.2.0_processed', '11.3.0_processed',
    '12.2.0_processed', '13.2.0_processed'
]

# 初始化用于保存所有文件夹数据的列表
all_data = []

# 遍历每个文件夹并处理数据
for folder in processed_folders:
    folder_data = process_folder(folder)
    all_data.extend(folder_data)

# 保存合并后的数据到CSV文件
save_to_csv(all_data, 'no_our_data.csv')
