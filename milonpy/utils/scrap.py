'''
Created on Mar 12, 2013

@author: nickmilon
'''
#@note in future we will use scrapy instead 
from mechanize import Browser
from BeautifulSoup import BeautifulSoup


def str_clear(obj):
    if isinstance(obj, basestring):
        return obj.replace('\n','').replace('\t','').replace('\r','').strip()
    else:
        return obj
 

def TableRowsToList(table):
    if isinstance(table, basestring):table= BeautifulSoup(table)
    def scrapRowVals(row,cell='td'):
        return ["".join(cell.findAll(text=True)).strip()  for cell in row.findAll(cell)] 
    trs= table.findAll("tr")
    th = [scrapRowVals(row,'th') for row in trs if row.first().name=='th'] 
    tr = [scrapRowVals(row) for row in trs if  row.first().name=='td']  
    return th,tr
def TableRowsToListOld(table, clearNPC=False):
    if isinstance(table, basestring):table= BeautifulSoup(table)
    def scrapRowVals(row):
        rt= [cell for cell in row.findAll("td")] 
        rt= [cell.findAll(text=True) for cell in rt] 
        if clearNPC:rt=[str_clear(it) for it in rt] 
        return rt       
    return [scrapRowVals(row) for row in table.findAll("tr")] 

def lst_clear(lst):
    for obj in lst: 
        if isinstance(obj, list):return lst_clear(obj)
        else: return obj.replace('\n','').replace('\t','').replace('\r','').strip()

def getTwtLimits():
    url="https://dev.twitter.com/docs/rate-limiting/1.1/limits" 
    mech = Browser() 
    page = mech.open(url)
    html = page.read() 
    soup = BeautifulSoup(html) 
    table=soup.find("table",attrs={'class':'views-table cols-4'})
    headers,rows=TableRowsToList(table)
    return headers,rows