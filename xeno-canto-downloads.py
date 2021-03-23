import os
import requests
import urllib.request, json

def bird_of_interest(bird):
    """ Returns a list that contains dictionaries that contain links
    to download bird recordings, file names among other details.
    
    Args: 
        bird: a string of the name of the bird of interest
    """
    
    bird=bird.replace(' ','%20')
    link='https://www.xeno-canto.org/api/2/recordings?query=' +bird
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        
    data=data['recordings']
    return data
    
def file_select(bird,country):
    """Returns a dictionary that comprise of links to download the 
    recordings with the the file names as the keys
    
    Args:
        bird: a string of the name of the bird of interest
        country: a string of the country the recordings were taken
    
    """
    data=bird_of_interest(bird)
    file_links={}
    for i in data:
        if i['cnt'].lower()==country.lower():
            file_links.update({i['file-name']:i['file']})
    return file_links

def file_download(bird,country,path):
    """ Downloads and save the audio recordings in the specified path
    Args:
        bird: a string of the name of the bird of interest
        country: a string of the country the recordings were taken
        path: a string of the path the user intends to store the downloads
    
    """
    file_links=file_select(bird,country)
    path=path+bird
    if os.path.isdir(path)==False:
        directory=os.mkdir(path)
    
        
    for i in file_links:
        url='https:'+file_links[i]
        myfile=requests.get(url)
        open(path+'/'+i, 'wb').write(myfile.content)

bird = input('Enter the bird of interest: ')

file_download(bird,'Kenya','C:/users/Gabe/downloads/')