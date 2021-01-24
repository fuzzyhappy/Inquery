import json
import re
from bs4 import BeautifulSoup
import requests
import spacy
from textblob import TextBlob
from string import punctuation
from itertools import chain

from BoilerMake8Build import link_extraction as la

from bs4 import BeautifulSoup
import urllib.request
from re import finditer

import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
#[https://www.cs.purdue.edu/people/faculty/apothen.html
#https://www.cs.purdue.edu/people/faculty/pfonseca.html
#https://www.cs.purdue.edu/people/faculty/mja.html
#https://www.cs.purdue.edu/people/faculty/aref.html
#https://www.cs.purdue.edu/people/faculty/pdrineas.html
#https://www.cs.purdue.edu/people/faculty/bxd.html
#https://www.cs.purdue.edu/people/faculty/cmh.html
#https://www.cs.purdue.edu/people/faculty/bxd.html
#https://www.cs.purdue.edu/people/faculty/lintan.html
#https://www.cs.purdue.edu/people/faculty/xyzhang.html
#https://www.cs.purdue.edu/people/faculty/yunglu.html
#https://www.cs.purdue.edu/people/faculty/clifton.html
#https://www.cs.purdue.edu/people/faculty/akate.html
#https://www.cs.purdue.edu/people/faculty/fahmy.htm


def extract_keywords(nlp, sequence, special_tags: list = None):
    result = []
    pos_tag = ['PROPN', 'NOUN', 'ADJ']

    doc = nlp(sequence.lower())

    if special_tags:
        tags = [tag.lower() for tag in special_tags]
        for token in doc:
            if token.text in tags:
                result.append(token.text)

    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk = final_chunk + token.text + " "
        if final_chunk:
            result.append(final_chunk.strip())

    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            result.append(token.text)
    return list(set(result))

def get_name():
    name = soup.find('h1')
    return(name.text)

def get_education():
    education = soup.find_all('div', class_ = 'education')
    education_list = []
    for edu in education:
        education_list.append(edu.text)
    return(education_list)

def get_research_spec():
    page = soup.find_all('p')
    search_words = set(["research"])
    blob = TextBlob(page[3].text + page[4].text + page[5].text)

    matches = [str(s) for s in blob.sentences if search_words & set(s.words)]
    if len(matches)>0:
        # load the small english language model,
        result = []
        for match in matches:
            result.append(extract_keywords(nlp, match))
        return result

def get_areas():
    page = soup.find_all('p')
    areas = page[3].text
    results = extract_keywords(nlp, areas)
    return results

def get_research():
    page = soup.find_all('p')
    research = page[6].text
    results = extract_keywords(nlp, research)
    return results

def get_publications():
    la.getPageData(url)
    return la.getPublications()

def get_website():
    soup = BeautifulSoup(url)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    return links

def get_bio():
    page = soup.find_all('p')
    search_words = set(["research", "interest"])
    blob = TextBlob(page[3].text + page[4].text + page[5].text)
    if (blob.sentences[0].find("research") == -1 and blob.sentences[1].find("research") == -1 and blob.sentences[2].find("research") == -1):
        return [blob.sentences[0].string]
    else:
        matches = [str(s) for s in blob.sentences if search_words & set(s.words)]
        if len(matches) > 0:
            result = []
            for match in matches:
                result.append(extract_keywords(nlp, match))
                #tagged_sentence = nltk.tag.pos_tag(match.split())
                # for word in tagged_sentence:
                #     if(word[1] == 'PRP' or  word[1] == 'PRP$'):
                #         match = match.replace(word[0], get_name() + "'s")
                #         # if(word[1] == 'PRP$'):
                #         #     match = match.replace(word[0], get_name() + "'s")
                #         if(match.count(get_name())<2):
                #             return [match]
            return matches

def make_data():
    name = get_name()
    try:
        bio = get_bio()[0]
    except:
        bio = []
    education = get_education()
    r_s = get_research()
    r_l = list(chain.from_iterable(r_s))
    try:
        if (get_research_spec()[0] is not None):
            final_list = set(r_l + get_areas() + get_research())
        else:
            final_list = set(get_areas() + get_research())
    except:
        final_list = []
    parse_fin_list = []
    for elem in final_list:
        if len(elem) > 5:
            parse_fin_list.append(elem)
    search_q = parse_fin_list
    pub = get_publications()
    return name, bio, education, search_q, pub


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Initalizes service account if one does not already exist
try:
    cred = credentials.Certificate('/Users/shellyschwartz/PycharmProjects/boilerMake/BoilerMake8Build/boilermake-8-project-firebase-adminsdk-n45vg-c326d22181.json')
    firebase_admin.initialize_app(cred)
except ValueError:
    pass

db = firestore.client()


# profRef = db.collection(u'profdata')

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
def uploadData(fullName, bio, education, researchAreas, extLink, publications):
    currentRef = db.collection(u'profdata').document(u'' + fullName + '')

    # Converts 2D array of publications to dictionary
    pubTitles = [None] * len(publications);
    pubLinks = [None] * len(publications);
    for i in range(len(publications)):
        pubTitles[i] = publications[i][0];
        pubLinks[i] = publications[i][1];
    pubMap = dict(zip(pubTitles, pubLinks));
    # print(pubMap);

    info = {
        u'fullName': fullName,
        u'education': education,
        u'bio': bio,
        u'researchArea': researchAreas,
        u'externalLinks': extLink,
        u'publications': pubMap
    }
    # print(info);
    currentRef.set(info);
from nltk.stem import PorterStemmer
import nltk
def process(s):
  # converts to lowercase
  s = s.lower()
  # removes punctuation
  s = re.sub(r'[^\w\s]', '', s)
  # converts words to root words (stemming)
  porter = PorterStemmer()
  s = " ".join([porter.stem(word) for word in nltk.tokenize.word_tokenize(s)])
  return s
if __name__ == "__main__":
    url = ["https://www.cs.purdue.edu/people/faculty/spa.html"]
    prof_l = ["https://www.cs.purdue.edu/people/faculty/xmt.html","https://www.cs.purdue.edu/people/faculty/rompf.html","https://www.cs.purdue.edu/people/faculty/spaf.html","https://www.cs.purdue.edu/people/faculty/dkihara.html","https://www.cs.purdue.edu/people/faculty/rego.html","https://www.cs.purdue.edu/people/faculty/aref.html","https://www.cs.purdue.edu/people/faculty/dec.html","https://www.cs.purdue.edu/people/faculty/sbasu.html","https://www.cs.purdue.edu/people/faculty/neville.html","https://www.cs.purdue.edu/people/faculty/popescu.html","https://www.cs.purdue.edu/people/faculty/jblocki.html","https://www.cs.purdue.edu/people/faculty/chunyi.html","https://www.cs.purdue.edu/people/faculty/eps.html","https://www.cs.purdue.edu/people/faculty/yexiang.html","https://www.cs.purdue.edu/people/faculty/bendy.html","https://www.cs.purdue.edu/people/faculty/panli.html", "https://www.cs.purdue.edu/people/faculty/ninghui.html","https://www.cs.purdue.edu/people/faculty/mingyin.html","https://www.cs.purdue.edu/people/faculty/dxu.html","https://www.cs.purdue.edu/people/faculty/apothen.html", "https://www.cs.purdue.edu/people/faculty/pfonseca.html", "https://www.cs.purdue.edu/people/faculty/mja.html", "https://www.cs.purdue.edu/people/faculty/aref.html","https://www.cs.purdue.edu/people/faculty/pdrineas.html", "https://www.cs.purdue.edu/people/faculty/cmh.html","https://www.cs.purdue.edu/people/faculty/bxd.html","https://www.cs.purdue.edu/people/faculty/lintan.html","https://www.cs.purdue.edu/people/faculty/xyzhang.html","https://www.cs.purdue.edu/people/faculty/yunglu.html","https://www.cs.purdue.edu/people/faculty/clifton.html","https://www.cs.purdue.edu/people/faculty/fahmy.html"]
    print(len(prof_l))
    for url in prof_l:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        nlp = spacy.load("en_core_web_sm")
        # name, bio, education, search_q
        name = make_data()[0]
        bio = make_data()[1]
        print(bio)
        edu = make_data()[2]
        search_q = make_data()[3]
        pub = make_data()[4]
        print(pub)
        n_l = []
        # for word in search_q:
        #     n_l.append(process(word))
        # uploadData(name, bio, edu, n_l, [], [])

