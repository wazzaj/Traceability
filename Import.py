import pyral
import requests
from pyral import Rally, RallyRESTAPIError, rallyWorkset
import sys, os

####################################################################################################

errout = sys.stderr.write

####################################################################################################

def addDependenciesToRally(rally, story, post):
    predecessor = getItem(rally, story)
    print "P: " + predecessor.FormattedID
    postStory = getItem(rally, post)
    print "S: " + postStory.FormattedID

    newList = list()

    for item in postStory.Predecessors:
        print item.FormattedID + " " + item.Name
        assert isinstance(item.ref, object)
        newList.append({"_ref" : str(item.ref)})

    newList.append({"_ref" : str(predecessor.ref)})

    info = dict(FormattedID=postStory.FormattedID, Predecessors=newList)
    print info
    return()

    print "Issuing POST request..."

    try:
        updatedStory = rally.post('UserStory', info)
    except RallyRESTAPIError, details:
        print 'ERROR: ' + str(details)
        sys.stderr.write('ERROR: %s \n' % details)
        sys.exit(2)

    print "Item Updated"
    print "FormattedID: %s Predecessor: %s" % (updatedStory.FormattedID, predecessor.FormattedID)

    return ()

def getItem(rally, id):
    # type: (object, object) -> object
    print "Processing GET request..."
    response = rally.get('PortfolioItem', fetch="_ref,ObjectID,FormattedID,Name,Predecessors", query="FormattedID = %s" % id)

    if not response.errors:
        for story in response:
            continue
    else:
        print response.errors
        sys.exit(9)

    return (story)

def getDependencies(rally):
    import pyexcel as pe
    import pyexcel.ext.xlsx

    records = pe.get_records(file_name="RallyUpload-DependenciestoCA-v2.xlsx")
    for record in records:
        print record['RALLY ID'] + " - " + record['Successor']
        addDependenciesToRally(rally, record['RALLY ID'], record['Successor'])

    return ()


def setupRally():
    options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
    args = [arg for arg in sys.argv[1:] if arg not in options]
    server, user, password, apikey, workspace, project = rallyWorkset(options)
    if apikey:
        print("S: " + str(server) + " A: " + apikey + " W: " + workspace + " P: " + project)
        rally = Rally(server, apikey=apikey, workspace=workspace, project=project)
    else:
        print("S: " + str(server) + " U: " + user + " P: " + password + " W: " + workspace + " P: " + project)
        rally = Rally(server, user, password, workspace=workspace, project=project)
    rally.enableLogging('mypyral.log')

    return (rally)


myRally = setupRally()
getDependencies(myRally)

exit()