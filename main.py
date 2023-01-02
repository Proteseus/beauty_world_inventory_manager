from flask import *
import data_fetch as dd

app = Flask(__name__)


@app.route('/')
def index():
    data = dd.fetchAll()
    for i in range(0, len(data)):
        data[i]['Bar Code'] = int(data[i]['Bar Code'])
    return render_template('index.html', data=data, len=len(data))


@app.route('/edit/<item_name>', methods=['GET'])
def edit(item_name: str):
    pass


@app.route('/delete/<item_name>', methods=['GET'])
def delete(item_name: str):
    print(item_name)
    print(type(item_name))
    dd.delete_item(item_name)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
