from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

DB_FILENAME = "classrooms.db"

# 수업 추가
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        학수번호 = request.form['학수번호']
        건물 = request.form['건물']
        강의실 = request.form['강의실']
        교과목 = request.form['교과목']
        시간 = request.form['시간']
        종류 = request.form['종류']

        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        query = """
        INSERT INTO 편람 (학수번호, 건물, 강의실, 교과목, 시간, 종류)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        cursor.execute(query, (학수번호, 건물, 강의실, 교과목, 시간, 종류))
        conn.commit()
        conn.close()
        return "수업이 추가되었습니다."

# 수업 삭제
@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        건물 = request.form['건물']
        강의실 = request.form['강의실']
        시간 = request.form['시간']
        교과목 = request.form['교과목']

        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()
        query = """
        DELETE FROM 편람
        WHERE 건물 = ? AND 강의실 = ? AND 시간 = ? AND 교과목 = ?
        """
        cursor.execute(query, (건물, 강의실, 시간, 교과목))
        conn.commit()
        conn.close()
        return "수업이 삭제되었습니다."

# 수업 수정
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        학수번호 = request.form['학수번호']
        건물 = request.form['건물']
        강의실 = request.form['강의실']
        시간 = request.form['시간']
        교과목 = request.form['교과목']
        종류 = request.form['종류']

        conn = sqlite3.connect(DB_FILENAME)
        cursor = conn.cursor()

        # 수업 정보를 업데이트하는 쿼리
        query = """
        UPDATE 편람
        SET 건물 = ?, 강의실 = ?, 시간 = ?, 교과목 = ?, 종류 = ?
        WHERE 학수번호 = ?
        """
        cursor.execute(query, (건물, 강의실, 시간, 교과목, 종류, 학수번호))
        conn.commit()
        conn.close()
        return "수업 정보가 수정되었습니다."

@app.route('/')
def index():
    return render_template('modifydb.html')

if __name__ == "__main__":
    app.run(debug=True, port=5003)  # 5003 포트에서 실행
