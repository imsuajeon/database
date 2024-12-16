from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_FILENAME = "classrooms.db"

# 메인 페이지 및 검색 기능
@app.route('/', methods=['GET', 'POST'])
def home():
    rooms = []
    if request.method == 'POST':
        location = request.form.get('location')
        input_time = request.form.get('time', None)

        try:
            building, room = location.split('-')
        except ValueError:
            flash("건물-강의실 형식으로 입력해주세요. 예: 7-311", "error")
            return render_template('Search.html', rooms=rooms)

        try:
            with sqlite3.connect(DB_FILENAME, check_same_thread=False) as conn:
                cursor = conn.cursor()
                # 기본 쿼리: 건물과 강의실로 조회
                query = """
                SELECT 건물, 강의실, 시간, 교과목
                FROM 편람
                WHERE 건물 = ? AND 강의실 = ?
                """
                params = [building, room]
                if input_time:
                    query += " AND 시간 = ?"
                    params.append(input_time)
                cursor.execute(query, params)
                results = cursor.fetchall()

                # 결과를 rooms 리스트에 담을 때, 사용 여부를 판단
                rooms = [
                    {
                        'building': row[0],
                        'room': row[1],
                        'time': row[2],
                        'subject': row[3],
                        'status': '사용 중' if input_time and row[2] == input_time else '비어 있음'
                    }
                    for row in results
                ]
        except sqlite3.Error as e:
            flash(f"데이터베이스 오류 발생: {e}", "error")
    return render_template('Search.html', rooms=rooms)

# 수업 관리 페이지로 이동
@app.route('/db-management', methods=['GET'])
def db_management():
    return render_template('SelectPage.html')  # 수업 관리 페이지를 렌더링

# 수업 추가 페이지
@app.route('/insert', methods=['GET'])
def insert_page():
    return render_template('InsertPage.html')

# 수업 삭제 페이지
@app.route('/delete', methods=['GET'])
def delete_page():
    return render_template('DeletePage.html')

# 수업 수정 페이지
@app.route('/update', methods=['GET'])
def update_page():
    return render_template('UpdatePage.html')

# 수업 추가 처리
@app.route('/insert-class', methods=['POST'])
def insert():
    try:
        학수번호 = request.form['학수번호']
        건물 = request.form['건물']
        강의실 = request.form['강의실']
        교과목 = request.form['교과목']
        시간 = request.form['시간']
        종류 = request.form['종류']

        with sqlite3.connect(DB_FILENAME, check_same_thread=False) as conn:
            cursor = conn.cursor()

            # 학수번호, 건물, 강의실, 시간, 교과목, 종류가 모두 일치하는 수업이 있는지 확인
            cursor.execute(""" 
            SELECT COUNT(*) FROM 편람 
            WHERE 학수번호 = ? AND 건물 = ? AND 강의실 = ? AND 시간 = ? AND 교과목 = ? AND 종류 = ? 
            """, (학수번호, 건물, 강의실, 시간, 교과목, 종류))
            result = cursor.fetchone()

            if result[0] > 0:
                flash("이미 동일한 수업이 존재합니다.", "error")
                return redirect(url_for('insert_page'))

            # 수업이 없으면 새로운 수업을 추가
            cursor.execute(""" 
            INSERT INTO 편람 (학수번호, 건물, 강의실, 교과목, 시간, 종류) 
            VALUES (?, ?, ?, ?, ?, ?) 
            """, (학수번호, 건물, 강의실, 교과목, 시간, 종류))
            conn.commit()
        flash("수업이 추가되었습니다.")
    except sqlite3.Error as e:
        flash(f"데이터베이스 오류 발생: {e}", "error")
    return redirect(url_for('insert_page'))

# 수업 삭제 처리
@app.route('/delete-class', methods=['POST'])
def delete():
    try:
        학수번호 = request.form['학수번호']
        건물 = request.form['건물']
        강의실 = request.form['강의실']
        시간 = request.form['시간']
        교과목 = request.form['교과목']
        종류 = request.form['종류']

        with sqlite3.connect(DB_FILENAME, check_same_thread=False) as conn:
            cursor = conn.cursor()

            # 해당 수업이 존재하는지 확인
            cursor.execute(""" 
            SELECT COUNT(*) FROM 편람 
            WHERE 학수번호 = ? AND 건물 = ? AND 강의실 = ? AND 시간 = ? AND 교과목 = ? AND 종류 = ? 
            """, (학수번호, 건물, 강의실, 시간, 교과목, 종류))
            result = cursor.fetchone()

            if result[0] == 0:
                flash("삭제하려는 수업이 존재하지 않습니다.", "error")
                return redirect(url_for('delete_page'))

            # 수업이 존재하면 삭제
            cursor.execute(""" 
            DELETE FROM 편람 WHERE 학수번호 = ? AND 건물 = ? AND 강의실 = ? AND 시간 = ? AND 교과목 = ? AND 종류 = ? 
            """, (학수번호, 건물, 강의실, 시간, 교과목, 종류))
            conn.commit()
        flash("수업이 삭제되었습니다.")
    except sqlite3.Error as e:
        flash(f"데이터베이스 오류 발생: {e}", "error")
    return redirect(url_for('delete_page'))

# 수업 수정 처리
@app.route('/update-class', methods=['POST'])
def update():
    try:
        기존_학수번호 = request.form['기존_학수번호']
        기존_건물 = request.form['기존_건물']
        기존_강의실 = request.form['기존_강의실']
        기존_시간 = request.form['기존_시간']
        기존_교과목 = request.form['기존_교과목']
        기존_종류 = request.form['기존_종류']

        새_학수번호 = request.form['새_학수번호']
        새_건물 = request.form['새_건물']
        새_강의실 = request.form['새_강의실']
        새_시간 = request.form['새_시간']
        새_교과목 = request.form['새_교과목']
        새_종류 = request.form['새_종류']

        with sqlite3.connect(DB_FILENAME, check_same_thread=False) as conn:
            cursor = conn.cursor()

            # 기존 수업이 존재하는지 확인
            cursor.execute(""" 
            SELECT COUNT(*) FROM 편람 
            WHERE 학수번호 = ? AND 건물 = ? AND 강의실 = ? AND 시간 = ? AND 교과목 = ? AND 종류 = ? 
            """, (기존_학수번호, 기존_건물, 기존_강의실, 기존_시간, 기존_교과목, 기존_종류))
            result = cursor.fetchone()

            if result[0] == 0:
                flash("수정하려는 수업이 존재하지 않습니다.", "error")
                return redirect(url_for('update_page'))

            # 기존 수업이 존재하면 수정
            cursor.execute(""" 
            UPDATE 편람 
            SET 학수번호 = ?, 건물 = ?, 강의실 = ?, 시간 = ?, 교과목 = ?, 종류 = ? 
            WHERE 학수번호 = ? AND 건물 = ? AND 강의실 = ? AND 시간 = ? AND 교과목 = ? AND 종류 = ? 
            """, (새_학수번호, 새_건물, 새_강의실, 새_시간, 새_교과목, 새_종류,
                  기존_학수번호, 기존_건물, 기존_강의실, 기존_시간, 기존_교과목, 기존_종류))
            conn.commit()
        flash("수업 정보가 수정되었습니다.")
    except sqlite3.Error as e:
        flash(f"데이터베이스 오류 발생: {e}", "error")
    return redirect(url_for('update_page'))

if __name__ == "__main__":
    app.run(debug=True, port=5003)
