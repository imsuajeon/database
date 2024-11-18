from flask import Flask, render_template, request
import sqlite3

# Flask 애플리케이션 객체 정의
app = Flask(__name__)

# 데이터베이스 연결 함수
def get_db_connection():
    conn = sqlite3.connect('classrooms.db')  # 데이터베이스 파일 경로에 맞게 수정
    conn.row_factory = sqlite3.Row  # 결과를 딕셔너리 형식으로 반환
    return conn

# 홈 페이지
@app.route('/', methods=['GET'])
def index():
    return render_template('Search.html')  # Search.html을 템플릿으로 렌더링

# 검색 결과 페이지
@app.route('/search', methods=['GET'])
def search():
    호관명 = request.args.get('호관명')
    호수 = request.args.get('호수')

    # 디버그용 로그 출력
    print(f"호관명: {호관명}, 호수: {호수}")

    # 데이터베이스에서 검색 쿼리 실행
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 강의실명 FROM classrooms
        WHERE 호관명 LIKE ? AND 호수 LIKE ?
    ''', (f'%{호관명}%', f'%{호수}%'))  # %는 와일드카드로 부분 일치를 의미
    results = cursor.fetchall()
    conn.close()

    # 디버그용 로그 출력
    print(f"검색 결과: {results}")

    return render_template('Search.html', results=results)

# 애플리케이션 실행
if __name__ == '__main__':
    app.run(debug=True)
