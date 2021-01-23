from firebase_admin import firestore
import firebase_admin
from firebase_admin import credentials

#Initalizes service account if one does not already exist
try:
    cred = credentials.Certificate('insert filepath here')
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

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
    u'fullName': fullName,
    u'education': education,
    u'researchArea': researchAreas,
    u'externalLinks': extLink,
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

## Upload sample data
#uploadData("Tree Mann", ["Stanford University"], ["Computational Chemistry"], "https://en.wikipedia.org/wiki/Stanford_University", [["title1", "link1"], ["title2", "link2"], ["title3", "None"]])
#uploadData("Purdue Pete", ["Purdue University"], ["Computational Chemistry", "Machine Learning", "Meme History"], "https://www.purdue.edu/", [["title1", "link1"], ["title2", "link2"], ["title3", "link3"]])
#uploadData("Perdew Yeet", ["Purdue University"], ["Computational Chemistry"], "https://en.wikipedia.org/wiki/Purdue_University", [["title1", "link1"], ["title2", None], ["title3", "link3"]])
#uploadData("Chuck Norris", ["Harvard University", "UC Berkeley"], ["Computational Chemistry", "Meme History", "Machine Learning"], "https://en.wikipedia.org/wiki/Chuck_Norris", [["title1", None], ["title2", None], ["title3", "link3"], ["title4", "link4"]])
#uploadData("Micheal Reeves", ["Cornell University", "UCLA"], ["Robotics", "Meme History", "Machine Learning", "Computational Chemistry"], "https://www.youtube.com/channel/UCtHaxi4GTYDpJgMSGy7AeSw", [["title1", "link1"], ["title2", None], ["title3", None], ["title4", None]])
#uploadData("Mark Zuckerberg", ["Harvard University"], ["Face Recognition", "Meme History"], None, [["title1", "link1"], ["title2", "link2"], ["title3", None]])


#print(f'{literalSearch("Meme History")} => {literalSearch("Meme History").to_dict}')
#doc = literalSearch("Meme History")
#print(f'Document data: {doc.to_dict()}')
