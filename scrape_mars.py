# DEPENDENCIES
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

# WRAP CODE IN SCRAPE FUNCTION
def scrape_all():
    #####################
    #####################

    # NASA MARS NEWS

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    content_title = soup.find(class_="content_title").text.replace('\n', '')
    content_paragraph = soup.find(class_="rollover_description_inner").text.replace('\n', '')

    #####################
    #####################

    # JPL MARS FEATURED IMAGE
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find desired info
    footer = soup.find('footer')
    img = footer.find('a')
    link = img['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + link

    browser.quit()

    #####################
    #####################

    # MARS WEATHER

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')

    # reset variable in case of multiple runs
    mars_weather = 'a'

    # loop with break point after most recent tweet by @MarsWxReport
    for x in range(1,2):
        tweets = soup.find_all(class_="tweet")
        for tweet in tweets:
            tweet_id = tweet['data-tweet-id']
            tweet_user = tweet['data-screen-name']
            #ensure scraped tweet was authored by this account and not retweeted
            if tweet_user == 'MarsWxReport':
                mars_weather = tweet.find(class_="content").find(class_="js-tweet-text-container").find('p').text
                break

    #####################
    #####################

    # MARS FACTS

    # scrape page for tables
    url = 'https://space-facts.com/mars/'
    table = pd.read_html(url)

    # Convert table to DataFrame 
    df = table[0]
    df = df.transpose()
    df.columns = df.iloc[0].str.replace(":", "")
    df = df.drop(0)
    df = df.transpose()

    # Convert DataFrame to HTML table
    html_table = df.to_html().replace('\n', '')
    html_table = html_table.replace('>1<','Value')
    html_table = html_table.replace('>0<','Fact')

    #####################
    #####################

    # MARS HEMISPHERES
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Initialize Lists
    hemisphere_image_urls = []
    img_url = []
    title = []
    links_to_visit = []

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')

    # Find desired info
    descriptions = soup.find_all(class_='description')
    for description in descriptions: 
        link = description.find('a')
        h3 = link.find('h3')
        partial_text = h3.text
        links_to_visit.append(partial_text)

    for link in links_to_visit:
        add_title = link.replace(" Enhanced", "")
        title.append(add_title)
        browser.click_link_by_partial_text(link)
        html = browser.html
        soup = bs(html, 'html.parser')
        download = soup.find(class_='downloads')
        ul = download.find('ul')
        li = ul.find('li')
        lnk = li.find('a')
        add_url = lnk['href']
        img_url.append(add_url)
        browser.visit(url)
        html = browser.html
        soup = bs(html, 'html.parser')

    browser.quit()

    dict_0 = {"title": title[0], "img_url": img_url[0]}
    dict_1 = {"title": title[1], "img_url": img_url[1]}
    dict_2 = {"title": title[2], "img_url": img_url[2]}
    dict_3 = {"title": title[3], "img_url": img_url[3]}
    hemisphere_image_urls.append(dict_0)
    hemisphere_image_urls.append(dict_1)
    hemisphere_image_urls.append(dict_2)
    hemisphere_image_urls.append(dict_3)

    #####################
    #####################

    data_dict = {
        "content_title": content_title,
        "content_paragraph": content_paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "html_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # RETURN RESULTS
    return data_dict
