from flask import Flask, render_template, redirect, request
import data_fetch as dd

app = Flask(__name__)


@app.route('/')
def index():
    data = dd.fetchAll()
    for i in range(0, len(data)):
        data[i]['Bar Code'] = int(data[i]['Bar Code'])
    return render_template('index.html', data=data)


@app.route('/edit/<item_name>', methods=['GET'])
def edit(item_name: str ):
    data = dd.fetchItem(item_name)
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
    dd.edit(edited_item[1], edited_item)

    return redirect('/')


@app.route('/delete/<item_name>', methods=['GET'])
def delete(item_name: str):
    print(item_name)
    print(type(item_name))
    dd.delete_item(item_name)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, host='192.168.124.254')
