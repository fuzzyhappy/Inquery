## List of professors https://www.cs.purdue.edu/research/
## Common test pages
# https://www.cs.purdue.edu/people/faculty/popescu.html
# https://www.cs.purdue.edu/people/faculty/rego.html
# https://www.cs.purdue.edu/people/faculty/apothen.html (Contains publications, with links)
# https://www.cs.purdue.edu/people/faculty/apsomas.html (Blank page, only external links)
# https://www.cs.purdue.edu/people/faculty/mingyin.html
# https://www.cs.purdue.edu/people/faculty/dgleich.html (Issues with getting extLinks, no .jpg found?)

from bs4 import BeautifulSoup
import urllib.request

# Returns array of external links (personal webpage and research pages) from Professor's website
# Can set logData to True to generate a txt file of links and indices found on the page
def getExternalLinks(site, logData=False):
    html_page = urllib.request.urlopen(site)
    soup = BeautifulSoup(html_page, features='lxml')
    rawLinks = soup.find_all('a', href=True)
    links = []
    jpgIndex = -1
    footerIndex = -1
    
    for i in range(len(rawLinks)):
        links.append(rawLinks[i].get('href'));
        if(jpgIndex == -1 and links[i].find(".jpg") != -1): #Finds index of jpg file and '#footerone'
            jpgIndex = i
        elif(footerIndex == -1 and links[i] == "#footerone"):
            footerIndex = i
    
    if(logData):
        ## Write links to txt file with indices. Useful for debugging.
        print(links[jpgIndex+1:footerIndex]) #Prints returned values
        with open("links_test.txt", "w") as f: #Logs all links found with indices
            i = 0
            for line in links:
                f.write(str(i) +" " + line + "\n")
                i += 1;
                
    
    return links[jpgIndex+1:footerIndex]

getExternalLinks("https://www.cs.purdue.edu/people/faculty/mingyin.html", True)



