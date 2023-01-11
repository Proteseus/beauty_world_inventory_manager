from wtforms import Form, DecimalField, StringField, SelectField, DateTimeLocalField
import data_fetch as dd


# item adding form
class AddItemForm(Form):
    name = StringField("Name")
    category = StringField("Category")
    made_in = StringField("Made in")
    size = DecimalField("Size")
    unit = StringField("Unit")
    quantity = DecimalField("Quantity")
    barcode = DecimalField("BarCode")
    price = DecimalField("Price")


# item sales form
class SaleItemForm(Form):
    item_names = []
    items = dd.fetch_all()
    for idx in items:
        item_names.append(items[idx]['Item Desc'])
    print(item_names)
    name = SelectField("Name", choices=item_names, id='name-selector')
    quantity = DecimalField("Quantity", id='quantity-input')
    customer = StringField("Customer", default="", id='customer-input')
