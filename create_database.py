from bs4 import BeautifulSoup
import sqlite3

# SQLite 데이터베이스 연결
conn = sqlite3.connect('classrooms.db')
cursor = conn.cursor()

# 강의실 정보 테이블 생성
cursor.execute('''
CREATE TABLE IF NOT EXISTS classrooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_name TEXT,
    building TEXT,
    course_time TEXT,
    course_name TEXT
);
''')

# 데이터베이스에 데이터 삽입 함수
def insert_data(room_name, building, course_time, course_name):
    cursor.execute('''
    INSERT INTO classrooms (room_name, building, course_time, course_name)
    VALUES (?, ?, ?, ?)
    ''', (room_name, building, course_time, course_name))
    conn.commit()

# HTML 파일 열기
with open(r'C:\Users\cele9\Umchi.ckenpizzapasta\incheon.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# BeautifulSoup을 사용하여 HTML 파싱
soup = BeautifulSoup(html_content, 'lxml')

# 예시: 강의실 정보가 담긴 div 태그를 찾기
rooms = soup.find_all('div', class_='room_info')  # 'room_info' 클래스를 가진 div 태그를 찾음

for room in rooms:
    room_name = room.find('span', class_='room_name').get_text(strip=True)  # 강의실 이름
    building = room.find('span', class_='building').get_text(strip=True)  # 건물 이름
    course_time = room.find('span', class_='course_time').get_text(strip=True)  # 수업 시간
    course_name = room.find('span', class_='course_name').get_text(strip=True)  # 수업 이름

    # 데이터베이스에 삽입
    insert_data(room_name, building, course_time, course_name)

# 커넥션 닫기
conn.close()

print("데이터베이스에 데이터 삽입 완료!")