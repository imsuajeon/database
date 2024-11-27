def check_room_status(input_time):
    # 강의실 상태 조회
    room_usage = get_room_status(input_time)
    status = []

    for room in room_usage:
        건물, 강의실, 시간, 교과목 = room
        status.append({
            "building": 건물,
            "room": 강의실,
            "time": 시간,
            "subject": 교과목,
            "status": "사용 중" if 시간 == input_time else "비어 있음"
        })

    return status