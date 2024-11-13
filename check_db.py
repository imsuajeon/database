import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('classrooms.db')
cursor = conn.cursor()

# 데이터베이스에서 모든 데이터 조회
cursor.execute('SELECT * FROM classrooms')

# 결과 출력
rows = cursor.fetchall()
for row in rows:
    print(row)

# 연결 닫기
conn.close()