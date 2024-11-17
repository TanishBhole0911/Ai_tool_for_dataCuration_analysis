# scrapping_modules_init/main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from collections import deque
import datetime
from query import google_search  # Import the google_search function
from scrapper import scrape_page, save_to_txt, dataset, visited_urls  # Import necessary functions and variables

# Ensure the app instance is correctly defined
app = FastAPI()

# Define request body model for scraping
class ScrapeRequest(BaseModel):
    query: str  # Search query
    keyword: list  # Keywords for scraping

cache = {}

@app.post("/scrape")  # /scrape endpoint define karna
def scrape(request: ScrapeRequest):
    cache_key = (request.query, tuple(request.keyword))
    if cache_key in cache:
        return {"message": "Scraping completed (from cache)", "filename": cache[cache_key]}
    
    visited_urls.clear()  # Clear visited URLs for each request
    dataset.clear()  # Clear dataset for each request
    max_depth = 3
    google_links = google_search(request.query, request.keyword)  # Search for Google links
    print("Query searched")
    url_queue = deque([(link, 0) for link in google_links])  # Add Google links to the queue

    while url_queue and len(dataset) < 10:  # Limit to 10 pages 
        current_url, depth = url_queue.popleft()
        if depth <= max_depth:
            scrape_page(current_url, depth, request.keyword, url_queue)  # Use the keyword

    filename = f"dataset_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    save_to_txt(dataset, filename)
    cache[cache_key] = filename
    return {"message": "Scraping completed", "filename": filename}

# # Main.py

# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List
# from scrapper import scrape_page, save_to_txt, dataset, visited_urls  # Import necessary functions and variables
# from collections import deque
# import datetime
# from query import google_search  # Import the google_search function
# from minor.nlp_backend.tet_processing import process_text  # Import the NLP processing function

# app = FastAPI()

# # Define request body model for scraping
# class ScrapeRequest(BaseModel):
#     query: str  # Search query
#     keyword: list  # Keywords for scraping

# # Define request body model for NLP
# class NLPRequest(BaseModel):
#     text: str  # The text to be processed

# @app.post("/scrape")
# def scrape(request: ScrapeRequest):
#     visited_urls.clear()  # Clear visited URLs for each request
#     max_depth = 3
#     google_links = google_search(request.query, request.keyword)  # Search for Google links
#     print("Query searched")
#     url_queue = deque([(link, 0) for link in google_links])  # Add Google links to the queue

#     while url_queue and len(dataset) < 10:  # Limit to 10 pages 
#         current_url, depth = url_queue.popleft()
#         if depth <= max_depth:
#             scrape_page(current_url, depth, request.keyword, url_queue)  # Use the keyword

#     filename = f"dataset_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
#     save_to_txt(dataset, filename)
    
#     return {"message": "Scraping completed", "filename": filename}

# @app.post("/nlp")
# def nlp(request: NLPRequest):
#     processed_data = process_text(request.text)  # Process the text with NLP
#     return {"message": "NLP processing completed", "data": processed_data}

# # API call example:


# # # Main.py

# # from fastapi import FastAPI
# # from pydantic import BaseModel
# # from typing import List
# # from scrapper import scrape_page, save_to_txt, dataset, visited_urls  # Import necessary functions and variables
# # from collections import deque
# # import datetime
# # from query import google_search  # Import the google_search function

# # app = FastAPI()

# # # Define request body model
# # class ScrapeRequest(BaseModel):
# #     query: str  # Change from List[str] to str
# #     keyword: list  # Change from List[str] to str

# # @app.post("/scrape")
# # def scrape(request: ScrapeRequest):
# #     visited_urls.clear()  # Clear visited URLs for each request
# #     max_depth = 3
# #     # url_queue ko sirf google_links se initialize karna hai
# #     google_links = google_search(request.query, request.keyword)  # Pass an empty list for keywords
# #     print("Query searched")
# #     url_queue = deque([(link, 0) for link in google_links])  # Google links ko queue mein add karo

# #     while url_queue and len(dataset) < 10:  # Limit to 10 pages 
# #         current_url, depth = url_queue.popleft()
# #         if depth <= max_depth:
# #             scrape_page(current_url, depth, request.keyword, url_queue)  # Use the single keyword

# #     filename = f"dataset_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
# #     save_to_txt(dataset, filename)
    
# #     return {"message": "Scraping completed", "filename": filename}
# #     # return {"message":"Query searched","url": url_queue}
# # # API call example:
# # # POST request to /scrape/ with body:
# # # {
# # #     "query": ["http://example.com"],
# # #     "keywords": ["keyword1", "keyword2"]
# # # }
    # return {"message":"Query searched","url": url_queue}
# API call example:
# POST request to /scrape with body:
# {
#     "query": ["Maruti Suzuki"],
#     "keywords": ["keyword1", "keyword2"]
# }
