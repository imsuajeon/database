from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# 데이터베이스 파일 경로
DB_FILENAME = "classrooms.db"

@app.route('/')
def index():
    return render_template('search2.html')

@app.route('/search', methods=['POST'])
def search():
    subject = request.form['subject']
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    
    # LIKE 쿼리 사용
    query = """
    SELECT 학수번호, 건물, 강의실, 시간, 교과목, 종류 
    FROM 편람
    WHERE 교과목 LIKE ?
    """
    cursor.execute(query, (f"%{subject}%",))  # 와일드카드 사용
    results = cursor.fetchall()
    conn.close()
    
    return render_template('search2.html', results=results, subject=subject)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
