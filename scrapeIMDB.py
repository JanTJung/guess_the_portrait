import requests
from bs4 import BeautifulSoup
import urllib
from pathlib import Path

folder_name = 'actorImages'
imdb_list_url = 'https://www.imdb.com/chart/top/?sort=rk,asc&mode=simple&page=1' #IMDb Top 250 Movies. Any IMDB list with elements selectable with '.titleColumn a' works

def get_html_as_soup(url):
    """This function returns the HTML contents of a given URL as a BeautifulSoup object.
    
    Parameters
    ----------
    url : str
        The URL adress to retrieve the HTML from

    Returns
    -------
    BeautifulSoup
        The content of the page as BeautifulSoup object
    """
    print('getting HTML from \"' + url + '\"')
    #User Agent needs to be set at the very least for the movie page (otherwise error 403)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    return BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')

def save_actor_images_for_movie(movie_url, images_list=[]):
    """This function iterates over all actors of a given movie passed as IMDB URL and saves the title image to the folder stored in the variable foldername
    
    Parameters
    ----------
    movie_url : str
        The IMDB URL of the movie
    images_list : list, optional
        Currently not used. Might be used in the future to save the actor image URLs into a list instead of saving them while iterating 
    """
    movie_soup = get_html_as_soup(movie_url)
    for actor in movie_soup.select('.title-cast__grid .ipc-lockup-overlay'):
        actor_url = urllib.parse.urljoin('https://www.imdb.com/' ,actor.get('href'))
        actor_soup = get_html_as_soup(actor_url)
        actor_img = actor_soup.select('.ipc-page-section .ipc-media img')[0]
        if(actor_img.get('width') != '90'): #No image for actor (in this case an image of width 90 is the first found element)
            actor_name = actor_soup.select('h1 span')[0].string
            print('Saving image of \"' + actor_name + '\"')
            actor_image_url = actor_img.get('srcset').split(' ')[-2]
            #images_list.append(actor_image_url)
            Path(folder_name).mkdir(parents=True, exist_ok=True)
            urllib.request.urlretrieve(actor_image_url, folder_name + '/' + actor_name.replace(' ', '_') + '.jpg')

print(get_html_as_soup.__doc__)
print(save_actor_images_for_movie.__doc__)

imdb_list_soup = get_html_as_soup(imdb_list_url)
#images_list = []
for link in imdb_list_soup.select('.titleColumn a'):
    movie_url = urllib.parse.urljoin('https://www.imdb.com/' ,link.get('href'))
    save_actor_images_for_movie(movie_url) #, images_list)
