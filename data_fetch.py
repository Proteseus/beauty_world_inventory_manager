import pandas as pd
import openpyxl as op
from datetime import datetime
from pprint import pprint

def fetchItem(name: str):
    df = pd.read_excel('data_files/stock.xlsx', sheet_name='Items')
    if(name in (df.loc[:, 'Name']).to_list()):
        ind = (df.loc[:, 'Name']).to_list().index(name)
        item = {}
        item["name"] = df.loc[:, 'Name'].to_list()[ind]
        item["price"] = df.loc[:, 'Price'].to_list()[ind]
        print (item)
        return item
    else:
        print (df)
        return -1
# fetchItem(10)

def fetchAll() -> list:
    df = pd.read_excel('data_files/stock.xlsx', sheet_name='Inventory')
    dic =  df.loc[:].to_dict()
    li = []
    for val in dic.values():
        li.append(val)
    # print (li)
    return li
# fetchAll()

def fetchAllSold():
    df = pd.read_excel('data_files/stock.xlsx', sheet_name='Sales')
    dic =  df.loc[:].to_dict()
    la = {}
    li = {}
    k = open('kk.json', 'w')
    for i in range(0, len(df)):
        li[i] = {}
        for key in dic.keys():
            if len(li[i]) == 0:
                li[i] = {key : ""}
            li[i][key] = dic[key][i]
    return li
# fetchAllSold()

def calculateSales(id, quantity: int):
    item = fetchItem(id)
    print(type(item['price']))
    print(quantity)
    total = int(quantity) * int(item["price"])
    print (total)
    return total
# calculateSales(10, 20)
#modify sales for inventory file
def setSales(id, quantity: int, customer: str):
    total = calculateSales(id, quantity)
    item = fetchItem(id)
    sale = [{"ItemID": id, "Price": item["price"], "Quantity": quantity, "Total": total, "Customer": customer, "Time": datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]
    df = pd.DataFrame(sale)
    
    print(total)
    
    rows = df.values.tolist()
    book = op.load_workbook(filename = 'data_files/stock.xlsx')
    sheet = book['Sales']
    sheet.delete_rows(idx=17)
    for row in rows:
        sheet.append(row)
    book.save(filename = 'data_files/test.xlsx')
    
    return total

#set new items to file
def set_items(description: str, category: int, made_in: str, size: float, unit: str, quantity: int, bar_code: int, price: float):
    profit_margin = price * 0.45
    profit_added_price = price + (price * 0.45)
    VAT = profit_margin * 0.15
    total = VAT + profit_added_price
    item = [{"Item Desc": description, "Category": category, "Made in": made_in, "Size/ml-g-oz": size, "Unit": unit, "Quantity": quantity, "Bar Code": bar_code, "Unit Price": price, "45% Profit": profit_margin, "Unit Price after profit": profit_added_price, "VAT": VAT, "Total": total, "On hand qty": quantity, "Sold qty": 0, "Total sales": 0}]
    df = pd.DataFrame(item)
    
    rows = df.values.tolist()
    book = op.load_workbook(filename='data_files/stock.xlsx')
    sheet = book['Inventory']
    for row in rows:
        sheet.append(row)
    book.save(filename='data_files/stock.xlsx')
#remove stock
def delete_item():
    df = pd.read_excel('data_files/stock.xlsx', sheet_name='Inventory', index_col=0)
    print(df.drop('col', inplace=True))
    
    rows = df.values.tolist()
    book = op.load_workbook(filename='data_files/stock.xlsx')
    sheet = book['Inventory']
    for row in rows:
        sheet.append(row)
    book.save(filename='data_files/stock.xlsx')
    
set_items('colpp', 'stock', 'eth', 12, 'pcs',23, 921321546465, 10.5)
# delete_item()