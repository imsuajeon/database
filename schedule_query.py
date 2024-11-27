import sqlite3

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

    # 결과 반환
    return result