import sqlite3

ess=sqlite3.connect("ess.db")
#cursor=ess.execute("select * from ALL_ESS where PROPOSAL_DEPARTMENT='MEZ910'")
#for row in cursor:
#	print(row)

cursor=ess.execute("select PROPOSAL_DATE from ALL_ESS")
for row in cursor:
	print(row)