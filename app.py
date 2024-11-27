from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    rooms = []  # 결과를 저장할 리스트

    if request.method == 'POST':
        # 폼 데이터 가져오기
        location = request.form['location']  # 건물-강의실
        input_time = request.form.get('time', None)  # 시간 (선택적)

        # 건물과 강의실 분리
        try:
            building, room = location.split('-')
        except ValueError:
            return "건물-강의실 형식으로 입력해주세요. 예: 인문관-101"

        # SQLite 데이터베이스 연결
        conn = sqlite3.connect('classrooms.db')  # 데이터베이스 파일 이름 확인
        cursor = conn.cursor()

        # SQL 쿼리 작성 및 실행
        if input_time:  # 시간이 입력된 경우
            query = """
            SELECT 건물, 강의실, 시간, 교과목
            FROM 편람
            WHERE 건물 = ? AND 강의실 = ? AND 시간 = ?
            """
            cursor.execute(query, (building, room, input_time))
        else:  # 시간이 입력되지 않은 경우
            query = """
            SELECT 건물, 강의실, 시간, 교과목
            FROM 편람
            WHERE 건물 = ? AND 강의실 = ?
            """
            cursor.execute(query, (building, room))

        results = cursor.fetchall()
        conn.close()

        # 결과를 HTML에 사용할 형식으로 변환
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

    return render_template('Search.html', rooms=rooms)

# Flask 앱 실행
if __name__ == "__main__":
    app.run(debug=True)