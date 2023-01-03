from wtforms import Form, DecimalField, StringField, validators


class AddItemForm(Form):
    name = StringField("Name")
    category = StringField("Category")
    made_in = StringField("Made in")
    size = DecimalField("Size")
    unit = StringField("Unit")
    quantity = DecimalField("Quantity")
    barcode = DecimalField("BarCode")
    price = DecimalField("Price")
