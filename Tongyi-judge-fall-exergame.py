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

def get_answer(answer):

    if 'YES' in answer:
        return 'YES'
    elif 'NO' in answer:
        return 'NO'
    else:
        return 'UNCERTAIN'
    
def question_answer(paper_info: dict):
    """
    输入：一篇论文的标题、摘要和发表的出版物名称
    输出：是否是关于利用运动游戏（Exergame）干预预防老年人跌倒的研究
    具体要求：
    P-人群：有老年人即可
    I-干预措施：运动游戏干预（虚拟现实、电子游戏、视频游戏等都算，只要有互动性和趣味性或有认知相关的训练就行）
    O-结局指标：跌倒发生率（要有关于跌倒次数的结果报告才能纳入）
    S-研究设计：随机对照实验（荟萃、综述、可行性分析那些没数据的不算，试点研究有跌倒发生率也可）。
    """
    system_message = '''You are now an expert on using exergames to prevent falls in the elderly. \
    You will be given a paper title, journal name, and abstract. \
    You will need to answer the following question: Is the paper about the use of exergames to prevent falls in the elderly? \
    The answer should be one of "YES", "NO", or "UNCERTAIN".\
    The criteria for judgment are as follows: \
    (1) The intervention targets should include older people; \
    (2) The intervention should be an exergame (e.g., virtual reality, video games, electronic games, cognitive training, etc.); \
    (3) The paper should include randomized controlled trials, and the results should be reported. \
    (4) Papers related to meta-analysis, review, and feasibility analysis without original data should not be included. \
    '''

    title = paper_info['title']
    abstract = paper_info['abstract']
    journal = paper_info['journal']
    prompt = system_message + ' \n' + '[Title]: ' + title + ' \n' + '[Journal]: ' + journal + ' \n' + '[Abstract]: ' + abstract
    Max_try = 10
    tried = 0
    got_ans = False
    answer = ''
    response = ''
    short = True
    print('[title]: ', title)
    while tried < Max_try and not got_ans:
        response = chat_single_qwen(prompt, short)
        if response.status_code == HTTPStatus.OK:
            got_ans = True
            answer = get_answer(response.output.text)
            print(f"[answer]: {answer}")
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
    return answer, response
    

def main():
# # test
#     paper_info_1 = {
#         'title': 'The effectiveness and cost-effectiveness of strength and balance Exergames to reduce falls risk for people aged 55years and older in UK assisted living facilities: a multi-centre, cluster randomised controlled trial',
#         'journal': 'BMC MEDICINE',
#         'abstract': '''Falls are the leading cause of fatal and non-fatal unintentional injuries in older people. The use of Exergames (active, gamified video-based exercises) is a possible innovative, community-based approach. This study aimed to determine the effectiveness of a tailored OTAGO/FaME-based strength and balance Exergame programme for improving balance, maintaining function and reducing falls risk in older people.MethodsA two-arm cluster randomised controlled trial recruiting adults aged 55years and older living in 18 assisted living (sheltered housing) facilities (clusters) in the UK. Standard care (physiotherapy advice and leaflet) was compared to a tailored 12-week strength and balance Exergame programme, supported by physiotherapists or trained assistants. Complete case analysis (intention-to-treat) was used to compare the Berg Balance Scale (BBS) at baseline and at 12weeks. Secondary outcomes included fear of falling, mobility, fall risk, pain, mood, fatigue, cognition, healthcare utilisation and health-related quality of life, and self-reported physical activity and falls.ResultsEighteen clusters were randomised (9 to each arm) with 56 participants allocated to the intervention and 50 to the control (78% female, mean age 78years). Fourteen participants withdrew over the 12weeks (both arms), mainly for ill health. There was an adjusted mean improvement in balance (BBS) of 6.2 (95% CI 2.4 to 10.0) and reduced fear of falling (p=0.007) and pain (p=0.02) in the Exergame group. Mean attendance at sessions was 69% (mean exercising time of 33min/week). Twenty-four percent of the control group and 20% of the Exergame group fell over the trial period. The change in fall rates significantly favoured the intervention (incident rate ratio 0.31 (95% CI 0.16 to 0.62, p=0.001)). The point estimate of the incremental cost-effectiveness ratio (ICER) was 15,209.80 per quality-adjusted life year (QALY). Using 10,000 bootstrap replications, at the lower bound of the NICE threshold of 20,000 per QALY, there was a 61% probability of Exergames being cost-effective, rising to 73% at the upper bound of 30,000 pound per QALY.ConclusionsExergames, as delivered in this trial, improve balance, pain and fear of falling and are a cost-effective fall prevention strategy in assisted living facilities for people aged 55years or older.
# '''
#     }
#     paper_info_2 = {
#         'title': 'Costs of an Off-the-Shelf Exergame Intervention in Patients with Heart Failure',
#         'journal': 'Games Health',
#         'abstract': '''Objectives: Exergaming is promising for patients with heart failure who are less inclined to start or maintain exercise programs involving traditional modes of physical activity. Although no effect on exercise capacity was found for an off-the-shelf exergame, it is important to gain insights into aspects related to costs to develop such interventions further. Materials and Methods: In a randomized controlled trial, the Heart Failure Wii study (HF-Wii study), the intervention group (exergame group) received an introduction to the exergame, the exergame was installed at home and help was offered when needed for 3 months. Patients received telephone follow-ups at 2, 4, 8, and 12 weeks after the installation. The control group (motivational support group) received activity advice and telephone follow-ups at 2, 4, 8, and 12 weeks. We collected data on hospital use and costs, costs of the exergame intervention, patient time-related costs, and willingness to pay. Results: No significant differences were found between the exergame group (n = 300) versus the motivational support group (n = 305) in hospital use or costs (1-year number of hospitalizations: P = 0.60, costs: P = 0.73). The cost of the intervention was 190 Euros, and the patient time-related costs were 98 Euros. Of the total estimated costs for the intervention, 287 Euros, patients were willing to pay, on average, 58%. Conclusion: This study shows that the costs of an intervention using an off-the-shelve exergame are relatively low and that the patients were willing to pay for more than half of the intervention costs. The trial is registered in ClinicalTrials.gov (NCT01785121).
# '''
#     }
    yes = 0
    uncertain = 0
    no = 0
    in_file = './wos-1546/wos-1546.txt'
    out_file = './wos-1546/wos-1546-'

    # 排除处理过的
    processed_titles = set()
    tmp = ['YES.txt', 'UNCERTAIN.txt', 'NO.txt']
    for t in tmp:
        if not os.path.exists(out_file + t):
            continue
        with open(out_file + t, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        for line in lines:
            if '[Title]' in line:
                title = line[len('[Title]    '):].strip()
                processed_titles.add(title)
                if t == 'YES.txt':
                    yes += 1
                elif t == 'UNCERTAIN.txt':
                    uncertain += 1
                else:
                    no += 1

    # 按行读取文件内容
    with open(in_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    left, right = 0, 0
    max_line = len(lines)
    index = 0
    while left < max_line - 1:
        print('[Index]:', index)
        index += 1
        while left < max_line - 1 and len(lines[left].strip()) == 0:
            left += 1
        right = left + 1
        while right < max_line and len(lines[right].strip()) > 0:
            right += 1
        line_1 = lines[left].strip()

        idx_1 = line_1.find('"')
        idx_2 = line_1.find('"', idx_1 + 1)

        if idx_1 == -1 and idx_2 == -1:
            idx_1 = line_1.find(').') + 2
            idx_2 = line_1.find('.', idx_1 + 1)

        author = line_1[:idx_1]
        title = line_1[idx_1 + 1:idx_2]

        if title in processed_titles:
            print('[Processed]:', title)
            continue

        journal = line_1[idx_2 + 2:].strip()
        abstract = lines[left + 1].strip()
        left = right

        paper_info = {
            'title': title,
            'journal': journal,
            'abstract': abstract
        }

        answer, response = question_answer(paper_info)
        if 'YES' in answer:
            yes += 1
        elif 'NO' in answer:
            no += 1
        else:
            uncertain += 1
        # 将结果写入文件
        out_file_name = out_file + answer + '.txt'
        with open(out_file_name, 'a', encoding='utf-8') as f:
            f.write('[Author]   ' + author + '\n')
            f.write('[Title]    ' + title + '\n')
            f.write('[Journal]  ' + journal + '\n')
            f.write('[Abstract] ' + abstract + '\n')
            f.write('[Answer]   ' + answer + '\n')
            f.write('[Response] ' + response.output.text.replace('\n\n', '. ') + '\n\n')

    print('[Total]:', index, '\n[YES]:', yes, '\n[NO]:', no, '\n[UNCERTAIN]:', uncertain)

    # question_answer(paper_info)


if __name__ == '__main__':
    main()