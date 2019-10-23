import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


URL=['https://arxiv.org/list/cs.AI/pastweek?show=64','https://arxiv.org/list/cs.LG/pastweek?show=279']#url集合

for i in range(len(URL)):#遍历循环
    RESPONSE=requests.get(URL[i])
    SOUP=BeautifulSoup(RESPONSE.text, 'html.parser')
#解析网页成bs4.BeautifulSoup类型,将html代码全部读取出来

    field=SOUP.select('h1')#选择包含‘h1'的所有，返回一个list，里面每一个元素是bs4.element.Tag
    FIELD=[]
    FIELD.append(field[1].get_text())#bs4.element.Tag的功能：get_text()获取文字内容，不要标签
    
    LINKS= SOUP.select('span[class="list-identifier"]')
    len(LINKS)
    #由于href中链接用了缩写，省略了域，所以我们用两个字符拼接的方式，还原地址
    links=[]
    head='https://arxiv.org'
    for m in range(len(LINKS)):
        link=LINKS[m].find_all('a')[0]['href']#Tag的find_all功能：找到a标签，对第一个元素（包含链接）提取href值
    #a[0].get_text()获取，<a>和</a>之间的文本
    #a[0]['href']#获取a内href值
        links.append(head+link)
    
    #urls=['https://arxiv.org/abs/1711.02352','https://arxiv.org/abs/1711.02298']
    
    #file = open('C:/Users/Mr.Handsome/Desktop/2017 CCF/code/yancheng_weather.csv','w')
    
    title_=[]
    receive_date_=[]
    abstract_=[]
    for url in links:
        response = requests.get(url) #获取url
    
        soup = BeautifulSoup(response.text, 'html.parser')#获取uml页面
    
        #-----------------------爬取你想要的东西--------------------------
        #标题
        title = soup.select('h1[class="title mathjax"]')#选择标题所在标签
        type(title[0])#soup的tag
        title_.append(title[0].get_text().split('\n'))#get_text()获取元素值（去掉标签），split分隔各元素成列表，再选择自己需要的即可
    
        #日期
        receive_date= soup.select('div[class="dateline"]')
        receive_date_.append(receive_date[0].get_text().replace('\n','').strip())
    
        #摘要
        abstract = soup.select('blockquote[class="abstract mathjax"]')
        element=abstract[0].get_text().split('\n')#分割
        abstract_.append("".join(element))#重组
        #二级领域
        FIELD.append(FIELD[0])
    del FIELD[-1]#由于开始初始化有一个值，为保障长度相等，所以要去掉一个
    #print(title_)
    #print(receive_date_)
    #print(abstract_)
    
    #通过dataframe转成文件
    data={'Title':title_,'Field':FIELD,'Receive_date':receive_date_,'Abstract':abstract_,'Link':links}
    df=DataFrame(data,columns=['Title','Field','Receive_date','Abstract','Link'])
    df.to_csv('./Outputs/%d.csv'%i,index=False)