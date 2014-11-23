import os
from infraApp import build_app
from flask.ext.script import Manager
from infraApp import db
from infraApp.models import User,scrapedProjects
from flask.ext.migrate import Migrate, MigrateCommand

app = build_app(os.getenv('FLASK_CONFIG') or 'default')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
@manager.command
def adduser(username, admin=True):
	'''Register a New Admin'''
	from getpass import getpass

	password = getpass()
	password2 = getpass(prompt='Confirm')
	if password != password2:
		import sys
		sys.exit('Error: passwords do not match')
	db.create_all()
	user = User(username=username, password=password, is_admin=admin)
	db.session.add(user)
	db.session.commit()
	print "Sucessfully Created Admin"

@manager.command
def importDPWH(directory):
	'''Import DPWH Data'''
	f = open("sep/"+directory+".txt", "r")

	lines = f.readlines()
	f.close()

	for data in xrange(len(lines)):
		newData = lines[data].split('\t')
		prjID = newData[0]
		title = newData[1]
		contractor = newData[2]
		impOffice = newData[3]
		srcFunds = newData[4]
		cost = newData[5]
		status = newData[6]
		startDate = newData[7]
		origComp = newData[8]
		actComp = newData[9]
		db.create_all()
		prj = scrapedProjects(prjID=prjID,title=title, contractor=contractor, impOffice=impOffice,
				srcFunds=srcFunds, cost=cost, status=status, startDate=startDate, origComp=origComp,
				actComp=actComp, regions=directory
			)
		db.session.add(prj)
		db.session.commit()

	print "finished adding region " + directory



if __name__ == '__main__':
    manager.run()
