import datetime
import numpy_financial as npf
from dateutil.relativedelta import relativedelta

decimal_places=2


def generate_payment_schedule(initial_payment, lease_term, annual_escalation_rate,commencement_date):
    monthly_payment = initial_payment
    payment_schedule = []
    total_monthly_payments = 0
    

    for period in range(0, lease_term):
        period_start_date = commencement_date + relativedelta(months=period)
        period_start_date = period_start_date.replace(day=min(commencement_date.day, period_start_date.day))
        total_monthly_payments += monthly_payment
        payment_schedule.append((period + 1, period_start_date, round(monthly_payment, 2)))

        if (period + 1) % 12 == 0:
            monthly_payment *= (1 + annual_escalation_rate / 100)

    return payment_schedule, total_monthly_payments

def calculate_single_lease_expense(prepaid_lease_payment, initial_direct_costs, lease_incentives, total_monthly_payments, lease_term):
    single_lease_expense = (prepaid_lease_payment + initial_direct_costs - lease_incentives + total_monthly_payments) / lease_term
    return single_lease_expense

def calculate_initial_lease_liability(payment_schedule, discount_rate):


    payments =[0]+ [payment for _, _, payment in payment_schedule]
    initial_lease_liability = npf.npv(discount_rate / 12, payments)
    #For Beginning of the period
    # payments =[0]+ [payment for _, _, payment in payment_schedule][1:0]
    # initial_lease_liability = npf.npv(discount_rate / 12, payments)+payment_schedule[0][2]


    return initial_lease_liability
    
 

def calculate_interest_assertion_lease_liability(initial_lease_liability,payment_Schedule,incremental_borrowing_rate):

    interest_assertion=(initial_lease_liability)*(incremental_borrowing_rate/12)
    principal_allocation=(payment_Schedule[0][2]-interest_assertion)
    #for beginning of the period
#   interest_assertion=(initial_lease_liability-payment_Schedule[0][2])*(incremental_borrowing_rate/12)

    lease_liability_balance=initial_lease_liability-payment_Schedule[0][2]+interest_assertion

    interest_assertion_values=[interest_assertion]
    lease_liability_balance_values=[lease_liability_balance]
    principal_allocation_values=[principal_allocation]


    for _,_,payment in payment_Schedule[1:]:

        interest_assertion=(lease_liability_balance)*(incremental_borrowing_rate/12)
        #for beginning of the period
        # interest_assertion=(lease_liability_balance-payment)*(incremental_borrowing_rate/12)
        interest_assertion_values.append(round(interest_assertion,decimal_places))
        principal_allocation_values.append(round(payment-interest_assertion,decimal_places))

        lease_liability_balance=lease_liability_balance-payment+interest_assertion
        lease_liability_balance_values.append(round(lease_liability_balance,decimal_places))

    return interest_assertion_values,lease_liability_balance_values,principal_allocation_values

def calculate_right_of_use_asset_balance(initial_lease_liability,prepaid_lease_payment,initial_direct_costs,lease_incentives):
    return initial_lease_liability+prepaid_lease_payment+initial_direct_costs-lease_incentives

def ROU_accum_amort(right_of_use_asset_balance,single_lease_expense,principle_allocation,payment_schedule):

    rou_accum_amort=single_lease_expense+principle_allocation[0]-payment_schedule[0][2]
    right_of_use_asset_balance=right_of_use_asset_balance-rou_accum_amort

    rou_accum_amort_values=[rou_accum_amort]
    right_of_use_asset_balance_values=[right_of_use_asset_balance]

    for (_,_,payment),principle in zip(payment_schedule[1:],principle_allocation[1:]):
        rou_accum_amort=single_lease_expense+principle-payment

        rou_accum_amort_values.append(round(rou_accum_amort,decimal_places))

        right_of_use_asset_balance=right_of_use_asset_balance-rou_accum_amort

        right_of_use_asset_balance_values.append(round(right_of_use_asset_balance,decimal_places))

    return rou_accum_amort_values,right_of_use_asset_balance_values




