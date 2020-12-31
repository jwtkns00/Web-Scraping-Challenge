from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {"executable_path": "/Users/jw/Desktop/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')[0].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    
    jpl_url = 'https://www.jpl.nasa.gov'
    images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(images_url)
    html = browser.html
    image_soup = bs(html, 'html.parser')
    image = image_soup.find_all('img')[3]['src']
    image_url = jpl_url + image

    facts_url = 'https://space-facts.com/mars/'
    mars_facts = pd.read_html(facts_url)
    mars_df = mars_facts[0]
    mars_df.columns = ['Description', 'Value']
    mars_df.set_index('Description', inplace=True)
    html_table = mars_df.to_html()
    html_table.replace("\n", '')
    mars_df.to_html("mars_facts_data.html")

    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    soup = bs(hemisphere_html, "html.parser")
    results = soup.find("div", class_= "result-list")
    hemispheres = results.find_all("div", class_="item")
    hemispheres_image_urls = []

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemispheres_image_urls.append({"title": title, "img_url": image_url})

    mars_dict = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": image_url,
        "fact_table": str(html_table),
        "hemisphere_images": hemispheres_image_urls
    }

    return mars_dict





