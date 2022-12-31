import requests
from bs4 import BeautifulSoup
import urllib
from pathlib import Path

folderName = 'actorImages'
imdbListURL = 'https://www.imdb.com/chart/top/?sort=rk,asc&mode=simple&page=1'

def getHTML(url):
    print('getting HTML from \"' + url + '\"')
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    x = requests.get(url, headers=headers)
    return BeautifulSoup(x.text, 'html.parser')
def printActorImagesForMovie(movieURL, imagesList=[]):
    movieSoup = getHTML(movieURL)
    for actor in movieSoup.select('.title-cast__grid .ipc-lockup-overlay'):
        actorURL = urllib.parse.urljoin('https://www.imdb.com/' ,actor.get('href'))
        actorSoup = getHTML(actorURL)
        actorImg = actorSoup.select('.ipc-page-section .ipc-media img')[0]
        if(actorImg.get('width') != '90'): #No image for actor (in this case an image of width 90 is the first found element)
            actorName = actorSoup.select('h1 span')[0].string
            print('Saving image of \"' + actorName + '\"')
            actorImageURL = actorImg.get('srcset').split(' ')[-2]
            #imagesList.append(actorImageURL)
            Path(folderName).mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(actorImageURL, folderName + '/' + actorName.replace(' ', '_') + '.jpg')
            
top250soup = getHTML(imdbListURL)
#imagesList = []
for link in top250soup.select('.titleColumn a'):
    movieURL = urllib.parse.urljoin('https://www.imdb.com/' ,link.get('href'))
    printActorImagesForMovie(movieURL) #, imagesList)
