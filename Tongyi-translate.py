import pandas as pd
import json
import random
import re
import os
import copy
import time
from itertools import groupby
from http import HTTPStatus
from tqdm import tqdm
import requests
import dashscope
from dashscope import Generation
from http import HTTPStatus
import csv
import pandas as pd


def chat_single_qwen(question_str, short = True):
    api_key_path = './api_key.txt'
    if not os.path.exists(api_key_path):
        raise Exception('api_key.txt not found')
    with open(api_key_path, 'r') as f:
        api_key = f.read().strip()
    dashscope.api_key=api_key # TOKEN HERE TODO
    if short:
        response=Generation.call(
            model=dashscope.Generation.Models.qwen_max,
            prompt=question_str,
        )
    else:
        time.sleep(6)
        response=Generation.call(
            model='qwen-max-longcontext',
            prompt=question_str,
        )

    return response
    
def question_answer(paper_info: dict):
    """
    输入：一篇论文的标题、发表的出版物名称、摘要，以及一段为什么和运动游戏预防老年人跌倒的原因
    """
    system_message = '''你是一名中文和英文的专业翻译官，你将收到一篇论文的标题、发表的出版物名称、摘要，以及一段为什么和运动游戏预防老年人跌倒的原因。 \
        请你将这些内容翻译成中文。各段内容中的[Title]、[Journal]、[Abstract]和[Response]不需要翻译，仍放在段落开头。'''

    title = paper_info['title']
    abstract = paper_info['abstract']
    journal = paper_info['journal']
    _response = paper_info['response']

    prompt = system_message + ' \n' + '[Title]: ' + title + ' \n' + '[Journal]: ' + journal + ' \n' + '[Abstract]: ' + abstract + ' \n' + '[Response]: ' + _response
    
    Max_try = 10
    tried = 0
    got_ans = False
    response = ''
    short = True
    print('[title]: ', title)
    while tried < Max_try and not got_ans:
        response = chat_single_qwen(prompt, short)
        if response.status_code == HTTPStatus.OK:
            got_ans = True
            print(f"[response]: {response}\n")
        elif "Range of input length should be" in str(response):
            print("[error]: Too long")
            short = False
        elif "Requests rate limit exceeded, please try again later." in str(response):
            print("[error]: Too quick")
            time.sleep(5)
        else:
            print('[error]: ', response)
        tried += 1
    return response
    

def main():
    in_file = './wos-1546/wos-YES-135.txt'
    out_file = './wos-1546/wos-YES-135-translated.txt'

    # 排除处理过的
    processed_title = set()
    if os.path.exists(out_file):
        with open(out_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if '[Title]:' in line:
                processed_title.add(line.split(']:')[1].strip())

    # 按行读取文件内容
    with open(in_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    left, right = 0, 0
    max_line = len(lines)
    index = 0
    while left < max_line - 1:
        print('[Index]: ', index)
        index += 1
        right = left + 1
        while right < max_line and len(lines[right].strip()) > 0:
            right += 1
        
        paper_info = {}
        for i in range(left, right):
            line = lines[i].strip()
            if '[Author]' in line:
                paper_info['author'] = line.split(']')[1].strip()
            elif'[Title]' in line:
                paper_info['title'] = line.split(']')[1].strip()
            elif '[Journal]' in line:
                paper_info['journal'] = line.split(']')[1].strip()
            elif '[Abstract]' in line:
                paper_info['abstract'] = line.split(']')[1].strip()
            elif '[Answer]' in line:
                paper_info['answer'] = line.split(']')[1].strip()
            elif '[Response]' in line:
                paper_info['response'] = line.split(']')[1].strip()
                for j in range(i+1, right):
                    paper_info['response'] += ('\n' + lines[j].strip())
        left = right
        if paper_info['title'] in processed_title:
            print('[Processed]: ', paper_info['title'])
            continue
        response = question_answer(paper_info).output.text
        translate = {}
        translate['Title'] = response[response.find('[Title]') + 8: response.find('[Journal]')].strip()
        translate['Journal'] = response[response.find('[Journal]') + 10: response.find('[Abstract]')].strip()
        translate['Abstract'] = response[response.find('[Abstract]') + 11: response.find('[Response]')].strip()
        translate['Response'] = response[response.find('[Response]') + 11: ].strip()

        with open(out_file, 'a', encoding='utf-8') as f:
            f.write('[Author]: ' + paper_info['author'] + '\n')
            f.write('[Title]: ' + paper_info['title'] + '\n')
            f.write('[Journal]: ' + paper_info['journal'] + '\n')
            f.write('[Abstract]: ' + paper_info['abstract'] + '\n')
            f.write('[Answer]: ' + paper_info['answer'] + '\n')
            f.write('[Response]: ' + paper_info['response'] + '\n')
            f.write('[Translate]: \n')
            f.write('[标题]: ' + translate['Title'] + '\n')
            f.write('[期刊]: ' + translate['Journal'] + '\n')
            f.write('[摘要]: ' + translate['Abstract'] + '\n')
            f.write('[回答]: ' + translate['Response'] + '\n\n')


if __name__ == '__main__':
    main()