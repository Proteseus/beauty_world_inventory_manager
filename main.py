from flask import *
import data_fetch as dd

app = Flask(__name__)

@app.route('/')
def index():
    data = dd.fetchAll()
    for i in range(0, len(data)):
        data[i]['Bar Code'] = int(data[i]['Bar Code'])
    return render_template('index.html', data=data, len=len(data))

@app.route('/edit/<id>', methods=['GET'])
def edit():
    pass

@app.route('/delete/<id>', methods=['GET'])
def delete(id):
    print(id)
    print(type(id))
    dd.delete_item(id)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)