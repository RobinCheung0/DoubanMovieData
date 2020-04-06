import core
import json
import csv
import datetime

nowTime = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
totalInfo = []

for i in range(10):
    print('获取第' + str(i+1) + '页中……')
    url = 'https://movie.douban.com/top250?start=' + str(i*25) + '&filter='
    info = core.analyseHTML(url)
    for singleMovie in info:
        totalInfo.append(singleMovie)

fileName = 'data' + nowTime
csvf = open(fileName + '.csv','w',newline='',encoding='GB18030')
writer = csv.writer(csvf)
print('正在保存至' + fileName + '.csv……')
writer.writerow(totalInfo[0].keys())
for item in totalInfo:
    writer.writerow(item.values())
csvf.close()
print('保存完毕！')
print('正在保存至' + fileName + '.json……')
with open(fileName + '.json','w',encoding='GB18030') as jsonf:
    json.dump(totalInfo,jsonf,ensure_ascii=False)
print('保存完毕！')
input()
