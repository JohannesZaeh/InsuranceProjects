import sys
import os
import numpy as np

from utils import read_input
from utils import write_output
from utils import load_fund
from utils import threeD_plot
from utils import twoD_plot

from functions import pure_fund_single_premium
from functions import pure_fund_regular_premium
from functions import static_hybrid_single_premium
from functions import dynamic_hybrid_single_premium

directory = sys.argv[1].replace("\\", "/")
directory = directory[:-1]
input_directory = directory + "/input"

base_input = read_input(input_directory + "/fund_timelapse_input.txt")

locals().update(base_input)

if isinstance(fund, str):
    fund_constant = False
else:
    constant_increment = fund
    fund_constant = True

start_years = [str(1972 + i) for i in range(0,int(2024-1972-maturity/12))]
months = ["01","02","03","04","05","06","07","08","09","10","11","12"]

result = []
start_dates = []

fund_id = fund


for i,year in enumerate(start_years):
    for m,month in enumerate(months):

        start_date = month + "/01/" + year
        start_dates.append(int(year) + m/12)

        # check if it should load a specific fund from /resources, otherwise turn constant fund into list.
        if fund_constant == False:
            path_fund = directory + "/resources/" + fund_id + ".txt"
            fund = load_fund(path_fund, start_date, int(maturity))
        else:
            fund = int(maturity) * [(1 + constant_increment) ** (1 / 12)]

        match contract_type:
            case "pure_fund_single_premium":
                account = pure_fund_single_premium(premium, fund, regular_charges, alpha, beta, gamma, maturity)
            case "pure_fund_regular_premium":
                life_table_path = directory + "/resources/" + life_table + ".txt"
                account = pure_fund_regular_premium(premium, fund, regular_charges, alpha, beta, gamma, maturity, age, life_table_path)                                  
            case "static_hybrid_single_premium":
                account = static_hybrid_single_premium(premium, guaranteed_benefit, worst_case, guaranteed_interest, real_interest, fund, regular_charges, alpha, beta, maturity)
            case "dynamic_hybrid_single_premium":
                account = dynamic_hybrid_single_premium(premium, guaranteed_benefit, worst_case, guaranteed_interest, real_interest, fund, regular_charges, alpha, beta, maturity)
    
        result.append(account)

x = np.array(result[0]["t"])
y = np.array(start_dates)
z = []
for i,date in enumerate(start_dates):
    z.append(result[i]["total"])
z = np.array(z)

benefits = np.array([result[i]["benefit_at_maturity"] for i in range(len(start_dates))])

threeD_plot(x,y,z)

'''
irrs = np.array([result[i]["irr"] for i in range(len(start_dates))])
print(np.mean(irrs))
print(f"irr standard deviation: {np.std(irrs)}")
print(min(irrs))
print(max(irrs))
twoD_plot(y,irrs)
'''

twoD_plot(y,benefits)





