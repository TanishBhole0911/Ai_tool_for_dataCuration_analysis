# master_server.py
import sys
print(sys.path)

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

# Importing necessary functions from scrapping_modules_init and nlp_backend
from Scrapping_modules_init.main import scrape as scrape_pages
from Minor.NLP_backend.main import process_nlp
import parser

app = FastAPI()

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
    try:
        # Step 1: Call the scraper and get filename of scraped data
        scrape_result = scrape_pages(request)
        
        parser_instance = parser.parser(request.keywords)
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