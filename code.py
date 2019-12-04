# tutorial https://github.com/ZihaoZhao/Arxiv_daily/blob/master/dailyarxiv.py
import requests
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
import pymysql
from collections import Counter
import os
import random


def get_one_page(url):
    response = requests.get(url)
    print(response.status_code)
    while response.status_code == 403:
        time.sleep(500 + random.uniform(0, 500))
        response = requests.get(url)
        print(response.status_code)
    print(response.status_code)
    if response.status_code == 200:
        return response.text

    return None


def main():
    url = 'https://arxiv.org/list/cs.AI/pastweek?skip=0&show=49'
    html = get_one_page(url)
    soup = BeautifulSoup(html, features='html.parser')
    content = soup.dl
    date = soup.find('h3')
    list_ids = content.find_all('a', title = 'Abstract')
    list_title = content.find_all('div', class_ = 'list-title mathjax')
    list_authors = content.find_all('div', class_ = 'list-authors')
    list_subjects = content.find_all('div', class_ = 'list-subjects')
    list_subject_split = []
    for subjects in list_subjects:
        subjects = subjects.text.split(': ', maxsplit=1)[1]
        subjects = subjects.replace('\n\n', '')
        subjects = subjects.replace('\n', '')
        subject_split = subjects.split('; ')
        list_subject_split.append(subject_split)

    items = []
    for i, paper in enumerate(zip(list_ids, list_title, list_authors, list_subjects, list_subject_split)):
        items.append([paper[0].text, paper[1].text, paper[2].text, paper[3].text, paper[4]])
    name = ['id', 'title', 'authors', 'subjects', 'subject_split']
    paper = pd.DataFrame(columns=name,data=items)
    paper.to_csv('d:/Job/Extractor/arxiv/'+time.strftime("%Y-%m-%d")+'_'+str(len(items))+'.csv')


    '''subject split'''
    subject_all = []
    for subject_split in list_subject_split:
        for subject in subject_split:
            subject_all.append(subject)
    subject_cnt = Counter(subject_all)
    #print(subject_cnt)
    subject_items = []
    for subject_name, times in subject_cnt.items():
        subject_items.append([subject_name, times])
    subject_items = sorted(subject_items, key=lambda subject_items: subject_items[1], reverse=True)
    name = ['name', 'times']
    subject_file = pd.DataFrame(columns=name,data=subject_items)
    #subject_file = pd.DataFrame.from_dict(subject_cnt, orient='index')
    subject_file.to_csv('d:/Job/Extractor/'+time.strftime("%Y-%m-%d")+'_'+str(len(items))+'.csv')
    #subject_file.to_html('subject_file.html')


    list_subject_split = []
    if not os.path.exists('d:/Job/Extractor/arxiv/selected/'+time.strftime("%Y-%m-%d")):
        os.makedirs('d:/Job/Extractor/arxiv/selected/'+time.strftime("%Y-%m-%d"))
    for paper_id, paper_title in zip(paper['id'], paper['title']):
        paper_id = paper_id.split(':', maxsplit=1)[1]
        paper_title = paper_title.split(':', maxsplit=1)[1]
        r = requests.get('https://arxiv.org/pdf/' + paper_id)
        while r.status_code == 403:
            time.sleep(500 + random.uniform(0, 500))
            r = requests.get('https://arxiv.org/pdf/' + paper_id)
        paper_id = paper_id.replace(".", "_")
        pdfname = paper_title.replace("/", "_")   #pdf名中不能出现/和：
        pdfname = pdfname.replace("?", "_")
        pdfname = pdfname.replace("\"", "_")
        pdfname = pdfname.replace("*","_")
        pdfname = pdfname.replace(":","_")
        pdfname = pdfname.replace("\n","")
        pdfname = pdfname.replace("\r","")
        pdfname = pdfname.replace("$","")
        pdfname = pdfname.replace("\\", "")
        pdfname = pdfname.replace("{", "")
        pdfname = pdfname.replace("}", "")
        print('d:/Job/Extractor/arxiv/selected/' + time.strftime("%Y-%m-%d") + '/%s %s.pdf' % (paper_id, paper_title))
        with open('d:/Job/Extractor/arxiv/selected/'+time.strftime("%Y-%m-%d")+'/%s %s.pdf'%(paper_id,pdfname), "wb") as code:
            code.write(r.content)



if __name__ == '__main__':
    main()
    time.sleep(10)