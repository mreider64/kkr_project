# KKR project README

# Overview:
extract_forward_curve.py: uses BeautifulSoup to scrape Pensford for the LIBOR & SOFR. Create new table and insert Pensford data into SQLite DB

payload_api.py: using FastAPI paired up with the uvicorn web server for the front-end, creates a REST endpoint to calculate payload via a POST request

# How to run:
Pip the relevant Python packages:
  - BeautifulSoup
  - requests
  - sqlite3
  - FastAPI
  - BaseModel
  - Uvicorn

Clone repo and cd into folder

Run extract_forward_curve.py to extract LIBOR & SOFR from Pensford and store it in a SQLite DB

Run 'uvicorn payload_api:app --reload' in the command line, and it should provide you the link to your localhost (e.g. http://127.0.0.1:8000)

Navigate to localhost/docs - from there, you should see payLoad API, where you can input the features of the loan and see the output below

# Time spent:
~5 hours

# Areas for improvement:
- Potentially replace FastAPI with a different backend (e.g. Flask) and customize the UI
- Add additional POST request to calculate total expected loan payment schedule in USD when you pass in property cost
- Add GET request to API to query the full Pensford extraction
- Add better error handling and validation of POST request inputs
