import requests
from bs4 import BeautifulSoup
import pandas as pd



site = "https://www.abante.com.ph/"



output = {
    'links':[],
    'section_links':[],
    'article_links':[]
}


def scrapeSectionLinks(soup):
    for section in soup.find_all("section"):
        for link in section.find_all("a",href=True):
            href = link.attrs['href']
            if href not in output['section_links']:
                output['section_links'].append(href)


def scrapeArticleLinks(soup):
    for article in soup.find_all("article"):
        for link in article.find_all("a",href=True):
            href = link.attrs['href']
            if href not in output['article_links']:
                output['article_links'].append(href)


def scrapeSite(siteUrl):
    # getting the request from url
    website = requests.get(siteUrl)

    # converting the text
    soup = BeautifulSoup(website.text, "html.parser")


    for link in soup.find_all("a",href=True):
        href = link.attrs['href']
        if not href.startswith("#"):
            if href.startswith("/"):
                href = site + href
            if href not in output['links']:
                output['links'].append(href)
                # No href values with 'article'/'section' found
                # if 'article' in href and href not in output['article_links']:
                #     output['article_links'].append(href)
                # if 'section' in href and href not in output['section_links']:
                #     output['section_links'].append(href)

    scrapeSectionLinks(soup)
    scrapeArticleLinks(soup)

    # This will scrape the link, not sure if this is needed
    # if site in href:
    #     scrapeSite(href)

    return output


print(f"{scrapeSite(site)}")

df = pd.DataFrame({'Result': scrapeSite(site)})
df.to_csv('Result.csv', index=False, encoding='utf-8')
