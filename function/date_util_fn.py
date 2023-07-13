def day_of_week(weekday: int) -> str:
    week_dict = {
        0 : '月',
        1 : '火',
        2 : '水',
        3 : '木',
        4 : '金',
        5 : '土',
        6 : '日',
    }
    return week_dict[weekday]