titles = """Alhasan-2021-Application of Interactive Video
Babadi-2021-Effects of virtual reality versus
Benitez-Lugo-2022-Effectiveness of feedback-based technology on physical and cognitive abilities in the elderly
Campo-Prieto-2022-Immersive Virtual Reality as
Fidan-2024-Effects of group-based virtual real
Fidan-2024-Effects of group-based virtual real
Ghous-et-al-2024-comparison-of-Nonimmersive-virtual-reality
Hsieh-2014-Virtual reality system based on Kin
Htut-2018-Effects of physical, virtual reality
Kanyilmaz-2022-Effectiveness of conventional v
Kartikasari-2023-The effect of adding exergame
Khushnood-2021-Role Wii Fit exer-games in impr
Effects of WiiActive exercises on fear of falling and functional outcomes in community-dwelling older adults: A randomised control trial
Lee-2023-Home-Based Exergame Program to Improv
Phirom-2020-Beneficial Effects of Interactive
Phu-2019-Balance training using virtual realit
Phu-2019-Balance training using virtual realit
Schwenk-2014-Interactive balance training inte
The effectiveness and cost-effectiveness of strength and balance Exergames to reduce falls risk for people aged 55 years and older in UK assisted living facilities: a multi-centre, cluster randomised controlled trial
Yang-2020-Effects of Kinect exergames on balan
Comparison of the effects of virtual reality-based balance exercises and conventional exercises on balance and fall risk in older adults living in nursing homes in Turkey
Zahedian-Nasab-2021-Effect of virtual reality
Zak-2022-Physiotherapy Programmes Aided by VR
Zak-2022-Physiotherapy Programmes Aided by VR
Zak-2022-Physiotherapy Programmes Aided by VR
虚拟情景互动训练对老年人跌倒风险的干预效果研究
虚拟现实训练对养老院老年人跌倒相关危险因素的影响"""
titles = titles.split("\n")
res_dict = {t:[] for t in titles}

file_path = 'tug.md'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

"""
* 随机序列的产生：低风险偏倚
* 分配隐藏：不清楚
* 实施偏倚：高风险偏倚
* 测量偏倚：低风险偏倚
* 随访偏倚：低风险偏倚
* 报告偏倚：低风险偏倚
* 其他偏倚：低风险偏倚
"""
metrics = ['随机序列的产生', '分配隐藏', '实施偏倚', '测量偏倚', '随访偏倚', '报告偏倚', '其他偏倚']
metrics_res = ['低风险偏倚', '不清楚', '高风险偏倚']

for i in range(len(lines)):
    line = lines[i].strip()
    if line in titles:
        res = {}
        for j in range(i+1, len(lines)):
            for metric in metrics:
                if '{}：'.format(metric) in lines[j]:
                    res[metric] = lines[j][lines[j].find('：') + 1:].strip()
            if len(res) == len(metrics):
                break
        res_dict[line] = list(res.values())

for k, v in res_dict.items():
    print(k, ':', ','.join(v))
