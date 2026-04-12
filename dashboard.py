from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Email Agent Dashboard is running!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)