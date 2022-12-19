from flask import *
import data_fetch as dd

app = Flask(__name__)

@app.route('/')
def index():
    data = dd.fetchAll()
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)