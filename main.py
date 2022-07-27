import os
import pandas as pd
from requests import session
from requests_html import HTMLSession

class GraphNode:
    def __init__(self, company_name, cash_account, limit, edges) -> None:
        self.company_name = company_name
        self.cash_account = cash_account
        self.limit = limit
        self.is_rus = False
        self.edges = edges
        
    def money_to_transfer(self):
        if (self.money > self.limit):
            return self.money-self.limit
        return 0

class CashAccount:
    def __init__(self, name, currency, money) -> None:
        self.name = name
        self.currency = currency
        self.money = money

def сurrency_сonversion() -> list:
    session = HTMLSession()
    r = session.get("https://www.profinance.ru/quotes/")
    r.html.render(timeout=10.0)

    print(r.html.find("#USDRUB > .quote__row__cell.quote__row__cell.quote__row__cell--ask").text)
    print(r.html.find("#EURRUB > .quote__row__cell.quote__row__cell.quote__row__cell--ask").text)
    print(r.html.find("#EURRUB > .quote__row__cell.quote__row__cell.quote__row__cell--ask").text)

filename = "data.xlsx"
xls = pd.ExcelFile(filename)

def get_all_companies_and_cash_accounts() -> dict:
    sheet_x = xls.parse(0)
    
    caca = {}
    org = sheet_x["Организация"].tolist()
    sch = sheet_x["Субконто 1"].tolist()
    companies = set(org)

    for keys in companies:
        caca[keys] = []
        
    for row in sheet_x.iterrows():
        tmp = CashAccount(row[1]['Субконто 1'], row[1]['Валюта'], row[1]['Остаток'])
        caca[row[1]['Организация']].append(tmp)
        
    return caca

# TODO
def companies_needs_to_pay(company_name, cash_account_name):
    sheet_y = xls.parse(1)
    
    all_companies = get_all_companies_and_cash_accounts()
    for cash_acc in all_companies[company_name]:
        if cash_account_name == cash_acc.name:
            cash_account = cash_acc
    root = GraphNode(company_name, cash_account, 0, [])
    