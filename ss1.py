import cfscrape
import bs4
from prettytable import PrettyTable
from ping3 import ping
import operator
import numpy
import base64

def ping_test(ip) -> int:
    delay = []
    delay.append(ping(ip,unit="ms"))
    delay.append(ping(ip,unit="ms"))
    delay.append(ping(ip,unit="ms"))
    delay = [x for x in delay if x != None]
    if len(delay) ==0:
        return 10000
    else:
        return int(numpy.mean(delay))

scraper = cfscrape.create_scraper()
soup = bs4.BeautifulSoup(scraper.get("https://www.youneed.win/free-ss").content)
content =  soup.tbody.get_text().strip("\n\n")
sslist = content.split("\n\n")

tableList = []
for text in sslist:
    text = text.strip("\n")
    tlist = text.split("\n")
    ssconfig = tlist[4]+":"+tlist[2]+"@"+tlist[0]+":"+tlist[1]
    ssurl = "ss://"+base64.b64encode(ssconfig.encode("utf8")).decode()
    tlist.append(ssurl)
    del tlist[2:4]
    tlist.insert(0, ping_test(tlist[0]))
    tableList.append(tlist)

tableList.sort(key=operator.itemgetter(0))

table = PrettyTable(["seq","TimeDelay","","ip","port","update time","country","sslink"])
for i in range(0,len(tableList)-1):
    tableList[i][0] = str(tableList[i][0]) + " ms"
    tableList[i].insert(0,i)
    table.add_row(tableList[i])
print(table)

