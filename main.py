import json
import re
from bs4 import BeautifulSoup
import requests
import spacy
from textblob import TextBlob
from string import punctuation
from itertools import chain
import nltk
#https://www.cs.purdue.edu/people/faculty/apothen.html
#https://www.cs.purdue.edu/people/faculty/pfonseca.html
#https://www.cs.purdue.edu/people/faculty/mja.html
#https://www.cs.purdue.edu/people/faculty/aref.html
#https://www.cs.purdue.edu/people/faculty/pdrineas.html
url = 'https://www.cs.purdue.edu/people/faculty/apothen.html'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')
nlp = spacy.load("en_core_web_sm")

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
    publications = soup.find_all('strong')
    publications_list = []
    for pub in publications:
        publications_list.append(pub.text)
    print(publications_list)

def get_website():
    soup = BeautifulSoup(url)
    links = []

    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))

    return links

def get_bio():
    page = soup.find_all('p')
    search_words = set(["research"])
    blob = TextBlob(page[3].text + page[4].text + page[5].text)
    if (blob.sentences[0].find("research") == -1 and blob.sentences[1].find("research") == -1):
        return [blob.sentences[0]]
    else:
        matches = [str(s) for s in blob.sentences if search_words & set(s.words)]
        if len(matches) > 0:
            result = []
            for match in matches:
                result.append(extract_keywords(nlp, match))
                tagged_sentence = nltk.tag.pos_tag(match.split())
                for word in tagged_sentence:
                    if(word[1] == 'PRP' or  word[1] == 'PRP$'):
                        match = match.replace(word[0], get_name())
                        return [match]
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
    return name, bio, education, search_q

if __name__ == "__main__":
    print(make_data())