from datetime import datetime

def get_today(_format):
    today = datetime.now()
    return today.strftime(_format)

def day_mapping(date_str, _format):
    days_in_korean = {
        0: '월',  # Monday
        1: '화',  # Tuesday
        2: '수',  # Wednesday
        3: '목',  # Thursday
        4: '금',  # Friday
        5: '토',  # Saturday
        6: '일'  # Sunday
    }

    today = datetime.strptime(date_str, _format)
    # 요일 숫자 가져오기 (0=월요일, 6=일요일)
    weekday = today.weekday()
    korean_day = days_in_korean[weekday]
    return korean_day