import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import requests

# Some constants for safe-keeping (:
gsearchUrl = "https://google.com/search?q="
targetUrl  = "site:https://www.searchenginejournal.com/ "
queryLang  = "&hl=en&lr=lang_en"
headers    = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
}
# Limit the amount of visited google pages per keyword
searchDepthMax = 2
# List of keywords to be searched
searchKeywords = []

# Populate list of keywords used for search
# Perhaps look into fetching a keyword on per-query basis 
# possible bottleneck if keyword file happens to be too large
with open('keywords.txt', 'r', encoding = 'UTF-8') as f:
    keywords = f.readlines()
    searchKeywords = [keyword.rstrip() for keyword in keywords]

# Overwrite previous links file & get the handle
links_file = open("links.csv", "w")
# Overwrite previous result : keyword file & get the handle
results_file = open("results.csv", "w")

# Parse the page looking for URLs pointing at our target & 
# write finds to the links csv file
def getSearchPageURL(soup):
    #for divurl in soup.find_all('div', class_="yuRUbf"):
    #   url = divurl.a['href']
    for link in soup.find_all('a', href = True):
        url = link['href']
        if url[:36] == 'https://www.searchenginejournal.com/':
            links_file.write(url + ',\n')

# Parse the page looking for 'result-stats' div to obtain total amount of
# indexed pages related to the search & save to file
def getResultsCount(soup, keyword):
    resultDiv = soup.find('div', id = 'result-stats')
    # If result-div is not found the search netted no results
    if resultDiv is None:
        resultCount = 0
    else:
        resultCount = resultDiv.text.split(" ")[1]
    results_file.write(str(resultCount) + ", " + keyword + ",\n")


# Crawl search pages for given keyword
def crawlPages(soup, searchDepth = 0):
    while searchDepth < searchDepthMax:
        getSearchPageURL(soup)
        # These css class searches are very fragile and easily broken
        # quite likely it will not get us any results as soon as we swap user-agent
        # consider using more crude method of finding & extracting the next-page url
        nextPage = soup.find_all('td', class_ = "d6cvqb")

        # Terrible choice, exceptions aren't the cheapest after all
        # but if we encounter one we're out of crawling 
        # TODO: Look into improving this part
        try:
            nextPage = nextPage[1].a['href']
            searchDepth += 1
        except:
            break

        response = requests.get(
            'https://google.com' + nextPage,
            headers = headers).text

        soup = BeautifulSoup(response, 'lxml')

# Main script loop
for keyword in searchKeywords:
    # Prepare initial query string
    parsedUrl = urllib.parse.quote_plus(targetUrl + keyword)
    queryUrl = gsearchUrl + parsedUrl + queryLang

    response = requests.get(
        queryUrl,
        headers = headers).text

    # Parse the raw html into easier to work with form
    soup = BeautifulSoup(response, 'lxml')

    getResultsCount(soup, keyword)
    crawlPages(soup)



links_file.close()
results_file.close()