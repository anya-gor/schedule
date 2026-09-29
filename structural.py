"""Учебное расписание дня — структурный стиль.

Данные (словари с предметом/временем/аудиторией) отделены от логики:
все операции — это отдельные функции над списком расписания.
"""


# ---------- Работа со временем ----------

def parse_time(text: str) -> int:
    """'08:30' -> 510 (минуты с полуночи). Нужно для корректной сортировки."""
    hours, minutes = text.split(":")
    return int(hours) * 60 + int(minutes)


def format_time(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


# ---------- Базовые операции над расписанием ----------

def make_lesson(subject: str, start: str, room: str) -> dict:
    """Создаёт запись пары. Время храним и в исходном виде, и в минутах."""
    return {"subject": subject, "start": start, "time": parse_time(start), "room": room}


def add_lesson(schedule: list, subject: str, start: str, room: str) -> bool:
    """Добавляет пару. False — если пара с таким предметом уже есть."""
    if find_by_subject(schedule, subject) is not None:
        return False
    schedule.append(make_lesson(subject, start, room))
    return True


def delete_by_subject(schedule: list, subject: str) -> bool:
    """Удаляет пару по предмету. False — если предмет не найден."""
    for i, lesson in enumerate(schedule):
        if lesson["subject"].lower() == subject.lower():
            del schedule[i]
            return True
    return False


def find_by_subject(schedule: list, subject: str):
    for lesson in schedule:
        if lesson["subject"].lower() == subject.lower():
            return lesson
    return None


def find_at_time(schedule: list, start: str):
    """Находит пару, начинающуюся в указанное время (или None)."""
    wanted = parse_time(start)
    for lesson in schedule:
        if lesson["time"] == wanted:
            return lesson
    return None


def sorted_by_time(schedule: list) -> list:
    """Список пар по возрастанию времени (исходный список не меняется)."""
    return sorted(schedule, key=lambda lesson: lesson["time"])


def format_schedule(schedule: list) -> str:
    if not schedule:
        return "  (расписание пусто)"
    lines = []
    for lesson in sorted_by_time(schedule):
        lines.append(f"  {format_time(lesson['time'])}  {lesson['subject']} — ауд. {lesson['room']}")
    return "\n".join(lines)


# ---------- Демонстрационный сценарий ----------

def demo(title: str, actions: list) -> None:
    """Прогоняет один набор действий и печатает итоговое расписание."""
    schedule: list = []
    print(f"\n=== {title} ===")
    for action in actions:
        op = action[0]
        if op == "add":
            ok = add_lesson(schedule, action[1], action[2], action[3])
            print(f"добавить {action[1]!r} {action[2]} -> {'ok' if ok else 'отклонено (предмет уже есть)'}")
        elif op == "del":
            ok = delete_by_subject(schedule, action[1])
            print(f"удалить предмет {action[1]!r} -> {'удалено' if ok else 'не найдено'}")
        elif op == "find":
            lesson = find_at_time(schedule, action[1])
            found = f"{lesson['subject']}, ауд. {lesson['room']}" if lesson else "ничего не найдено"
            print(f"поиск на {action[1]} -> {found}")
    print("Итоговое расписание:")
    print(format_schedule(schedule))


if __name__ == "__main__":
    demo("Пример 1: обычный понедельник", [
        ("add", "Математический анализ", "08:30", "301"),
        ("add", "Информатика", "10:10", "215"),
        ("add", "Физика", "11:50", "118"),
        ("find", "10:10"),
        ("find", "12:00"),
    ])

    demo("Пример 2: удаление и повторное добавление", [
        ("add", "История", "09:00", "104"),
        ("add", "Информатика", "10:10", "215"),
        ("add", "Информатика", "14:00", "216"),  # дубликат -> отклоняется
        ("del", "История"),
        ("add", "История", "13:30", "105"),
    ])

    demo("Пример 3: пустое расписание", [
        ("find", "08:30"),
        ("del", "Физика"),
    ])
