import requests
from bs4 import BeautifulSoup
import subprocess
from tqdm import tqdm
import os

# define the name of the directory to be created
path = os.getcwd()+'/scraped_data'

try:
    os.mkdir(path)
except OSError:
    print("\nCreation of the directory %s failed" % path)
else:
    print("\nSuccessfully created the directory %s " % path)


# Using f"{}" instead of normal variable parsing because sometimes it doesn't work, i don't know why, i don't care why
def wget(link):
    subprocess.run([f"wget --content-disposition -q --no-check-certificate -P \"{path}\" \"{link}\""], shell=True)


# Theoretically you can make this can scrape everything from brewology but I cant promise anything
# Tested and works for psp
def page_change(num: int):
    page = "https://psp.brewology.com" + f"/downloads/?dcid=1&np={num}&search="
    return page


# Hardcoded the pages because i cant bother grabbing them like this, just load up the site and see the total page number
# At the time of writing they were 368
pages = 368


def scrape_page(url: str):
    links = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.findAll('a'):
        temp = str(link.get('href'))
        if "/downloads/download.php?id" in temp:
            links.append(temp)
    for i in range(0, len(links)):
        links[i] = links[i].replace('download.php', 'get.php')
        links[i] = "https://psp.brewology.com" + links[i]
    return links


if __name__ == '__main__':
    print(' ')
    print(' ')
    print('---------------')
    print('Brewology PSP Homebrew Scraper')
    print('Made by Crisp')
    print('---------------')
    print(' ')
    print(' ')
    print(f'LOADING LINKS FROM {pages} PAGES')
    total_links = []
    for i in tqdm(range(1, pages)):
        links = scrape_page(page_change(i))
        for j in range(0, len(links)):
            total_links.append(links[j].replace('&mcid=1', ''))
    print(' ')
    print(' ')
    print('---------------')
    print(' ')
    print('This will probably take a long time, brewology\'s bandwidth isn\'t great')
    print(f'DOWNLOADING {len(total_links)} LINKS TO \"{path}\"')
    print(' ')
    for k in tqdm(range(0, len(total_links))):
        wget(total_links[k])
