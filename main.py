import argparse
import math

parser = argparse.ArgumentParser(description="Loan Calculator")

parser.add_argument("--type", choices=["annuity", "diff"])
parser.add_argument("--principal")
parser.add_argument("--periods")
parser.add_argument("--interest")
parser.add_argument("--payment")

args = parser.parse_args()

args = {"type": args.type, "principal": args.principal, "periods": args.periods, "interest": args.interest, "payment": args.payment}

def is_float_val(y):
    if isinstance(y, list):
        try:
            [float(y) for y in y]
            return True
        except ValueError:
            return False
    else:
        try:
            float(y)
            return True
        except ValueError:
            return False

def annuity_validation(x):
    if not x.get("interest") and (x.get("interest") is None or not is_float_val(x.get("interest"))):
        print("Incorrect parameters")
        return False
    else:
        flag = []
        if not x.get("principal") or not is_float_val(x.get("principal")):
            flag.append("p")
        if not x.get("periods") or not is_float_val(x.get("periods")):
            flag.append("n")
        if not x.get("payment") or not is_float_val(x.get("payment")):
            flag.append("a")
        # print(flag)
        if len(flag) == 1:
            x["flag"] = flag[0]
            return x
        else:
            print("Incorrect parameters")
            return False

def diff_validation(x):
    if x.get("payment") or (x.get("principal") is None or x.get("periods") is None or x.get("interest") is None):
        print("Incorrect parameters")
        return False
    elif not is_float_val([x.get("principal"), x.get("periods"), x.get("interest")]):
        print("Incorrect parameters")
        return False
    else:
        x["flag"] = "d"
        return x

def full_validation(x):
    if x.get("type") == "diff":
        return diff_validation(x)
    elif x.get("type") == "annuity":
        return annuity_validation(x)
    else:
        print("Incorrect parameters")
        return False


if full_validation(args):
    question = args["flag"]

    if question == "d":
        full_sum = 0

        loan_principal = float(args["principal"])
        interest_rate = float(args["interest"]) / 100 / 12
        num_of_periods = int(args["periods"])

        for m in range(1, num_of_periods + 1):
            x = loan_principal / num_of_periods + interest_rate * (loan_principal - (loan_principal * (m - 1)) / num_of_periods)
            print(f"Month {m}: payment is {math.ceil(x)}")
            full_sum += math.ceil(x)

        print(f"\nOverpayment = {int(full_sum - loan_principal)}")

    elif question == "n":
        # number of monthly payments
        loan_principal = float(args["principal"])
        monthly_payment = int(args["payment"])
        interest_rate = float(args["interest"]) / 100 / 12

        num_of_months = math.ceil(
            math.log(monthly_payment / (monthly_payment - interest_rate * loan_principal), 1 + interest_rate))

        years_to_pay = num_of_months // 12
        months_to_pay = num_of_months % 12

        result = "It will take "
        if years_to_pay:
            if years_to_pay == 1:
                result += "1 year "
            else:
                result += f"{years_to_pay} years "

        if years_to_pay and months_to_pay:
            result += "and "

        if months_to_pay:
            if months_to_pay == 1:
                result += "1 month "
            else:
                result += f"{months_to_pay} months "

        result += "to repay this loan!"
        print(result)
        print(f"Overpayment = {int(monthly_payment * num_of_months - loan_principal)}")
    elif question == "a":

        loan_principal = float(args["principal"])
        interest_rate = float(args["interest"]) / 100 / 12
        num_of_periods = int(args["periods"])

        monthly_payment = loan_principal \
                          * ((interest_rate * (1 + interest_rate) ** num_of_periods) / ((1 + interest_rate) ** num_of_periods - 1))

        print(f"Your annuity payment = {math.ceil(monthly_payment)}!")
        print(f"Overpayment = {int(math.ceil(monthly_payment) * num_of_periods - loan_principal)}")

    elif question == "p":
        annuity = float(args["payment"])
        num_of_periods = int(args["periods"])
        interest_rate = float(args["interest"]) / 100 / 12

        loan_principal = annuity \
                         / ((interest_rate * (1 + interest_rate) ** num_of_periods) / (((1 + interest_rate) ** num_of_periods) - 1))
        print(f"Your loan principal = {int(loan_principal)}!")
        print(f"Overpayment = {int(annuity * num_of_periods - int(loan_principal))}!")
