'''

Script name: payload_api.py
Author: Marty Reider
Date: 5/8/22
Purpose: 
        
    Create REST API for the payout of a loan based on the combination of 
    the Pensford rates & user inputted information


'''

from fastapi import FastAPI
from pydantic import BaseModel
from decimal import Decimal
import sqlite3

class Loan(BaseModel):
    maturity_date   : str
    reference_rate  : str
    rate_floor      : float
    rate_ceiling    : float
    rate_spread     : float

app = FastAPI()


@app.post("/payload")
def calculate_interest_rate(loan: Loan):
    ## validate that reference rate
    if loan.reference_rate.upper() not in ("LIBOR", "SOFR"):
        return {"Error": "Reference rate not either LIBOR or SOFR"}
    
    connection = sqlite3.connect('forward_curve.db')
    cursor = connection.cursor()
    
    cmd_query = """
        SELECT 
              reset_date
            , CASE
                WHEN \'""" + loan.reference_rate.upper() + """\' = 'SOFR' THEN one_mo_sofr
                ELSE one_mo_libor
              END AS rate
        FROM forward_curve
        WHERE reset_date <= \'""" + loan.maturity_date + """\'
        ORDER By reset_date ASC
    """
    forward_curve = cursor.execute(cmd_query).fetchall()

    payload = []
    
    for reset_date, rate in forward_curve:
        ## manipulate rates with str and Decimal to avoid rounding precision errors
        rate    = Decimal(str(rate))
        spread  = Decimal(str(loan.rate_spread))
        floor   = Decimal(str(loan.rate_floor))
        ceiling = Decimal(str(loan.rate_ceiling))
                         
        rate_final = float(max(min(rate + spread, ceiling), floor))

        payload.append({  "date" : reset_date, "rate" : rate_final})
    
    return payload
    
    
    
    
    
    


