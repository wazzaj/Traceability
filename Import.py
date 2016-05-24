import pyral
import requests
from pyral import Rally, rallyWorkset
import sys

username = 'dan@acme.com'
password = 'Motivate!'
host = 'https://demo-apac.rallydev.com/slm/webservice/v2.0/'

def setUpBasicAuth(r):

    return()

def addDependenciesToRally(rally, pre, Post):
    response = rally.get('UserStory', fetch=True, query="FormattedID = %s" % pre)

    print response.resultCount
#    if not response.errors:
    for story in response:
        print story
        print("Match on " + story.FormattedID)
        print story.details()
#        else:
#            print("Errors" + str(response.errors))

    return()

def getDependencies(rally):
    import pyexcel as pe
    import pyexcel.ext.xlsx

    records = pe.get_records(file_name="Test.xlsx")
    for record in records:
        print(record['Pre'],record['Post'])
        addDependenciesToRally(rally,record['Pre'],record['Post'])
          
    return()


def setupRally():
    options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
    args = [arg for arg in sys.argv[1:] if arg not in options]
    server, user, password, apikey, workspace, project = rallyWorkset(options)
    print("S: " + str(server) + " U: " + user + " P: " + password + " A: " + apikey + " W: " + workspace)
    rally = Rally(server, user, password, workspace=workspace, project=project)
    rally.enableLogging('mypyral.log')

    return(rally)

myRally = setupRally()
getDependencies(myRally)

exit()
