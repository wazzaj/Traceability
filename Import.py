import pyral
import requests
from pyral import Rally, RallyRESTAPIError, rallyWorkset
import sys, os
from json import JSONEncoder

####################################################################################################

errout = sys.stderr.write

####################################################################################################

def addDependenciesToRally(rally, pre, post):
    postStory = getStory(rally, pre)
    print "S: " + postStory.FormattedID
    predecessor = getStory(rally, post)
    print "P: " + predecessor.FormattedID

    postStory.Predecessors.append(predecessor)

    print len(postStory.Predecessors)

    for item in postStory.Predecessors:
        print item.FormattedID + " " + item.Name

    info = {
        "FormattedID": postStory.FormattedID,
        "Name": "Updated from Import Script 2",
        "Predecessors": postStory.Predecessors
    }

    try:
        updatedStory = rally.post('UserStory', info)
    except RallyRESTAPIError, details:
        print 'ERROR: ' + details
        sys.stderr.write('ERROR: %s \n' % details)
        sys.exit(2)

    print "Story Updated"
    print "FormattedID: %s Predecessor: %s" % (updatedStory.FormattedID, predecessor.FormattedID)

    return ()


def getStory(rally, storyID):
    # type: (object, object) -> object
    response = rally.get('UserStory', fetch=True, query="FormattedID = %s" % storyID)

    if not response.errors:
        for story in response:
            continue

    return (story)


def getDependencies(rally):
    import pyexcel as pe
    import pyexcel.ext.xlsx

    records = pe.get_records(file_name="Test.xlsx")
    for record in records:
        addDependenciesToRally(rally, record['Pre'], record['Post'])

    return ()


def setupRally():
    options = [arg for arg in sys.argv[1:] if arg.startswith('--')]
    args = [arg for arg in sys.argv[1:] if arg not in options]
    server, user, password, apikey, workspace, project = rallyWorkset(options)
    print("S: " + str(server) + " U: " + user + " P: " + password + " A: " + apikey + " W: " + workspace)
    rally = Rally(server, user, password, workspace=workspace, project=project)
    rally.enableLogging('mypyral.log')

    return (rally)


myRally = setupRally()
getDependencies(myRally)

exit()
