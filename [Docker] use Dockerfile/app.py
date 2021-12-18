from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/test')
def test():
    return render_template('index.html')

@app.route('/post', methods=['POST'])
def post():
    value = request.form['test']
    return value

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)