# Dependencies 
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import os
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # Path to my chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)
    
# Create dictionary to import into Mongo
mars_dict = {}

# Mars News
def news():

        # Initialize browser 
        browser = init_browser()

        
        # Visit url 
        news_url = 'https://redplanetscience.com/'
        browser.visit(news_url)

        # HTML and parse
        html = browser.html
        soup = bs(html, 'html.parser')

        # Retrieve title and paragraph for latest news
        title = soup.find("div", class_ = "content_title").text
        paragraph = soup.find("div", class_ = "article_teaser_body").text
        # Dictionary entry from mars news
        mars_dict['news_title'] = title
        mars_dict['news_paragraph'] = paragraph

        return mars_dict

        #browser.quit()

# Featured Image
def image():

        # Initialize browser 
        browser = init_browser()


        # Visit url
        space_url = 'https://spaceimages-mars.com/'
        browser.visit(space_url)

        # html and parse
        image_html = browser.html
        soup = bs(image_html, 'html.parser')

        # Retrieve background-image url from style tag 
        image_url  = soup.find_all('img')[1]["src"]
        featured_image_url = space_url + image_url

      # Dictionary entry from FEATURED IMAGE
        mars_dict['featured_image_url'] = featured_image_url 
        
#         browser.quit()

        return mars_dict

        
        
# Mars Facts
def facts():

        # Initialize browser 
        browser = init_browser()

         # Set url and read tables
        facts_url = 'https://galaxyfacts-mars.com/'
        browser.visit(facts_url)
        tables = pd.read_html(facts_url)
        mars_df = tables[1]
        #Assign columns
        mars_df.columns = ['Description', 'Value']
        html_table = mars_df.to_html(table_id="html_tbl_css",justify='left',index=False)

        # Dictionary entry from Mars Facts

        mars_dict['tables'] = html_table

        return mars_dict

# Mars Hemisphere

def hemispheres():

        # Initialize browser 
        browser = init_browser()

        # Visit hemispheres website through splinter module 
        hemis_url = 'https://marshemispheres.com/'
        browser.visit(hemis_url)

        # html and parse
        html_hemis = browser.html
        soup = bs(html_hemis, 'html.parser')

        # Retreive all items 
        items = soup.find_all('div', class_='item')

        # Create list for urls 
        hemis_image_urls = []

        # Store main_url 
        hemis_main_url = 'https://marshemispheres.com/' 

        # Loop through stored items
        for i in items: 
            # Title
            title = i.find('h3').text
            
            # Link
            partial_img_url = i.find('a', class_='itemLink product-item')['href']
            
            # Visit link
            browser.visit(hemis_main_url + partial_img_url)
            
            # image
            partial_img_html = browser.html
            
            # Parse 
            soup = bs( partial_img_html, 'html.parser')
            
            # Retrieve full image 
            img_url = hemis_main_url + soup.find('img', class_='wide-image')['src']
            
            # Append the retreived information into a list of dictionaries 
            hemis_image_urls.append({"title" : title, "img_url" : img_url})

        mars_dict['hemisphere_image_urls'] = hemis_image_urls
        
       
        browser.quit()

        # Return mars_data dictionary 

        return mars_dict