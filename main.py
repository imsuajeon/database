from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('main.html')

if __name__ == "__main__":
    app.run(debug=True, port=5002)  # 메인 페이지는 5002번 포트에서 실행
