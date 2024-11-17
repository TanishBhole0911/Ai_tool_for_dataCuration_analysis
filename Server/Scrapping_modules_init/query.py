from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
chromeOptions = Options()
chromeOptions.headless = True

service = Service("./chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service=service, options=chromeOptions)

# Google search
def google_search(query, keywords):
    search_query = f"{query} {' '.join([f'[{keyword}]' for keyword in keywords])}"
    driver.get("https://www.google.com")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(search_query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3) 

    search_results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
    urls = []
    for index, result in enumerate(search_results[:5]):  #first 5 for eg
        link = result.find_element(By.TAG_NAME, 'a')
        url = link.get_attribute("href")
        urls.append(url)
        print(f"Result {index + 1}: {result.text}")
        print(f"URL: {url}\n")

    return urls

def get_user_input(q):
    query = input("Enter your query: ")
    keywords = []
    for i in range(4):
        keyword = input(f"Enter keyword {i+1}: ")
        keywords.append(keyword)
    q.put((query, keywords))

# def main():
#     q = queue.Queue()
#     # Create a new thread to get the user input
#     input_thread = threading.Thread(target=get_user_input, args=(q,))
#     input_thread.start()
#     input_thread.join()
#     query, keywords = q.get()
#     urls = google_search(query, keywords)
#     return urls, keywords

# if __name__ == "__main__":
#     main()