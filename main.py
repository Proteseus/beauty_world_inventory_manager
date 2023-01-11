from flask import Flask, render_template, redirect, request, flash
import data_fetch as dd
from forms import AddItemForm, SaleItemForm

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)


@app.route('/')
def index():
    data = dd.fetch_all()
    for i in range(0, len(data)):
        data[i]['Bar Code'] = int(data[i]['Bar Code'])
    return render_template('index.html', data=data)


@app.route('/add/', methods=['POST', 'GET'])
def add():
    form = AddItemForm(request.form)
    if request.method == 'POST' and form.validate():
        items = [form.name.data, form.category.data, form.made_in.data, form.size.data, form.unit.data,
                 form.quantity.data, form.barcode.data, form.price.data]
        item_key = ["Item Desc", "Category", "Made in", "Size/ml-g-oz", "Unit", "Quantity", "Bar Code", "Unit Price"]
        item = {}
        for idx, i_key in enumerate(item_key):
            item[i_key] = items[idx]
        print(item)
        dd.set_items(item)
        return redirect('/')
    return render_template('add_listings.html', form=form)


@app.route('/edit/<item_name>', methods=['GET'])
def edit(item_name: str):
    data = dd.fetch_item(item_name)
    for ind in data:
        print(ind)
    return render_template('edit.html', data=data)


@app.route('/edit/', methods=['POST'])
def edit_item():
    form_data = request.form
    edited_item = {}
    keys = [1, 2, 3, 4, 8, 9]
    for idx, key in enumerate(form_data.keys()):
        edited_item[keys[idx]] = form_data[key]
    print(edited_item)
    dd.edit_item(edited_item[1], edited_item)

    return redirect('/')


@app.route('/delete/<item_name>', methods=['GET'])
def delete(item_name: str):
    print(item_name)
    print(type(item_name))
    dd.delete_item(item_name)
    return redirect('/')


@app.route('/sales/', methods=['GET', 'POST'])
def sale_item():
    form = SaleItemForm(request.form)
    if request.method == 'POST' and form.validate():
        result, remaining = dd.set_sales(form.name.data, form.quantity.data, form.customer.data)
        if result:
            return redirect('/sold/')
        else:
            flash(f"Not enough in stock, only {remaining} are available", 'warning')
    return render_template('sales.html', form=form)


@app.route('/sold/', methods=['GET'])
def sold():
    data = dd.fetch_all_sold()
    return render_template('all_sold.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.124.254')
