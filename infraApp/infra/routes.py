from flask import render_template, request, url_for, flash, redirect
from flask.ext.login import login_user, logout_user, login_required
from . import infra
from ..models import User, Projects, scrapedProjects, Comment
from .forms import AddProjectForm, CommentForm, SearchForm, ProjectEditorForm
from .. import db
from api_query import get_list_of_suppliers, get_orginfo_from_orgid, get_orgcategory, get_number_of_previous_bids_of_org, get_awards_total_of_org
import ast

@infra.route('/')
@infra.route('/index')
def index():
    dataList = Projects.query.order_by(Projects.dateStart.desc()).all()
    return render_template('infra/index.html', dataList=dataList)


@infra.route('/addData', methods=['GET', 'POST'])
@login_required
def addProject():
	form = AddProjectForm()
	dataList = Projects.query.order_by(Projects.dateStart.desc()).all()
	if form.validate_on_submit():
		proj = Projects(
				prjID=form.prjID.data,
				title=form.title.data,
				cost=form.cost.data,
				contractor=form.contractor.data,
				address=form.address.data,
				status=form.status.data,
				funding=form.funding.data,
				dateStart=form.dateStart.data,
				dateEnd=form.dateEnd.data,
				agency=form.agency.data,
				lat=form.lat.data,
				lon=form.lon.data,
				region=form.region.data 
			)
		db.session.add(proj)
		db.session.commit()	
		return render_template('infra/index.html', form=form, dataList=dataList)
	return render_template('infra/addData.html', form=form, dataList=dataList)

@infra.route('/projectList', methods=['GET', 'POST'])
def projectList():
	projList = scrapedProjects.query.limit(20)
	form = SearchForm()
	numResults=0
	if form.validate_on_submit():
		projList = scrapedProjects.query.filter(scrapedProjects.title.like('%'+form.title.data+'%'))
		numResults = projList.count()
		return render_template('infra/projects.html', projList=projList, form=form, numResults=numResults)
	return render_template('infra/projects.html', projList=projList, form=form, numResults=numResults)

@infra.route('/project/<prjID>', methods=['GET', 'POST'])
def projectProfile(prjID):
	proj = scrapedProjects.query.filter_by(prjID=prjID).all()
	form = CommentForm()
	comment = None
	if form.validate_on_submit():
		comment=Comment(body=form.body.data, 
			author_name = form.name.data,
			author_email = form.email.data,
			approved=True,
			prjID = str(prjID)
			)
		if comment:
			db.session.add(comment)
			db.session.commit()
			flash('Your comment has been posted.')
			return redirect(url_for('.projectProfile', prjID=proj[0].prjID) + '#top')
	comments = proj[0].comments.order_by(Comment.id.asc()).all()
	return render_template('infra/profile.html', 
							proj=proj[0], 
							cost=ast.literal_eval(proj[0].cost.encode('ascii','ignore')), 
							form=form, 
							comments=comments)


@infra.route('/profileEdit/<prjID>', methods=['GET', 'POST'])
def projectEditorProfile(prjID):
	proj = scrapedProjects.query.filter_by(prjID=prjID).all()
	form = ProjectEditorForm()
	if form.validate_on_submit():
		edit = scrapedProjects(
			prjID=proj.prjID,
			title=proj.title,
			cost=proj.cost,
			contractor=proj.contractor,
			status=form.status.data,
			srcFunds=proj.srcFunds,
			startDate=proj.startDate,
			origComp=proj.origComp,
			actComp=form.actComp.data,
			impOffice=proj.impOffice,
			latitude=form.lat.data,
			longitude=form.lon.data,
			regions=proj.regions
			)
		if edit:
			db.session.add(edit)
			db.session.commit()
			flash('Updated Project')
			return render_template('infra/editProj.html', 
						proj=proj[0], 
						cost=ast.literal_eval(proj[0].cost.encode('ascii','ignore')), 
						form=form
						)
	return render_template('infra/editProj.html', 
							proj=proj[0], 
							cost=ast.literal_eval(proj[0].cost.encode('ascii','ignore')), 
							form=form)


@infra.route('/contractors', methods=['GET', 'POST'])
def contractorList():
	numResults=0
	conID =[]
	conName =[]
	province =[]
	#print len(get_list_of_suppliers())
	listOfSuppliers = get_list_of_suppliers()
	for i in xrange(0, len(get_list_of_suppliers())):
		
		conID.append({"conID" :listOfSuppliers[i].get("org_id"),
			"conName":listOfSuppliers[i].get("org_name"),
			"province":listOfSuppliers[i].get("province")})
	return render_template('infra/contractors.html', conID=conID)



@infra.route('/contractor/<conID>', methods=['GET','POST'])
def contractorProfile(conID):
	conName = get_orginfo_from_orgid(conID)[0].get("org_name")
	conLoc = get_orginfo_from_orgid(conID)[0].get("province")
	category = get_orgcategory(conID)[0].get("businesscategory")
	bidded_projects = get_number_of_previous_bids_of_org(conID)
	total_amount_of_projects=get_awards_total_of_org(conID)[1]
	num_of_awarded = get_awards_total_of_org(conID)[0]
	return render_template('infra/conProfile.html', 
		conName=conName, 
		conLoc=conLoc,
		category=category,
		bidded_projects=bidded_projects,
		total_amount_of_projects = total_amount_of_projects,
		num_of_awarded=num_of_awarded 
		)