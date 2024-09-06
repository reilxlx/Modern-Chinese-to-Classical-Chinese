import os
import json
import random
from pathlib import Path

def process_bitext(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pairs = content.split('\n\n')
    processed_pairs = []
    
    for pair in pairs:
        parts = pair.split('现代文：')
        if len(parts) == 2:
            ancient = parts[0].replace('古文：', '').strip()
            modern = parts[1].strip()
            processed_pairs.append((ancient, modern))
    
    return processed_pairs

def get_source(file_path):
    parts = file_path.parts[1:-1]
    return '《' + '·'.join(parts) + '》'

def create_jsonl(root_dir, output_file):
    root_path = Path(root_dir)
    
    with open(output_file, 'w', encoding='utf-8') as out_file:
        for file_path in root_path.rglob('bitext.txt'):
            pairs = process_bitext(file_path)
            source = get_source(file_path)
            
            for ancient, modern in pairs:
                if random.random() < 0.3:  # 30% 概率现代文作为input
                    instruction = f"你是一位精通中国古代文学和现代汉语的语言专家。你的任务是将给定的现代汉语准确转换成古文，保持原文的意思和风格，同时使用符合古代文学特征的语言。请将以下现代文转换为古文："
                    data = {
                        "instruction": instruction,
                        "input": modern,
                        "output": ancient
                    }
                else:  # 70% 概率古文作为input
                    instruction = f"你是一位精通中国古代文学和现代汉语的语言专家。你的任务是将给定的古文段落准确翻译成现代汉语，保持原文的意思和风格，同时使用当代读者容易理解的语言。请将以下{source}中的古文翻译成现代文："
                    data = {
                        "instruction": instruction,
                        "input": ancient,
                        "output": modern
                    }
                
                json.dump(data, out_file, ensure_ascii=False)
                out_file.write('\n')

root_directory = './your_root_directory'
output_file = 'output.jsonl'
create_jsonl(root_directory, output_file)
