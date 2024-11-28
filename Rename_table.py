import sqlite3

# 데이터베이스 연결
conn = sqlite3.connect('classrooms.db')
cursor = conn.cursor()

# 2. 새 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS 편람_new (
    학수번호 TEXT,
    건물 TEXT,
    강의실 TEXT,
    시간 TEXT,
    교과목 TEXT,
    종류 TEXT
);
''')

# 3. 기존 데이터를 새 테이블로 이동
cursor.execute('''
INSERT INTO 편람_new (학수번호, 건물, 강의실, 시간, 교과목, 종류)
SELECT field1, field2, field3, field4, field5, field6
FROM 편람;
''')

# 4. 기존 테이블 삭제
cursor.execute('DROP TABLE 편람;')

# 5. 새 테이블 이름 변경
cursor.execute('ALTER TABLE 편람_new RENAME TO 편람;')

# 변경 사항 저장 및 종료
conn.commit()
conn.close()

print("테이블 컬럼 이름 변경 및 데이터 이전 완료!")