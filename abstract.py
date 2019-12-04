import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
URL=['https://arxiv.org/list/cs.LG/pastweek?show=10','https://arxiv.org/list/cs.AI/pastweek?show=10']#url集合
startdate = '2019-12-01'
enddate = '2019-12-03'
kbkeyword = 'semantic|representation|knowledge'
cvkeyword = 'image|graph'
dff = pd.DataFrame()

for i in range(len(URL)):
    RESPONSE=requests.get(URL[i])
    SOUP=BeautifulSoup(RESPONSE.text, 'html.parser')
#解析网页成bs4.BeautifulSoup类型,将html代码全部读取出来

    LINKS= SOUP.select('span[class="list-identifier"]')
    #由于href中链接用了缩写，省略了域，所以我们用两个字符拼接的方式，还原地址
    links=[]
    head='https://arxiv.org'
    for m in range(len(LINKS)):
        link=LINKS[m].find_all('a')[0]['href']#Tag的find_all功能：找到a标签，对第一个元素（包含链接）提取href值
        links.append(head+link)

    title_=[]
    receive_date_=[]
    abstract_=[]
    for url in links:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')#获取uml页面
    
        #标题
        title = soup.select('h1[class="title mathjax"]')#选择标题所在标签
        title_.append(title[0].get_text().lstrip('Title:'))#get_text()获取元素值（去掉标签），split分隔各元素成列表，再选择自己需要的即可

    
        #日期
        receive_date= soup.select('div[class="dateline"]')
        receive_date_.append(receive_date[0].get_text().replace('\n','').strip())
    
        #摘要
        abstract = soup.select('blockquote[class="abstract mathjax"]')
        element=abstract[0].get_text().split('\n')#分割
        abstract_.append("".join(element).lstrip('Abstract:  '))

    #通过dataframe转成文件
    data={'Title':title_,'Receive_date':receive_date_,'Abstract':abstract_,'Link':links}
    df=pd.DataFrame(data,columns=['Title','Receive_date','Abstract','Link'])
    # Filter date
    df['Receive_date'] = df['Receive_date'].apply(
        lambda x: x.replace('(Submitted on ', '').split('2019', 1)[0] + '2019')
    df = df[~df['Receive_date'].str.contains('revised|2018')]
    df['Receive_date'] = df['Receive_date'].apply(lambda x: datetime.datetime.strptime(x, '%d %b %Y'))
    df = df[(df['Receive_date'] >= startdate) & (df['Receive_date'] <= enddate)]
    dff = dff.append(df)

def tocsv(dff,keyword,field):
    dff = dff[dff['Abstract'].str.contains(keyword[i], flags=re.IGNORECASE, regex=True)]
    dff.to_csv('./Outputs/'+field+'.csv', index=False)

tocsv(dff,kbkeyword,'knowledge_based')