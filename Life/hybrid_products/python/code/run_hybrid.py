# Johannes Zaeh, 26.05.2024
import sys
import os
from utils import read_input
from utils import write_output
from utils import load_fund
from functions import run_hybrid
from functions import pure_fund_single_premium
from functions import pure_fund_regular_premium

'''
Script to calculate a hybrid product according to parameters specified in text files in the /input folder.
This script needs to be run with the .cmd files in the main folder, because it will automatically set the right paths.
This way, the whole project is contained within a single folder and can be run anywhere without problems.
'''
directory = sys.argv[1].replace("\\", "/")
directory = directory[:-1]

input_directory = directory + "/input"
output_directory = directory + "/output"

input_files = os.listdir(input_directory)

batch_size = len(input_files)

# For every text file in the input folder:
for i, file in enumerate(input_files):

    print(f"Calculating: {i + 1}/{batch_size}")
    # load data from input file
    input_path = input_directory + "/" + file
    input = read_input(input_path)
    locals().update(input)

    # input parameters should also be in the output file for better readability
    output = input
    output.update({"type": contract_type})

    # check if it should load a specific fund from /resources, otherwise turn constant fund into list.
    if isinstance(fund,str):
        path_fund = directory + "/resources/" + fund + ".txt"
        fund = load_fund(path_fund, start_date, int(maturity))
    else:
        fund = int(maturity) * [(1 + fund) ** (1 / 12)]

    # Calculate results
    if contract_type == "pure_fund_single_premium":
        account = pure_fund_single_premium(premium, fund, regular_charges, alpha, beta, gamma, maturity)
    elif contract_type == "pure_fund_regular_premium":
        life_table_path = directory + "/resources/" + life_table + ".txt"
        account = pure_fund_regular_premium(premium, fund, regular_charges, alpha, beta, gamma, maturity, age,
                                            life_table_path)
    else:
        account = run_hybrid(single_premium, guaranteed_benefit, worst_case, guaranteed_interest, real_interest,
                         fund, regular_charges, alpha, beta, maturity, contract_type)

    # add results to output
    output.update(account)

    # write results to text file in /output folder
    output_path = output_directory + "/" + file[:-4] + "_output.txt"
    write_output(output_path, output)

print("Done!")
