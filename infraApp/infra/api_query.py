import urllib
import json

AWARD = "539525df-fc9a-4adf-b33d-04747e95f120"
BIDDERS_LIST = "6427affb-e841-45b8-b0dc-ed267498724a"
ORGANIZATION = "ec10e1c4-4eb3-4f29-97fe-f09ea950cdf1"
BID_LINE_ITEM = "daa80cd8-da5d-4b9d-bb6d-217a360ff7c1"
BID_INFORMATION = "baccd784-45a2-4c0c-82a6-61694cd68c9d"
PROJECT_LOCATION = "116b0812-23b4-4a92-afcc-1030a0433108"
ORGANIZATION_BUSINESS_CATEGORY = "58ea40bf-15e9-4c38-adef-fd93455d8c7e"
# REC_AWARD = 164391
# REC_BIDDERS_LIST = 186389
# REC_ORGANIZATION = 98938
# REC_BID_LINE_ITEM = 215770
# REC_BID_INFORMATION = 165988
# REC_PROJECT_LOCATION = 258349
# REC_ORGANIZATION_BUSINESS_CATEGORY = 72806

URL = "http://philgeps.cloudapp.net:5000/api/action/datastore_search?resource_id="


def url_to_json(url):
	f = urllib.urlopen(url)
	return json.load(f)

# Returns total number and bid price of awarded projects by an organization
def get_awards_total_of_org(orgid): #org_id=awardee_id
	total = 0
	awards = 0
	url = URL+AWARD+'&filters={"awardee_id":"'+str(orgid)+'"}'
	j = url_to_json(url)
	for x in j['result']['records']:
		total+=float(x['contract_amt'])
		awards+=1
	return awards, total

# Returns number of previous bids by an organization
def get_number_of_previous_bids_of_org(orgid):
	total = 0
	url = URL+BIDDERS_LIST+'&filters={"org_id":"'+str(orgid)+'"}'
	j = url_to_json(url)
	for x in j['result']['records']:
		total+=1
	return total

# Returns bid information (dict file)
def get_bidinfo_from_refid(refid):
	url = URL+BID_INFORMATION+'&filters={"ref_id":"'+str(refid)+'"}'
	j = url_to_json(url)
	return j['result']['records']

# Returns information about an organization (dict file)
def get_orginfo_from_orgid(orgid):
	url = URL+ORGANIZATION+'&filters={"org_id":"'+str(orgid)+'"}'
	j = url_to_json(url)
	return j['result']['records']
def get_orgcategory(orgid):
	url = URL+ORGANIZATION_BUSINESS_CATEGORY+'&filters={"orgid":"'+str(orgid)+'"}'
	j = url_to_json(url)
	return j['result']['records']

# Returns bidders for each award/project (QUESTION: Line Item ba tayo or Project as a whole yung number of bidders)
def get_bidderslist_from_awardid(awardid):
	total = 0
	url = URL+BIDDERS_LIST+'&filters={"award_id":"'+str(awardid)+'"}'
	j = url_to_json(url)
	for x in j['result']['records']:
		total+=1
	return total, j['result']['records']


# Returns json file of projects within a certain province
def get_project_with_location_json(province):
	url = URL+PROJECT_LOCATION+'&filters={"location":"'+province+'"}&limit=100&sort="modified_date"'
	j = url_to_json(url)
	# f = urllib.urlopen(url)
	# j = json.load(f)
	return j['result']['records']

# Returns list of bid information (json looking format) for projects within a certain province
def get_list_of_projects_per_location(province):
	proj = list()
	proj_info = list()
	pl = get_project_with_location_json(province)

	for p in pl:
		proj.append(int(p['refid']))

	for refid in proj:
		url = URL+BID_INFORMATION+'&filters={"ref_id":"'+str(refid)+'"}'
		j = url_to_json(url)
		proj_info.append(j['result']['records'])

	return proj_info

# Return list of suppliers for a certain province
def get_list_of_suppliers_per_location(province):
	url = URL+ORGANIZATION+'&filters={"member_type":"Supplier", "province":"'+province+'"}&limit=100'
	j = url_to_json(url)
	return j['result']['records']

def get_list_of_suppliers():
	url = URL+ORGANIZATION+'&filters={"member_type":"Supplier"}&limit=100'
	j = url_to_json(url)
	return j['result']['records']

# Return list of buyers for a certain province
def get_list_of_buyers():
	url = URL+ORGANIZATION+'&filters={"member_type":"Buyer"}&limit=100'
	j = url_to_json(url)
	return j['result']['records']

def get_list_of_buyers_per_location(province):
	url = URL+ORGANIZATION+'&filters={"member_type":"Buyer", "province":"'+province+'"}&limit=100'
	j = url_to_json(url)
	return j['result']['records']


def suppliers_stats(province):
	frn = 0
	loc = 0
	sup = get_list_of_suppliers_per_location(province)
	for s in sup:
		if s['is_org_foreign']==1:
			frn+=1
		else:
			loc+=1
	return loc, frn

# get_list_of_projects_per_location("Metro Manila")
#print get_list_of_suppliers()


# print get_orginfo_from_orgid(11951)
# print get_bidinfo_from_refid(889944)
# print get_awards_total_of_org(1015)
# print get_number_of_previous_bids_of_org(1015)
# print get_bidderslist_from_awardid(48086)
