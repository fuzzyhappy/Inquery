#import firebase_admin
#from firebase_admin import credentials
from firebase_admin import firestore

######################### Use a service account, only needs to be run once #################
#cred = credentials.Certificate('insert path name')
#firebase_admin.initialize_app(cred)
#####################################owo#####################################################

db = firestore.client()
#profRef = db.collection(u'profdata')

## Old format, not currently used
# def formatData(firstName, lastName, dept, email, researchAreas, links):
#     out = {
#     u'first_name': u''+ firstName +'',
#     u'last_name': u''+ lastName +'',
#     u'department': u''+ dept +'',
#     u'email': u''+ email +'',
#     u'area of research': researchAreas,
#     u'external links': links
#     }
#     #print(out)
#     return out


## Accepted data
# Full Name
# Education(in the form of a list)
# Research areas(in the form of a list)
# External link to website (if they have one)
# Publications: [[title, link to publication], [title2, link2], [title3]]
def uploadData(fullName, education, researchAreas, extLink, publications):
    currentRef = db.collection(u'profdata').document(u''+ fullName +'')
    
    #Converts 2D array of publications to dictionary
    pubTitles = [None]*len(publications);
    pubLinks = [None]*len(publications);
    for i in range(len(publications)):
        pubTitles[i] = publications[i][0];
        pubLinks[i] = publications[i][1];
    pubMap = dict(zip(pubTitles, pubLinks));
    #print(pubMap);
    
    info = {
    u'fullName': u''+ fullName +'',
    u'education': u''+ education +'',
    u'area_of_research': researchAreas,
    u'external links': u''+ extLink +'',
    u'publications': pubMap
    }
    #print(info);
    currentRef.set(info);

#Attempted query commands, often result in errors
# def dispByName(names):
#     results[i] = profRef.where(u'area of research', u'==', True).stream()
         
# def literalSearch(inputResearchArea):
#     results = profRef.where(u'area_of_research', u'array_contains', u''+ inputResearchArea +'').stream()
#     return results

## Misc test lines
#currentRef = db.collection(u'profdata').document(u'pete')
#currentRef.set(formatData("Purdue Pete", "Purdue University", ["Machine Learning", "Meme History"], "https://www.purdue.edu/"));

#uploadData("Purdue Pete", "Purdue University", ["Machine Learning", "Meme History", "Biocomputing"], "https://www.purdue.edu/", [["title1", "link1"], ["title2", "link2"], ["title3", "link3"]])

#print(f'{literalSearch("Meme History")} => {literalSearch("Meme History").to_dict}')
#doc = literalSearch("Meme History")
#print(f'Document data: {doc.to_dict()}')
