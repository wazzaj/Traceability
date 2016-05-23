import urllib2
import json
import base64
import pyral
#import requests

username = 'xxx@xxx.com'
password = 'xxxxxxxx'
host = 'https://demo-apac.rallydev.com/slm/webservice/v2.0/'

def setUpBasicAuth(r):
    base64string = base64.b64encode(bytes('%s:%s' % (username, password),'ascii'))
    r.add_header("Authorization", "Basic %s" % base64string.decode('utf-8'))
    return()

def addDependenciesToRally(Pre, Post):
    request = urllib.request.Request(host +
            'hierarchicalrequirement?query=(FormattedID%20%3D%20' + Pre + ')' +
            '&fetch=true')

    print(host +
            'hierarchicalrequirement?query=(FormattedID%20%3D%20' + Pre + ')' +
            '&fetch=true')
    
    setUpBasicAuth(request)
    result = urllib.request.urlopen(request).read()

    jsonResponse = json.loads(result.decode('utf-8'))
#    print(json.dumps(jsonResponse))

    if jsonResponse["QueryResult"]["TotalResultCount"] > 0:
        print('Result ' + str(jsonResponse["QueryResult"]["TotalResultCount"]))
        
    return()

def getDependencies(host):
    import pyexcel as pe
    import pyexcel.ext.xlsx

    records = pe.get_records(file_name="Test.xlsx")
    for record in records:
        print(record['Pre'],record['Post'])
        addDependenciesToRally(record['Pre'],record['Post'])
          
    return()                              
          
getDependencies(host)

exit()
