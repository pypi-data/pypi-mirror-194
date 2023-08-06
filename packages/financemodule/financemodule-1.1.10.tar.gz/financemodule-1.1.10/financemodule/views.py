from datetime import date
from datetime import datetime as dt

from financemodule.models import Finance , FinanceAccounting , Exchangerate
from .enum import Partytype , ProgramType , FinancingStage , CustomerType , Accounttype


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
    calculated_date = (dt.strptime(str(due_date), "%Y-%m-%d")- dt.strptime(str(current_date), "%Y-%m-%d")).days
    interest_amount = (finance_amount) * (interest_rate) * (calculated_date / 365)
    return interest_amount, interest_rate


def FinanceModuleHandler(
    program_type,
    margin,
    interest_paid_by,
    finance_req_id,
    finance_currency,
    base_currency,
    account_number_1,
    account_number_2,
    finance_amount,
    interest_type,due_date
):
    current_interest_amount = calculated_interest_amount(interest_type, margin, finance_amount, due_date)
    calculated_amount = finance_amount - current_interest_amount
    exchange_rate_queryset = Exchangerate.objects.get(rate_currency=finance_currency)
    if program_type == ProgramType.APF.value:
        if interest_paid_by == Partytype.ownparty.value:

            FinanceAccounting.objects.bulk_create([
        
            # type DEBIT 
            FinanceAccounting(contract_ref = finance_req_id, stage = FinancingStage.Financing.value ,
            type =  Accounttype.DEBIT.value , currency=finance_currency,amount=finance_amount , account = account_number_1 , 
            account_type= CustomerType.customer.value,base_currency= base_currency ,
            base_currency_amount= finance_amount * exchange_rate_queryset.rate_mid,
            exch_rate = exchange_rate_queryset.rate_mid),

            # type CREDIT
            FinanceAccounting(contract_ref = finance_req_id, stage = FinancingStage.Financing.value,
            type = Accounttype.CREDIT.value , currency=finance_currency,amount= finance_amount, account = account_number_2 , 
            account_type= CustomerType.customer.value,base_currency= base_currency ,
            base_currency_amount= finance_amount * exchange_rate_queryset.rate_mid,
            exch_rate = exchange_rate_queryset.rate_mid),
            ])

        if interest_paid_by == Partytype.counterparty.value:
        
            FinanceAccounting.objects.bulk_create([
        
            # type DEBIT 
            FinanceAccounting(contract_ref = finance_req_id, stage = FinancingStage.Financing.value , 
            type =  Accounttype.DEBIT.value  , currency=finance_currency,amount=finance_amount , account = account_number_1 , 
            account_type= CustomerType.customer.value,base_currency= base_currency ,
            base_currency_amount= finance_amount * exchange_rate_queryset.rate_mid,
            exch_rate = exchange_rate_queryset.rate_mid),

            # type CREDIT
            FinanceAccounting(contract_ref = finance_req_id, stage = FinancingStage.Financing.value,
            type =  Accounttype.CREDIT.value  , currency=finance_currency,amount= calculated_amount, account = account_number_2 , 
            account_type= CustomerType.customer.value,base_currency= base_currency ,
            base_currency_amount= calculated_amount * exchange_rate_queryset.rate_mid,
            exch_rate = exchange_rate_queryset.rate_mid),
            ])

        return current_interest_amount
    else:
        raise ValueError("program type should be APF, RF , DF")