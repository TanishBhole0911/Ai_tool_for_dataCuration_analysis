from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from urllib.parse import urljoin, urlparse
from collections import deque
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True
service = Service("./chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chromeOptions)

# Set up Selenium WebDriver
wait = WebDriverWait(driver, 10)
visited_urls = set()
dataset = []

# def extract_useful_content(soup, url):
#     useful_content = ""
    
#     # Extract main content based on common HTML elements
#     main_content = soup.find('main') or soup.find('body') or soup.find('div', class_='main-content') or soup.find('section')
#     if main_content:
#         # Extract paragraphs
#         paragraphs = main_content.find_all('p')
#         for p in paragraphs:
#             useful_content += p.get_text() + "\n\n"
        
#         # Extract list items
#         lists = main_content.find_all(['ul', 'ol'])
#         for lst in lists:
#             items = lst.find_all('li')
#             for item in items:
#                 useful_content += "- " + item.get_text() + "\n"
#             useful_content += "\n"
#     return useful_content.strip()


def extract_useful_content(soup):
    useful_content = ""
    
    # Try finding main content in typical HTML tags
    main_content = (soup.find('main') or soup.find('article') or soup.find('div', role='main') or soup.find('body'))
    
    if main_content:
        # Extract paragraphs
        paragraphs = main_content.find_all('p')
        for p in paragraphs:
            useful_content += p.get_text() + "\n\n"
        
        # Extract list items (if any)
        lists = main_content.find_all(['ul', 'ol'])
        for lst in lists:
            items = lst.find_all('li')
            for item in items:
                useful_content += "- " + item.get_text() + "\n"
            useful_content += "\n"
    
    return useful_content.strip()
    # useful_content = ""
    # main_content = soup.find('div', {'id': 'mw-content-text'})
    # if main_content:
    #     # extracting content
    #     paragraphs = main_content.find_all('p')
    #     for p in paragraphs:
    #         useful_content += p.get_text() + "\n\n"
        
    #     lists = main_content.find_all(['ul', 'ol'])
    #     for lst in lists:
    #         items = lst.find_all('li')
    #         for item in items:
    #             useful_content += "- " + item.get_text() + "\n"
    #         useful_content += "\n"
    
    # return useful_content.strip()

def save_to_txt(data, filename='dataset.txt'):
    output_dir = "../scraped_data/"
    full_path = output_dir + filename
    with open(full_path, 'w', encoding='utf-8') as file:
        for item in data:
            file.write(item['url'] + "\n")
            file.write("="*50 + "\n")
            file.write(item['content'] + "\n\n")
            file.write("-"*50 + "\n\n")


def interact_with_ui(driver):
    # Example: Click on expand buttons
    try:
        expand_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'collapsible')))
        for button in expand_buttons:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)  # Wait for content to expand
    except TimeoutException:
        print("No expandable sections found")
    # try:
    #     expand_buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'mw-collapsible-toggle')))
    #     for button in expand_buttons:
    #         driver.execute_script("arguments[0].click();", button)
    #         time.sleep(5)  # Wait 
    # except TimeoutException:
    #     print("No expandable sections found")

def scrape_page(url, depth, keywords, url_queue):
    if url in visited_urls:
        return
    
    visited_urls.add(url)
    
    try:
        driver.get(url)
        time.sleep(2)  # Wait

        # UI
        interact_with_ui(driver)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = extract_useful_content(soup)
        print("reached content successfully")
        
        # Check for keywords and save to dataset
        if any(keyword.lower() in content.lower() for keyword in keywords):
            dataset.append({'url': url, 'content': content})
            for item in dataset:
                print(item['url'])
                print(item['content'])
                print("\n")
            
            # Storing relevant links
            for link in soup.find_all('a', href=True):
                link_url = urljoin(url, link['href'])
                if (urlparse(link_url).netloc == urlparse(url).netloc and link_url not in visited_urls and any(keyword.lower() in link.get_text().lower() for keyword in keywords)):
                    url_queue.append((link_url, depth + 1))
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None  # Return None in case of an error

# def main():
#     urls, keywords = query.main()
#     visited_urls = set()
#     max_depth = 3
#     url_queue = deque([(url, 0) for url in urls])

#     # Bfs
#     while url_queue and len(dataset) < 10:  # Limit to 10 pages 
#         current_url, depth = url_queue.popleft()
#         if depth <= max_depth:
#             scrape_page(current_url, depth, keywords, url_queue)

#     driver.quit()

#     filename = f"dataset_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#     save_to_txt(dataset, filename)

# if __name__ == "__main__":
#     main()
