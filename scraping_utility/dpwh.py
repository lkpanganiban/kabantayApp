import requests
from bs4 import BeautifulSoup
import sys

def scrapME(site):
	url = requests.get("http://www.dpwh.gov.ph/infrastructure/pms/"+site)
	#url = open("pmo.asp.html", "r")
	data = url.text
	soup=BeautifulSoup(data)
	tab9=soup.findAll("table", {"id" : "table9"})

	records9=[]
	for i in range(0,len(tab9)):
		for row in tab9[i].findAll('tr'):
		    col = row.findAll('font')
		    for j in range(0, len(col)):
		        clean1 = col[j].contents[0]
		        clean2 = clean1.strip()
		        clean3 = clean2.encode('ascii', 'ignore')
		        records9.append(clean3)

	prjID = []
	prjName = []
	contractor =[]
	impOffice = []
	srcFunds = []

	for l in range(0,len(records9),9):
		prjID.append(records9[l])

	for l in range(2,len(records9),9):
		prjName.append(records9[l])

	for l in range(4,len(records9),9):
		contractor.append(records9[l])

	for l in range(6,len(records9),9):
		impOffice.append(records9[l])
		
	for l in range(8,len(records9),9):
		srcFunds.append(records9[l])

	#cost of the project
	cost=[]
	tab10=soup.findAll("table", {"id" : "table10"})
	for row in tab10:
		col10 = row.findAll('font')
		clean1 = col10[1].contents[0]
		clean2 = clean1.strip()
		clean3 = clean2.encode('ascii','ignore')
		cost.append(clean3)

	#status of the project
	status=[]
	tab12=soup.findAll("table", {"id" : "table12"})
	for row in tab12:
		col12 = row.findAll('font')

		clean1 = col12[1].contents[0]
		clean2 = clean1[:6].strip()
		clean3 = clean2.encode('ascii', 'ignore')
		status.append(clean3)

	records11=[]

	tab11=soup.findAll("table", {"id" : "table11"})
	for i in range(0,len(tab11)):
		for row in tab11[i].findAll('tr'):
		    col = row.findAll('font')
		    for j in range(0, len(col)):
		        clean1 = col[j].contents[0]
		        clean2 = clean1.strip()
		        clean3 = clean2.encode('ascii', 'ignore')
		        records11.append(clean3)

	startDate=[]
	origComplete=[]
	actComplete=[]

	for l in range(1,len(records11),6):
		startDate.append(records11[l])

	for l in range(3,len(records11),6):
		origComplete.append(records11[l])

	for l in range(5,len(records11),6):
		actComplete.append(records11[l])

	bigArray = []
	f=open(site+'.txt', 'w')
	for k in range(0, len(prjID)):
		f.write(
		    prjID[k]+"^"+
		    prjName[k]+"^"+
		    contractor[k]+"^"+
		    impOffice[k]+"^"+
		    srcFunds[k]+"^"+
		    cost[k]+"^"+
		    status[k]+"^"+
		    startDate[k]+"^"+
		    origComplete[k]+"^"+
		    actComplete[k]+"\n"
		    )

	f.close()

if __name__ == "__main__":
	#print(sys.argv[1])
	scrapME(str(sys.argv[1]))
	
