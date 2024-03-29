from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
import time
import lxml


def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    article_list = soup.find("ul", class_="item_list")
    news_title = article_list.find("div", class_="content_title").text
    news_p = article_list.find("div", class_="article_teaser_body").text

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    browser.find_by_css('div.carousel_items a.fancybox').click()
    time.sleep(1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    featured_image = soup.find('img', class_='fancybox-image')
    featured_image_url = "https://www.jpl.nasa.gov" + \
        str(featured_image).split(" ")[2].split('"')[1]

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)
    mars_weather = browser.find_by_css(
        'div.js-tweet-text-container p.tweet-text').text

    url = "https://space-facts.com/mars/"

    mars_facts_df = pd.read_html(url)[0]
    mars_facts_df = mars_facts_df.rename(index=str, columns={0: "Description", 1: "Value"})
    mars_facts_html = mars_facts_df.to_html(index='False')

    mars = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts_html
    }

    return mars