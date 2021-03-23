"""Ensure urllib library is installed first in the 
    environment you will run the program in"""


import os
import requests
import urllib.request, json
from collections import Counter


def country_of_interest(country):
    """ Returns a list that contains dictionaries that contain links
    to download bird recordings, file names among other details.
    
    Args: 
        country: a string of the name of the country the recordings were done
    """

    link='https://www.xeno-canto.org/api/2/recordings?query=cnt:' + country
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        
    pages = data['numPages']
    
    recordings = []
    
    for i in range(pages):
        page  = '&page=' + str(i + 1)

        link='https://www.xeno-canto.org/api/2/recordings?query=cnt:' + country + page
        with urllib.request.urlopen(link) as url:
            data = json.loads(url.read().decode())
            data = data['recordings']
            for i in data:
                recordings.append(i)
        
    
    return recordings


def file_select(country, num_of_species):
    """Returns a dictionary that comprise of links to download the 
    recordings with the the file names as the keys
    
    Args:
        country: a string of the country the recordings were taken
        num_of_species: an integer of the number of most frequent birds
    
    """
    birds_dict = {}    
    recordings = country_of_interest(country)
    species = [i['en'] for i in recordings]
    num_species = Counter(species)
    most_frequent = num_species.most_common(num_of_species)
    for i in most_frequent:
        file_plus_links = {}
        for ii in recordings:
            if ii['en'] == i[0]:
                file_plus_links.update({ii['file-name']:'https:' + ii['file']})
                
        birds_dict.update({i[0]:file_plus_links})

    return birds_dict


def file_download(country, num_of_species, path):
    """ Downloads and save the audio recordings in the specified path
    Args:
        country: a string of the country the recordings were taken
        path: a string of the path the user intends to store the downloads
        num_of_species: an integer of the number of most frequent birds
    
    """
    birds_dict = file_select(country, num_of_species)
    for i in birds_dict:
        path = os.path.join(path, i)
        if os.path.isdir(path) == False:
            directory=os.mkdir(path)    
        for ii in birds_dict[i]:
            url = birds_dict[i][ii]
            myfile=requests.get(url)
            open(os.path.join(path, ii), 'wb').write(myfile.content)


country = input('Enter the name of a country: ')
num_of_species = input('Enter the number of most frequent species: ')
path = ('Enter the path to store the files: ')

file_download(country, num_of_species, path)
