# master_server.py
import sys
print(sys.path)

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import httpx

# Importing necessary functions from scrapping_modules_init and nlp_backend
from Minor.NLP_backend.main import process_nlp
import parser

app = FastAPI()
cache = {}
class ScrapeRequest(BaseModel):
    query: str
    keywords: list
    columns_to_save: list
    
dummy_columns_to_save = [
        "Person",
        "Org",
        "Date",
        "Loc",
        "Misc",
        "Money",
        "Percent",
        "Time",
        "Quantity",
        "Ordinal",
        "Cardinal",
        "Product"
    ]

@app.post("/process")
async def process_request(request: ScrapeRequest):
            # Step 1: Call the scraper API and get filename of scraped data
    cache_key = (request.query, tuple(request.keywords))

        # Check if the result is already cached
    if cache_key in cache:
        print("Returning cached result for:", request)  # Log cache hit
        return cache[cache_key]  # Return cached result

    try:
        print("Received request:", request)  # Log the incoming request
            # Step 1: Call the scraper asynchronously and wait for the response
        url = "http://127.0.0.1:8001/scrape"
        data = {
                "query": request.query,
                "keyword": request.keywords
            }

        async with httpx.AsyncClient(timeout=None) as client:
            response = await client.post(url, json=data)
            print("Response from scraper:", response.status_code, response.text)  # Log the response

            # Step 2: Check if the request was successful
        print("here")
        if response.status_code == 200:
            scrape_result = response.json()  # Expecting a JSON response with a filename
            print("Scrape successful:", scrape_result)
        else:
            print("Error:", response.status_code, response.text)
            raise HTTPException(status_code=response.status_code, detail=response.text)
        print("here1")
        parser_instance = parser(request.keywords)
        parsed_file_path = parser_instance.parse_data(scrape_result['filename'])
        
        # Step 2: Process the scraped data with NLP model using returned filename
        svg_file, csv_file = process_nlp(parsed_file_path, request.columns_to_save)

        return {
            "message": "Processing completed successfully",
            "svg_file": svg_file,
            "csv_file": csv_file,
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/files/svg/{filename}")
async def get_svg_file(filename: str):
    file_path = f"relationships/{filename}"  # Adjust path as needed
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="SVG file not found")

@app.get("/files/csv/{filename}")
async def get_csv_file(filename: str):
    file_path = f"structured_data/{filename}"  # Adjust path as needed
    if os.path.exists(file_path):
        return FileResponse(file_path)
    raise HTTPException(status_code=404, detail="CSV file not found")