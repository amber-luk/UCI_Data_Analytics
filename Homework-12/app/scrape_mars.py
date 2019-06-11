import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist


def scrape():
    scraped_data = {}

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    # NASA Mars News
    url_news = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url_news)

    html_news = browser.html
    soup_news = BeautifulSoup(html_news, 'html.parser')

    result_title = soup_news.find('div', class_='content_title').find('a')
    news_title = result_title.text.strip()
    scraped_data["news-headline"] = news_title

    result_p = soup_news.find('div', class_='image_and_description_container').find('div', class_='rollover_description_inner')
    news_p = result_p.text.strip()
    scraped_data["news-text"] = news_p


    # JPL Mars Space Images - Featured Image
    url_img = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_img)

    html_img = browser.html
    soup_img = BeautifulSoup(html_img, 'html.parser')

    featured_title = soup_img.find('section', class_='primary_media_feature').find('h1', class_='media_feature_title').text.strip()

    browser.find_by_id('full_image').click()

    browser.is_element_present_by_text('more info')
    browser.find_link_by_partial_text('more info').click()

    featured_image_url = browser.find_by_css('img[class="main_image"]')['src']
    scraped_data["featured-image"] = featured_image_url


    # Mars Weather
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twitter)

    html_twitter = browser.html
    soup_twitter = BeautifulSoup(html_twitter, 'html.parser')

    mars_weather = soup_twitter.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    scraped_data["Mars-weather-tweet"] = mars_weather


    # Mars Facts
    url_facts = 'https://space-facts.com/mars/'
    facts_table = pd.read_html(url_facts)[0]
    facts_table.columns = ['description', 'mesurement']
    facts_table_html = facts_table.to_html()
    scraped_data["table-of-facts-(html)"] = facts_table_html


    # Mars Hemispheres
    url_hems = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hems)

    html_hems = browser.html
    soup_hems = BeautifulSoup(html_hems, 'html.parser')

    mars_hemisphere_products = browser.find_by_css('a.product-item h3')
    hemisphere_image_urls = []

    for i in range(len(mars_hemisphere_products)):
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[i].click()
        hemisphere["img_url"] = browser.find_link_by_partial_text('Sample').first['href']
        hemisphere["title"] = browser.find_by_css('h2.title').text
        hemisphere_image_urls.append(hemisphere)

        browser.back()

    scraped_data["Mars-hemisphere-images"] = hemisphere_image_urls

    return scraped_data
