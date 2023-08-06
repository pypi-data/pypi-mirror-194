from datetime import date
from datetime import datetime as dt

# Create your views here.
from django.shortcuts import render

from .models import Finance, FinanceAccounting

# Create your views here.

def interest_amount(interest_type , margin , finance_amount , due_date):
    current_date = date.today()
    if interest_type == "Fixed":
        interest_rate = margin
    if interest_type == "floating":
        interest_rate = margin
    calculated_date = (dt.strptime(str(due_date), "%Y-%m-%d") - dt.strptime(str(current_date), "%Y-%m-%d")).days
    calculated_interest_amount = ((finance_amount)*(interest_rate)*( calculated_date / 365))
    return calculated_interest_amount


def FinanceModuleHandler(program_type , interest_paid_by , finance_req_id , finance_currency , finance_amount , interest_type):
    if program_type == "APF":
        if interest_paid_by == "own_party":
            FinanceAccounting.objects.create(
                contract_ref= finance_req_id,
                stage="financing",
                type = "D",
                currency=finance_currency,
                amount = finance_amount,
                account_type= "customer",
                base_ccy = "base_currency",
                base_ccy_amount = "",
                exch_rate = "",
            )
            FinanceAccounting.objects.create(
                contract_ref= finance_req_id,
                stage="financing",
                type = "C",
                currency=finance_currency,
                amount = finance_amount,
                account_type= "customer",
                base_ccy = "base_currency",
                base_ccy_amount = "",
                exch_rate = "",
            )
        if interest_paid_by == "counterparty":
            current_interest_amount = interest_amount(interest_type = interest_type)
            FinanceAccounting.objects.create(
                contract_ref= finance_req_id,
                stage="financing",
                type = "D",
                currency=finance_currency,
                amount = finance_amount ,
                account_type= "customer",
                base_ccy = "base_currency",
                base_ccy_amount = "",
                exch_rate = "",
            )
            FinanceAccounting.objects.create(
                contract_ref= finance_req_id,
                stage="financing",
                type = "C",
                currency=finance_currency,
                amount = finance_amount - current_interest_amount ,
                account_type= "customer",
                base_ccy = "base_currency",
                base_ccy_amount = "",
                exch_rate = "",
            )
        return None


