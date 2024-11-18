import csv

# CSV 파일 읽기
def load_rooms(file_name):
    rooms = {}
    with open(file_name, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ho_gwan = row['호관']
            ho_su = row['호수']
            room_name = row['강의실명']
            
            if ho_gwan not in rooms:
                rooms[ho_gwan] = {}
            rooms[ho_gwan][ho_su] = room_name
    return rooms

# 강의실명 출력
def get_room_name(rooms, ho_gwan, ho_su):
    if ho_gwan in rooms and ho_su in rooms[ho_gwan]:
        return rooms[ho_gwan][ho_su]
    else:
        return "해당 강의실을 찾을 수 없습니다."

# 사용자 입력 받기
def main():
    rooms = load_rooms('인천대_건물명.csv')  # rooms.csv 파일을 로드
    ho_gwan = input("호관 번호를 입력하세요: ")
    ho_su = input("호수 번호를 입력하세요: ")
    
    room_name = get_room_name(rooms, ho_gwan, ho_su)
    print(f"강의실명: {room_name}")

if __name__ == "__main__":
    main()
