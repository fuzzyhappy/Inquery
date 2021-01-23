from bs4 import BeautifulSoup
import urllib.request


html_page = urllib.request.urlopen("https://www.cs.purdue.edu/people/faculty/apsomas.html")
soup = BeautifulSoup(html_page, features='lxml')
rawLinks = soup.find_all('a', href=True)
links = []
extLinks = []
jpgIndex = -1
footerIndex = -1


for i in range(len(rawLinks)):
    links.append(rawLinks[i].get('href'));
    if(jpgIndex == -1 and links[i].find(".jpg") != -1): #Finds index of jpg file and '#footerone'
        jpgIndex = i
    elif(footerIndex == -1 and links[i] == "#footerone"):
        footerIndex = i

extLinks = links[jpgIndex+1:footerIndex]

## Write links to txt file with indices. Useful for debugging.
# with open("links_test.txt", "w") as f:
#     i = 0
#     for line in links:
#         f.write(str(i) +" " + line + "\n")
#         i += 1;
#
#print(extLinks)

