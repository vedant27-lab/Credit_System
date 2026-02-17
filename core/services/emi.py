def calculate_emi(P, annual_rate, tenure_months):
    r=(annual_rate/100)/12
    n=tenure_months

    emi = (P*r*(1+r)**n)/((1+r)**n-1)
    return round(emi, 2)


