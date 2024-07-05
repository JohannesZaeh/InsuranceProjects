# Johannes Zaeh, 26.05.2024
import math
import sys
import numpy_financial as npf
from utils import load_life_table

'''
Here are all the mathematical functions needed to calculate static/dynamic hybrid products.
'''

'''
Function to calculate the present value of the guaranteed benefit, given the guaranteed interest rate, regular charges and the timespan.
'''


def calculate_pv(guaranteed_benefit, guaranteed_interest_monthly, regular_charges, steps):
    pv = guaranteed_benefit

    # determine present value by starting with guaranteed benefit and going back.
    # only go back maturity-1 steps because you need the present value after one step from your current point.
    for t in range(steps - 1):
        pv = pv / guaranteed_interest_monthly + regular_charges

    return pv


'''
Function to calculate the ratio of how much can be put in the fund at any given point in time. 
Calculate s.t. when the fund performs worst case over one period, investing the rest at the guaranteed interest will still
give the guaranteed benefit, with regular charges considered.
'''


def calculate_split(total_account, guaranteed_benefit, steps, worst_case, guaranteed_interest_monthly, regular_charges):
    # determine present value of guarantee one step ahead
    pv = calculate_pv(guaranteed_benefit, guaranteed_interest_monthly, regular_charges, steps)

    # determine how much can be put in the fund
    fund_part = min((total_account - pv) / worst_case, total_account)

    # determine the ratio
    trad_part = total_account - fund_part

    return [trad_part, fund_part]


'''
Calculate IRR for single premium
'''


def calculate_irr(benefit, single_premium, maturity):
    years = int(maturity / 12)

    # use formula for single premium
    irr = (benefit / single_premium) ** (1 / years) - 1

    return irr


def calulate_irr_regular_premium(benefit, premium, maturity):
    cashflows = []

    for t in range(int(maturity)):
        cashflows.append(premium)

    cashflows.append(-benefit)

    irr = npf.irr(cashflows)

    irr = (1 + irr) ** 12

    irr = irr - 1

    return irr


'''
Calculate complete evolution of a hyrid product given the input parameters. 
'''


def run_hybrid(single_premium, guaranteed_benefit, worst_case, guaranteed_interest, real_interest, fund,
               regular_charges, alpha, beta, maturity, type):
    T = int(maturity)
    guaranteed_interest_monthly = (1 + guaranteed_interest) ** (1 / 12)
    real_interest_monthly = (1 + real_interest) ** (1 / 12)

    Account = {"t": [0], "traditional_part": [],
               "fund_part": [], "total": []}

    savings_premium = (1 - (alpha + beta)) * single_premium
    Account["total"].append(savings_premium)

    guaranteed_benefit_nominal = guaranteed_benefit * single_premium

    if type == "static_hybrid":
        # calculate pv for T+1 because the calculate_pv method substracts one step as is needed usually for the dynamic part
        pv = calculate_pv(guaranteed_benefit_nominal, guaranteed_interest_monthly, regular_charges, T + 1)
        Account["traditional_part"].append(pv)
        Account["fund_part"].append(savings_premium - pv)

    elif type == "dynamic_hybrid":
        split = calculate_split(savings_premium, guaranteed_benefit_nominal, T, worst_case,
                                guaranteed_interest_monthly,
                                regular_charges)

        Account["traditional_part"].append(split[0])
        Account["fund_part"].append(split[1])
    else:
        print("invalid product type")
        sys.exit()

    for t in range(1, T + 1):

        traditional_part_new = (Account["traditional_part"][t - 1] - regular_charges) * real_interest_monthly
        fund_part_new = Account["fund_part"][t - 1] * fund[t - 1]
        new_total = traditional_part_new + fund_part_new

        if type == "dynamic_hybrid":
            [traditional_part_new, fund_part_new] = calculate_split(new_total, guaranteed_benefit_nominal, T - t,
                                                                    worst_case,
                                                                    guaranteed_interest_monthly,
                                                                    regular_charges)

        Account["t"].append(t)
        Account["traditional_part"].append(traditional_part_new)
        Account["fund_part"].append(fund_part_new)
        Account["total"].append(new_total)

    Account["benefit_at_maturity"] = Account["total"][-1]

    irr = calculate_irr(Account["total"][-1], single_premium, maturity)
    Account["irr"] = irr

    return Account


def pure_fund_single_premium(premium, fund, regular_charges, alpha, beta, gamma, maturity):
    T = int(maturity)

    Account = {"t": [0], "traditional_part": [],
               "fund_part": [], "total": []}

    savings_premium = (1 - (alpha + beta)) * premium
    Account["total"].append(savings_premium)

    Account["traditional_part"].append(0)
    Account["fund_part"].append(savings_premium)

    for t in range(1, T + 1):
        fund_part_new = (Account["fund_part"][t - 1] - regular_charges) * (1 - gamma) ** (1 / 12) * fund[t - 1]
        new_total = fund_part_new

        Account["t"].append(t)
        Account["traditional_part"].append(0)
        Account["fund_part"].append(fund_part_new)
        Account["total"].append(new_total)

    Account["benefit_at_maturity"] = Account["total"][-1]
    irr = calculate_irr(Account["total"][-1], premium, maturity)
    Account["irr"] = irr

    return Account


def pure_fund_regular_premium(premium, fund, regular_charges, alpha, beta, gamma, maturity, age, life_table_path):
    T = int(maturity)

    Account = {"t": [0], "traditional_part": [0],
               "fund_part": [0], "total": [0]}

    sum_gross_premiums = T * premium * 0.5
    qx = load_life_table(life_table_path)
    current_age = int(age)

    alpha_distributed = (alpha * premium * T) / 60

    for t in range(1, T + 1):
        if t < 61:
            fund_part_new = (Account["fund_part"][t - 1] + premium * (
                    1 - beta) - alpha_distributed - regular_charges) * (1 - gamma) ** (1 / 12)
        else:
            fund_part_new = (Account["fund_part"][t - 1] + premium * (1 - beta) - regular_charges) * (1 - gamma) ** (
                    1 / 12)

        death_benefit = max(sum_gross_premiums, fund_part_new)
        risk_premium = (death_benefit - fund_part_new) * qx[current_age] * (1 / (12 - qx[current_age]))

        fund_part_new = (fund_part_new - risk_premium) * fund[t - 1]

        new_total = fund_part_new

        if t % 12 == 0:
            current_age += 1

        Account["t"].append(t)
        Account["traditional_part"].append(0)
        Account["fund_part"].append(fund_part_new)
        Account["total"].append(new_total)

    Account["benefit_at_maturity"] = Account["total"][-1]
    #irr = calulate_irr_regular_premium(Account["benefit_at_maturity"], premium, maturity)
    #Account["irr"] = irr
    # riy = calculate_riy(account, premium, maturity, alpha, beta, gamma, regular_charges, product_type)

    return Account
