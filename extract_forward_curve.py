'''

Script name: extract_forward_curve.py
Author: Marty Reider
Date: 5/8/22
Purpose: 
    1) Scrape Pensford for forward curve values
    2) Insert these values into SQLite db


'''


from bs4 import BeautifulSoup
import requests
import sqlite3
import datetime
from decimal import Decimal


## Scrape Pensford for monthly SOFR / LIBOR values

pensford_url = "https://www.pensford.com/resources/forward-curve"

result = requests.get(pensford_url)
soup = BeautifulSoup(result.text, "html.parser")
fwd_curve_tbl_raw = soup.find("table", id = "curve-table")

fwd_curve_tbl = []

## extract date / libor values from HTML text
for row in fwd_curve_tbl_raw.findAll("tr"):
    columns = row.findAll("td")

    ## filter out column header row
    if  columns[0].text.strip() != "Reset Date":
             
        ## format dates into yyyy-mm-dd
        date = datetime.datetime.strptime(columns[0].text.strip(), "%m/%d/%Y").strftime("%Y-%m-%d")
        
        ## convert SOFR value from percentage to decimal
        sofr = float(Decimal(columns[1].text.strip().replace("%", "")) * Decimal(".01"))
                
        ## convert LIBOR value from percentage to decimal
        libor = float(Decimal(columns[3].text.strip().replace("%", "")) * Decimal(".01"))

        fwd_curve_tbl.append([date, sofr, libor])
            
## Insert libor values into db

connection = sqlite3.connect('forward_curve.db')
cursor = connection.cursor()

## always drop and recreate table prior to adding new data
cmd_drop_tbl = 'DROP TABLE IF EXISTS forward_curve'
    
cmd_create_tbl = 'CREATE TABLE forward_curve(reset_date text, one_mo_sofr float, one_mo_libor float)'

cursor.execute(cmd_drop_tbl) 
cursor.execute(cmd_create_tbl) 
    
## insert records one at a time
for date, sofr_val, libor_val in fwd_curve_tbl:
    cmd_insert = """
        INSERT INTO forward_curve (reset_date, one_mo_sofr, one_mo_libor) 
        VALUES(\'""" + date + """\',  """ + str(sofr_val) + """, """ + str(libor_val) + """)
    """
    cursor.execute(cmd_insert) 
    
##delete later
cmd_query = """
    SELECT *
    FROM forward_curve
"""

connection.commit()
connection.close()



   
    