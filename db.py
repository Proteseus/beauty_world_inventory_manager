import sqlite3
import pandas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import User
from datetime import datetime
from secrets import compare_digest


def connector():
    conn = sqlite3.connect('instance/sample.sqlite')
    cur = conn.cursor()
    return conn, cur


def initializer():
    conn, cur = connector()
    # read from excel
    item = ["No", "item", "category", "made", "size/ml-g-Oz", "unit", "quantity", "barcode",
            "unit_price", "profit", "price_after_profit", "on_hand", "expiry_date"]
    df = pandas.read_excel('DOC-20230108-WA0002.xlsx', sheet_name='All Items', skiprows=2, index_col='No', usecols=item)

    # add read data to sqlite db
    df.to_sql('inventory', conn, if_exists='replace', index=False)

    cur.execute("""CREATE TABLE IF NOT EXISTS sale (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item VARCHAR(255) NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                total REAL NOT NULL,
                vat REAL NOT NULL,
                customer TEXT,
                phone_number INTEGER,
                "date" TEXT NOT NULL
                )""")
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS supplier (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item VARCHAR(255) NOT NULL,
                    quantity INTEGER NOT NULL,
                    total REAL NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    phone INTEGER NOT NULL,
                    "date" TEXT NOT NULL
                    )""")
    conn.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS kart (
                    name VARCHAR(255) NOT NULL,
                    quantity INTEGER NOT NULL,
                    price REAL NOT NULL, 
                    customer VARCHAR(255),
                    phone_number INTEGER
                    )""")
    cur.close()
    conn.commit()
    conn.close()


# initializer()


def login(user: str, password: str):
    conn, cur = connector()
    cur.execute("select password from user where username = ?", (user,))
    item = cur.fetchone()[0]
    cur.close()
    conn.close()
    print(item, password)
    if item == password:
        return True
    else:
        return False


def fetch_item(item_id: str):
    conn, cur = connector()
    cur.execute("select * from inventory where item = ?", (item_id,))
    item = cur.fetchall()
    cur.close()
    conn.close()
    return item


def fetch_item_sim(item_id: str):
    conn, cur = connector()
    cur.execute("select * from inventory where item like ?", ('%' + item_id + '%',))
    item = cur.fetchall()
    cur.close()
    conn.close()
    return item


def fetch_all():
    conn, cur = connector()
    cur.execute("select * from inventory")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def fetch_all_sold():
    conn, cur = connector()
    cur.execute("select * from sale")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def set_supplier(items: list):
    conn, cur = connector()
    cur.execute("""INSERT INTO supplier (item, quantity, total, name, phone, date) 
        VALUES (?, ?, ?, ?, ?, ?)""",
                (items[0], items[1], items[2], items[3], items[4], datetime.now().strftime('%Y-%m-%d'),))
    conn.commit()
    conn.close()


def fetch_supplier():
    conn, cur = connector()
    cur.execute("select item, quantity, total, name, phone, date from supplier")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def fetch_cart():
    conn, cur = connector()
    cur.execute("SELECT * FROM kart")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def fetch_sale(item_id: int):
    conn, cur = connector()
    cur.execute("select item, price, quantity, total, vat from sale where id = ?", (item_id,))
    item = cur.fetchall()
    cur.close()
    conn.close()
    return item


def calculate_sales(price: float, quantity: int):
    total = int(quantity) * price
    print("Total:", total)
    return total


def modify_on_sale(item_id: str, quantity: int):
    conn, cur = connector()
    item = fetch_item(item_id)

    cur.execute('UPDATE inventory SET on_hand=? WHERE item=?', ((item[0][10] - quantity), item_id,))
    conn.commit()
    conn.close()


def on_hand_checker(item_id: str, quantity: int):
    item = fetch_item(item_id)
    if quantity > int(item[0][10]):
        return False, item[0][10]
    else:
        return True, item[0][10]


def add_to_kart(items: list):
    price = fetch_item(items[0])[0][9]
    total = price * items[1]
    conn, cur = connector()
    cur.execute("""INSERT INTO kart (name, quantity, price, customer, phone_number) VALUES (?, ?, ?, ?, ?)""",
                (items[0], items[1], total, items[2], items[3]))
    conn.commit()
    conn.close()


def remove_from_cart(item_id: str):
    conn, cur = connector()
    cur.execute("""DELETE FROM kart WHERE name=?""", (item_id,))
    conn.commit()
    conn.close()


def clear_cart():
    conn, cur = connector()
    cur.execute("DELETE FROM kart")
    conn.commit()
    conn.close()


def set_sale(item_id: str, quantity: int, customer: str, phone_number: int):
    item = fetch_item(item_id)

    total = calculate_sales(item[0][9], quantity)
    vat = total * 0.02
    total += vat
    print("#total:", item[0][9], item[0][8], quantity, total, sep=' : ')

    conn, cur = connector()
    cur.execute("""INSERT INTO sale (item, price, quantity, total, vat, customer, phone_number, date) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (item[0][0], item[0][7], quantity, total, vat, customer, phone_number,
                 datetime.now().strftime('%Y-%m-%d'),))
    conn.commit()
    conn.close()

    modify_on_sale(item_id, quantity)

    return True


def set_items(items: list):
    conn, cur = connector()
    if items[0] == fetch_item(items[0])[0][0]:
        on_hand = int(items[5]) + int(fetch_item(items[0])[0][10])
        cur.execute('UPDATE inventory SET on_hand=? WHERE item=?', (on_hand, items[0],))
        conn.commit()
        conn.close()
    else:
        print(type(int(items[8])))
        profit = float(items[7]) + (int(items[8]) / 100) * float(items[7])
        print(profit)
        cur.execute("""INSERT INTO inventory (item, category, made, "size/ml-g-Oz", unit, quantity, barcode,
                                        unit_price, profit, price_after_profit, on_hand, expiry_date) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (items[0], items[1], items[2], items[3], items[4], items[5], items[6],
                     items[7], items[8], profit, items[5], items[9],))
        conn.commit()
        conn.close()


def delete_item(item_id: str):
    conn, cur = connector()
    cur.execute('DELETE FROM inventory WHERE item=?', (item_id,))
    conn.commit()
    conn.close()


def edit_item(item_id: str, edited_item: dict):
    print(edited_item)
    conn, cur = connector()
    cur.execute('UPDATE inventory SET item=?, category=?, made=?, "size/ml-g-Oz"=?, unit_price=?, profit=?'
                'WHERE item=?',
                (edited_item[0], edited_item[1], edited_item[2], edited_item[3],
                 edited_item[4], edited_item[5], edited_item[0],))
    conn.commit()
    conn.close()


#################
def delete_sale(item_id: list):
    conn, cur = connector()
    print(item_id)
    print(len(item_id))

    item_on_hand = int(fetch_item(item_id[1])[0][10]) + int(fetch_sale(item_id[0])[0][2])

    cur.execute('UPDATE inventory SET on_hand=? WHERE item=?', (item_on_hand, item_id[1],))
    conn.commit()

    cur.execute('DELETE FROM sale WHERE id=?', (item_id[0],))
    conn.commit()
    conn.close()


def edit_sale(item_id: int, edited_item: list):
    print(edited_item)
    items = fetch_item(edited_item[1])
    item = items[0]
    sold = fetch_sale(item_id)[0]
    print(sold, item, sep="\n")
    price = sold[1]
    quantity = sold[2]

    original = item[10] + quantity
    print("=>", original)
    original -= int(edited_item[2])
    print("=>", original)

    conn, cur = connector()
    total = int(edited_item[2]) * price
    vat = total * 0.2
    total += vat

    cur.execute('UPDATE sale SET item=?, price=?, quantity=?, total=?, vat=?'
                'WHERE id=?',
                (edited_item[1], price, edited_item[2], total,
                 vat, edited_item[0],))
    conn.commit()

    cur.execute('UPDATE inventory SET on_hand=? WHERE item=?', (original, item[0]))
    conn.commit()
    conn.close()


####################


def signup(username: str, password: str, role: str):
    try:
        engine = create_engine('sqlite:///instance/sample.sqlite', echo=True)

        Session = sessionmaker(bind=engine)
        session = Session()

        user = User(username=username, password=password, role=role)
        session.add(user)

        session.commit()
        session.commit()

        return True
    except Exception:
        return False


def get_role(username: str):
    conn, cur = connector()
    cur.execute("SELECT * FROM user WHERE username=?", (username,))
    role = cur.fetchone()[3]
    cur.close()
    conn.close()
    return role


def get_daily_report():
    conn, cur = connector()
    cur.execute("""SELECT id, i.item, category, made, "size/ml-g-Oz", unit, s.quantity, barcode, unit_price, profit,
                    price_after_profit, total, vat, customer, phone_number, date
                    FROM sale as s
                    LEFT JOIN inventory as i
                    ON i.item = s.item AND date = date('now')""")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_weekly_report():
    def fetch_week():
        week = datetime.now().isocalendar().week
        if week < 10:
            return '0' + str(week)
        return str(week)

    conn, cur = connector()
    cur.execute("""SELECT id, i.item, category, made, "size/ml-g-Oz", unit, s.quantity, barcode, unit_price, profit, 
                    price_after_profit, total, vat, customer, phone_number, date
                    FROM sale as s
                    LEFT JOIN inventory as i
                    ON i.item = s.item AND strftime('%W', date) = ? """, (fetch_week(),))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_monthly_report():
    def fetch_month():
        month = datetime.now().month
        if month < 10:
            return '0' + str(month)
        return str(month)

    conn, cur = connector()
    cur.execute("""SELECT id, i.item, category, made, "size/ml-g-Oz", unit, s.quantity, barcode, unit_price, profit, 
                    price_after_profit, total, vat, customer, phone_number, date
                    FROM sale as s
                    LEFT JOIN inventory as i
                    ON i.item = s.item AND strftime('%m', date) = ? """, (fetch_month(),))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_annual_report():
    def fetch_year():
        year = datetime.now().year
        return str(year)

    conn, cur = connector()
    cur.execute("""SELECT id, i.item, category, made, "size/ml-g-Oz", unit, s.quantity, barcode, unit_price, profit, 
                    price_after_profit, total, vat, customer, phone_number, date
                    FROM sale as s
                    LEFT JOIN inventory as i
                    ON i.item = s.item AND strftime('%Y', date) = ? """, (fetch_year(),))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
