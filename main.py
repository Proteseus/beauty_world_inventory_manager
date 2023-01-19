from flask import Flask, render_template, redirect, request, flash
import data_fetch as dd

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)


@app.route('/')
def index():
    inventory = dd.fetch_all()
    key = ["Item Desc", "Category", "Made in", "Size/ml-g-oz", "Unit", "Quantity", "Bar Code", "Unit Price",
           "Profit", "Unit Price after profit", "On hand qty"]
    for i in range(0, len(inventory)):
        inventory[i]['Bar Code'] = int(inventory[i]['Bar Code'])
    return render_template('index.html', data=inventory, keys=key)


@app.route('/add/', methods=['POST', 'GET'])
def add():
    form = request.form
    if request.method == 'POST':
        items = [form['name'], form['category'], form['made_in'], form['size'], form['unit'], form['quantity'],
                 form['barcode'], form['price']]
        item_key = ["Item Desc", "Category", "Made in", "Size/ml-g-oz", "Unit", "Quantity", "Bar Code", "Unit Price"]
        item = {}
        for idx, i_key in enumerate(item_key):
            item[i_key] = items[idx]
        print(item)
        dd.set_items(item)
        return redirect('/')
    return render_template('add_listing.html', form=form)


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


@app.route('/sales/', methods=['GET'])
def sale():
    item_names = []
    items = dd.fetch_all()
    for idx in items:
        item_names.append(items[idx]['Item Desc'])

    return render_template('sales.html', items=item_names)


@app.route('/sales/', methods=['POST'])
def sale_item():
    form_data = request.form
    result, remaining = dd.set_sales(form_data['name'], form_data['quantity'], form_data['customer'])
    if result:
        return redirect('/sold/')
    else:
        flash(f"Not enough in stock, only {remaining} are available", 'warning')
    return render_template('sales.html')


@app.route('/sold/', methods=['GET'])
def sold():
    data = dd.fetch_all_sold()
    return render_template('all_sold.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
