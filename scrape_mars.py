# Import dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Initialize chromedriver within a function
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

# Define scrape function
def scrape ():

    # Initialize browser function
    browser = init_browser()
    
    # Initialize mars_data dictionary
    mars_data = {}

    
    # URL of page to be scraped
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)
    nasa_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(nasa_html, 'html.parser')


    # Collect the latest News Title and Paragraph Text.
    latest_news_title = soup.find('div', class_='content_title').text
    latest_news_p = soup.find('div', class_='article_teaser_body').text

    # Store data in dictionary
    mars_data["news_title"] = latest_news_title
    mars_data["news_p"] = latest_news_p


    # URL of page to be scraped
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    expand = browser.find_by_css('a.fancybox-expand')
    jpl_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(jpl_html, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    image = soup.find('img', class_='fancybox-image')['src']
    image_path = f'https://www.jpl.nasa.gov{image}'
    
    # Store data in dictionary
    mars_data["featured_image"] = image_path


    # URL of page to be scraped
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)
    weather_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(weather_html, 'html.parser')

    # Scrape the latest Mars weather tweet from the Mars weather twitter account.
    tweets = soup.find('ol', class_='stream-items')
    weather = tweets.find('p', class_="tweet-text").text

    # Save the tweet text for the weather report as a variable called mars_weather.
    mars_weather = 'Sol 2230 (2018-11-14), high -5C/23F, low -72C/-97F, pressure at 8.59 hPa, daylight 06:22-18:39'

    # Store data in dictionary
    mars_data["weather"] = mars_weather


    # URL of page to be scraped
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    facts_html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(facts_html, 'html.parser')

    # Use Pandas to scrape the table containing facts about the planet from the Mars Facts webpage.
    mars_table = soup.find('table', class_='tablepress tablepress-id-mars')
    column_1 = mars_table.find_all('td', class_='column-1')
    column_2 = mars_table.find_all('td', class_='column-2')

    # Initialize lists to be appended
    descriptions = []
    values = []

    # Append each fact to the relevant list.
    for row in column_1:
        description = row.text.strip()
        descriptions.append(description)
    
    for row in column_2:
        value = row.text.strip()
        values.append(value)
    
    # Convert to DataFrame
    facts_df = pd.DataFrame({
        "Description":descriptions,
        "Value":values
        })

    # Use Pandas to convert the data to a HTML table string.
    facts_html = facts_df.to_html(index=False)
    
    # Store data in dictionary
    mars_data["facts_table"] = facts_html
    
    
    # URL of page to be scraped
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Initialize list to be appended
    hemisphere_image_urls = []

    # Loop through each hemisphere link
    for i in range (1,9,2):
        
        # Initialize dictionary
        hemisphere_dict = {}

        # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres.
        browser.visit(hemispheres_url)
        hemispheres_html = browser.html
        soup = BeautifulSoup(hemispheres_html, 'html.parser')

        # Click each of the links to the hemispheres in order to find the image url to the full resolution image.
        # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name.
        hemisphere_name_links = soup.find_all('a', class_='product-item')
        hemisphere_name = hemisphere_name_links[i].text.strip('Enhanced')
    
        hemisphere_detail_links = browser.find_by_css('a.product-item')
        hemisphere_detail_links[i].click()
        browser.find_link_by_text('Sample').first.click()
        browser.windows.current = browser.windows[-1]
    
        hemisphere_image_html = browser.html
        browser.windows.current = browser.windows[0]
        browser.windows[-1].close()
    
        hemisphere_image_soup = BeautifulSoup(hemisphere_image_html, 'html.parser')
        hemisphere_image_path = hemisphere_image_soup.find('img')['src']

        # Use a Python dictionary to store the data using the keys img_url and title.
        hemisphere_dict['title'] = hemisphere_name.strip()
    
        hemisphere_dict['img_url'] = hemisphere_image_path

        # Append the dictionary with the image url string and the hemisphere title to a list.
        hemisphere_image_urls.append(hemisphere_dict)
    
    # Store data in dictionary
    mars_data["hemisphere_images"] = hemisphere_image_urls

    # Quit out of browser
    browser.quit()

    # Output of scrape function
    return mars_data
    


