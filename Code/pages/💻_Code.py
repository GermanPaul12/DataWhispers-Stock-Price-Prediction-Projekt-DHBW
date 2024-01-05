import streamlit as st

st.title("Our Code 💻")

if st.checkbox("Web-Scraping with Selenium"):
    
    st.code('''
            import time
from concurrent import futures
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

START_AT_STARTTIME = 43770  # date epoch as used by economictimes
END_AT_STARTTIME = 43921


def get_fresh_driver():
    """
    Get a fresh Chrome driver with a Google Bot User Agent.
    :return: selenium.webdriver.Chrome
    """
    driver_path = "/opt/homebrew/bin/chromedriver" # CHANGE THIS TO YOUR PATH
    s = Service(driver_path)
    user_agent = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html)"  # Google Bot User Agent
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--no-sandbox')
    options.add_argument('—-disable-extensions')
    driver = webdriver.Chrome(service=s, options=options)

    return driver


def save_html(link: str):
    """
    Worker function, executed in parallel. Saves a single HTML of the given link to a file in ./data/{date}/
    :param link: str
    :return:
    """
    MAX_RETRIES = 2
    import uuid
    date = link[-5:]
    link = link[:-5]
    success = False
    retries = 0
    driver = None
    while not success and retries < MAX_RETRIES:
        try:
            driver = get_fresh_driver()
            driver.get(link)
            time.sleep(4)
            _ = driver.find_element(By.XPATH, '/html/body/main/header')
            success = True
        except:
            driver.quit()
            time.sleep(10)
            retries += 1
            print(f"RETRY_{link}_{date}...")
    uuid = uuid.uuid4()
    with open(f'./data/{date}/{uuid}.html', 'w') as f:
        f.write(driver.page_source)
    driver.quit()


def run():
    """
    Run the scraping. See constants above for the start and end date. Store HTMLs to files in ./data/{date}/
    :return: None
    """
    MAX_RETRIES = 2
    for starttime in range(START_AT_STARTTIME, END_AT_STARTTIME + 1):
        success = False
        retries = 0
        element = None
        while not success and retries < MAX_RETRIES:
            
            try:
                driver = get_fresh_driver()
                driver.get(f"http://economictimes.indiatimes.com/archivelist/starttime-{starttime}.cms")
                time.sleep(5)
                element = driver.find_element(By.XPATH, '/html/body/main/div[8]/section/span/table[2]/tbody')
                success = True
                print(f"success_{starttime}")
            except:
                driver.quit()
                time.sleep(30)
                retries += 1
                print(f"RETRY_{starttime}...")

        # Find all the anchor elements within the div
        link_elements = element.find_elements(By.TAG_NAME, 'a')

        # Get only the first 100 link_elements
        link_elements = link_elements[:100]
        links = []

        # Extract the href attributes from each anchor element and store them in a list
        for link in link_elements:
            links.append(link.get_attribute('href') + str(starttime))
            # pool.apply_async(save_html, args=(link.get_attribute('href'), starttime))

        Path(f"./data/{starttime}").mkdir(parents=True, exist_ok=True)

        driver.quit()

        print(f"start threading with {len(links)} articles...")
        with futures.ThreadPoolExecutor(max_workers=16) as executor:
            executor.map(save_html, links)


if __name__ == '__main__':
    run()
''')

if st.checkbox("Requirements"):
    st.code('''
            nltk==3.7
pandas==1.4.1
scikit_learn==1.3.2
selenium==4.15.2
lxml==4.9.3
bertopic==0.16.0
docarray==0.39.1
gensim==4.3.2
plotly==5.15.0
streamlit==1.26.0
cufflinks==0.17.3''')   
     