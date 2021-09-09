from app.domain.helpers import MonthsCycle


def get_next_n_months_for_current(current: int, n: int):
    months_numbers = [current, ]
    while True:
        if next(MonthsCycle) == current:
            break
    for i in range(n):
        months_numbers.append(
            next(MonthsCycle)
        )
    return months_numbers
