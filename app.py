from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search():
    rooms = []
    if request.method == 'POST':
        input_time = request.form['time']
        rooms = get_room_status(input_time)  # get_room_status는 이전에 정의한 함수입니다.
    return render_template('Search.html', rooms=rooms)

def get_room_status(input_time):
    # SQLite 데이터베이스 연결
    conn = sqlite3.connect('classrooms.db')  # 데이터베이스 파일 이름으로 변경
    cursor = conn.cursor()

    # 특정 시간에 강의실 상태를 조회하는 SQL 쿼리
    query = """
    SELECT 건물, 강의실, 시간, 교과목
    FROM 편람
    WHERE 시간 = ?
    """
    cursor.execute(query, (input_time,))
    result = cursor.fetchall()
    conn.close()

    # 결과 반환 (DB에서 가져온 데이터를 room 객체로 변환)
    rooms = []
    for row in result:
        rooms.append({
            'building': row[0],
            'room': row[1],
            'time': row[2],
            'subject': row[3],
            'status': '사용 중' if row else '비어 있음'
        })
    return rooms

if __name__ == '__main__':
    app.run(debug=True)