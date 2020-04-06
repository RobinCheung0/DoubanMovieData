import requests
from bs4 import BeautifulSoup
import re

internetHeaders = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69'
}

def getURL(url):
    try:
        requestPage = requests.get(url,headers=internetHeaders)
        if requestPage.status_code == 200:
            return requestPage.text
        return None
    except requests.exceptions.RequestException:
        return None

def analyseHTML(url):
    infos = []
    rawHTML = getURL(url)
    bs = BeautifulSoup(rawHTML,'lxml')
    main = bs.find('ol',{'class':'grid_view'})
    
    listTitles = []
    listRanks = []
    listRatingNum = []
    listDiscriptions = []
    listDetail = []

    titles = main.find_all('span',{'class':'title'})
    for title in titles:
        if title.text[1] != '/':
            listTitles.append(title.text)
    ranks = main.find_all('em')
    for rank in ranks:
        listRanks.append(rank.text)

    ratingNum = main.find_all('span',{'class':'rating_num'})
    for num in ratingNum:
        listRatingNum.append(num.text)
    
    discriptions = main.find_all('p',{'class':''})
    for discription in discriptions:
        listDiscriptions.append(re.sub('\s','',discription.text))

    for unsplitDiscription in listDiscriptions:
        item = re.findall('导演:(.*?)主演:(.*?)...(\d{4})/(.*?)/(.*?)$',unsplitDiscription)
        if len(item) == 0:
            item = [['N/A','N/A','N/A','N/A','N/A']]
        else:
            for i in item:
                i = list(i)
                item[0] = i

        if item[0][4] == 'N/A' or len(item[0][4]) == 2:
            item[0][4] = item[0][4]
        elif len(item[0][4]) == 4:
            fixedStr = item[0][4][0:2] + '/' +item[0][4][2:]
            item[0][4] = fixedStr
        elif len(item[0][4]) == 6:
            fixedStr = item[0][4][0:2] + '/' +item[0][4][2:4] + '/' + item[0][4][4:]
            item[0][4] = fixedStr
        elif len(item[0][4]) == 8:
            fixedStr = item[0][4][0:2] + '/' +item[0][4][2:4] + '/' + item[0][4][4:6] + '/' + item[0][4][6:]
            item[0][4] = fixedStr
        elif len(item[0][4]) == 10:
            fixedStr = item[0][4][0:2] + '/' +item[0][4][2:4] + '/' + item[0][4][4:6] + '/' + item[0][4][6:8] + '/' + item[0][4][8:]
            item[0][4] = fixedStr
        listDetail.append(item[0])


    for i in range(25):
        info = {'影名':listTitles[i],
                '排名':listRanks[i],
                '得分':listRatingNum[i],
                '主演':listDetail[i][0],
                '导演':listDetail[i][1],
                '时间':listDetail[i][2],
                '地点':listDetail[i][3],
                '分类':listDetail[i][4]}
        infos.append(info)
    return infos