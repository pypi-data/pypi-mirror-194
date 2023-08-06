from datetime import date
from datetime import datetime as dt

# Create your views here.
from django.shortcuts import render

from .models import Finance, FinanceAccounting


def process(request):
    return (
        request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", ""))
        .split(",")[0]
        .strip()
    )


# Create your views here.


def calculated_interest_amount(interest_type, margin, finance_amount, due_date):
    current_date = date.today()
    if interest_type == "FIXED":
        interest_rate = margin
    if interest_type == "FLOATING":
        interest_rate = 90 + int(margin)
    calculated_date = (
        dt.strptime(str(due_date), "%Y-%m-%d")
        - dt.strptime(str(current_date), "%Y-%m-%d")
    ).days
    interest_amount = (finance_amount) * (interest_rate) * (calculated_date / 365)
    return interest_amount, interest_rate


def FinanceModuleHandler(
    program_type,
    margin,
    interest_paid_by,
    finance_req_id,
    finance_currency,
    finance_amount,
    interest_type,
    due_date,
):
    if program_type == "APF":
        if interest_paid_by == "own_party":
            FinanceAccounting.objects.create(
                contract_ref=finance_req_id,
                stage="financing",
                type="D",
                currency=finance_currency,
                amount=finance_amount,
                account_type="customer",
                base_currency="base_currency",
                base_currency_amount="",
                exch_rate="",
            )
            FinanceAccounting.objects.create(
                contract_ref=finance_req_id,
                stage="financing",
                type="C",
                currency=finance_currency,
                amount=finance_amount,
                account_type="customer",
                base_currency="base_currency",
                base_currency_amount="",
                exch_rate="",
            )
        if interest_paid_by == "counterparty":
            current_interest_amount = calculated_interest_amount(
                interest_type, margin, finance_amount, due_date
            )
            FinanceAccounting.objects.create(
                contract_ref=finance_req_id,
                stage="financing",
                type="D",
                currency=finance_currency,
                amount=finance_amount,
                account_type="customer",
                base_currency="base_currency",
                base_currency_amount="",
                exch_rate="",
            )
            FinanceAccounting.objects.create(
                contract_ref=finance_req_id,
                stage="financing",
                type="C",
                currency=finance_currency,
                amount=finance_amount - current_interest_amount,
                account_type="customer",
                base_currency="base_currency",
                base_currency_amount="",
                exch_rate="",
            )
        return current_interest_amount
