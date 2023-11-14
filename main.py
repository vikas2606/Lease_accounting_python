import datetime
import pandas as pd
from lease_calculator import generate_payment_schedule, calculate_single_lease_expense, calculate_initial_lease_liability,calculate_interest_assertion_lease_liability,calculate_right_of_use_asset_balance,ROU_accum_amort

# Dummy data
initial_payment = 410000
lease_term = 63
annual_escalation_rate = 3
prepaid_lease_payment = 0
initial_direct_costs = 0
lease_incentives = 0
incremental_borrowing_rate = 0.09
##YYYY:MM:DD
commencement_date=datetime.date(2019,4,1)


payment_schedule, total_monthly_payments = generate_payment_schedule(initial_payment, lease_term, annual_escalation_rate,commencement_date)
single_lease_expense = calculate_single_lease_expense(prepaid_lease_payment, initial_direct_costs, lease_incentives, total_monthly_payments, lease_term)
initial_lease_liability = calculate_initial_lease_liability(payment_schedule,incremental_borrowing_rate)
interest_assertion_values,lease_liability_balance_values,principle_allocation_values=calculate_interest_assertion_lease_liability(initial_lease_liability,payment_schedule,incremental_borrowing_rate)
right_of_use_asset_balance=calculate_right_of_use_asset_balance(initial_lease_liability,prepaid_lease_payment,initial_direct_costs,lease_incentives)
rou_accum_amort_values,right_of_use_asset_balance_values=ROU_accum_amort(right_of_use_asset_balance,single_lease_expense,principle_allocation_values,payment_schedule)

excel_file_path = 'payment_schedule.xlsx'
df = pd.DataFrame(payment_schedule, columns=['Period Number', 'Period Start Date', "Month's Payment"])
df["Single Lease Expense"] = single_lease_expense
df["Interest Assertion"]=interest_assertion_values
df["Principal Allocation Values"]=principle_allocation_values
df["Lease Liability Balance"]=lease_liability_balance_values
df["Right of use Asset Balance"]=right_of_use_asset_balance_values
df["ROU Accum Amort"]=rou_accum_amort_values

df.to_excel(excel_file_path, index=False)

print(f"Payment schedule saved to {excel_file_path}")
print(f"Initial Lease Liability Balance: {initial_lease_liability:.2f}")
print(f"Right to use asset balance:{right_of_use_asset_balance:.2f}")
