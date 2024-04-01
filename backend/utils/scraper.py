import math
import threading
from selenium import webdriver
import selenium
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
#from webdriver_mananger.chrome import ChromeDriverManager

def get_driver(headless=False):
    options = Options()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
    #service = Service(ChromeDriverManager().install())
    if headless:
        options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    return driver

def get_frontpage_post_URLs(ticker:str,driver, WSB=True):
    """Retrieves all URLs of posts on the front page of r/wallstreetbets that mention a given ticker
    ARGS: ticker (str): The ticker to search for
    RETURN: list: A list of URLs of posts that mention the given ticker"""
    
    print("getting links")
    url = "https://www.reddit.com/r/wallstreetbets/search/?q=%2Bflair%3ADiscussion+"+ticker+"&type=link&cId=33c4f3c1-04bc-48c9-88ba-2e29358869c2&iId=dd948810-572a-476a-84e1-a666783866b0&sort=relevance&t=week"
    POST_URL_XPATH = "//a[@data-testid='post-title'][@href]"
    
    if not WSB:
        url = "https://www.reddit.com/r/stocks/search/?q=%20"+ticker+"%20%20&restrict_sr=1&t=week"
    
    
    driver.get(url)

    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, POST_URL_XPATH)))
    all_posts = driver.find_elements(By.XPATH,POST_URL_XPATH)

    post_urls = []
    for post in all_posts:
        post_urls.append(post.get_attribute("href"))
    return post_urls

#Old method for getting text from a single post
def get_text_from_post(url:str):
    """Retrieves the text of a single post on reddit (OLD METHOD)"""
    options = Options()
    #options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    
    driver.get(url)
    post_text = ""
    
    TITLE_XPATH = "//h1[@slot='title']" 
    title = driver.find_element(By.XPATH, TITLE_XPATH).text
    post_text += "Title: " + title + "\n"

    READ_MORE_XPATH = "//button[contains(text(),'Read more')]"
    try:
        read_more_button = driver.find_element(By.XPATH, READ_MORE_XPATH)
        #print(type(read_more_button))
        read_more_button.click()
    except:
        pass

    TEXT_XPATH = "//div[@slot='text-body']/*/*/p"
    all_text = driver.find_elements(By.XPATH, TEXT_XPATH)
    for text in all_text:
        post_text+=text.text+" "
    #print(post_text)
    return post_text

def get_texts_from_posts(urls:list, driver):
    
    #XPATHs for required elements on reddit post page
    TITLE_XPATH = "//h1[@slot='title']"
    READ_MORE_XPATH = "//button[contains(text(),'Read more')]"
    TEXT_XPATH = "//div[@slot='text-body']/*/*/p"

    post_texts = []
    for url in urls:
        driver.get(url)

        #Wait for page to load
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, TITLE_XPATH)))
        except TimeoutException:
            #Usually means reddit blocked the request because it was too fast, so just try again
            try:
                driver.get(url)
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, TITLE_XPATH)))
            except:
                #If it fails again, just skip this post
                continue

        #Get title of post
        title = driver.find_element(By.XPATH, TITLE_XPATH).text

        #Skip posts about potentially irrelevant discussions
        if "What Are Your Moves Tomorrow" in title or "Daily Discussion" in title:
            continue
        post_text = "Title: " + title + "\n"
        
        #Long posts have a "Read more" button, so click it if it exists
        try:
            read_more_button = driver.find_element(By.XPATH, READ_MORE_XPATH)
            read_more_button.click()
        except:
            pass
        
        #Get all text elements in main post
        all_text = driver.find_elements(By.XPATH, TEXT_XPATH)
        for text in all_text:
            post_text+=text.text+" "

        if post_text is not None:
            post_texts.append(post_text)
        
        #Wait so reddit doesn't auto-block next request
        time.sleep(0.3)
    return post_texts

def get_all_discussions(ticker:str):
    driver = get_driver(headless=True)

    #Get all posts from r/wallstreetbets
    all_posts = get_frontpage_post_URLs(ticker,driver)
    all_texts = get_texts_from_posts(all_posts,driver)

    #Get all posts from r/stocks
    all_posts = get_frontpage_post_URLs(ticker,driver, False)
    all_texts += get_texts_from_posts(all_posts,driver)

    return all_texts
    """for post in all_posts:
        text = get_text_from_post(post)
        print(text)
        if text is None or "What Are Your Moves Tomorrow" in text or "Daily Discussion" in text:
            print("skipping")
            continue
        all_texts.append(text)
        print("appended")
    print(len(all_texts))
    return all_texts"""

if __name__ == "__main__":
    discussions = get_all_discussions("NVDA")
    print(len(discussions))