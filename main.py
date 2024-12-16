from flask import Flask, render_template, request, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_FILENAME = "classrooms.db"

@app.route('/', methods=['GET', 'POST'])
def home():
    rooms = []
    searched_room = None
    if request.method == 'POST':
        location = request.form.get('location')
        input_time = request.form.get('time', None)

        try:
            building, room = location.split('-')
            searched_room = f"{building}-{room}"
        except ValueError:
            flash("건물-강의실 형식으로 입력해주세요. 예: 7-311", "error")
            return render_template('Search.html', rooms=rooms, searched_room=None)

        try:
            with sqlite3.connect(DB_FILENAME) as conn:
                cursor = conn.cursor()
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

    print("Searched Room (Flask):", searched_room)  # 디버깅 출력
    return render_template('Search.html', rooms=rooms, searched_room=searched_room)

if __name__ == "__main__":
    app.run(debug=True, port=5003)
