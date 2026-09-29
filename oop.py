"""Учебное расписание дня — ООП-стиль.

Состояние инкапсулировано: Lesson хранит свои поля и проверяет их,
Schedule владеет коллекцией и всеми операциями над ней.
"""

from __future__ import annotations


class Lesson:
    """Пара: предмет, время начала, аудитория."""

    def __init__(self, subject: str, start: str, room: str) -> None:
        self._subject = self._validate_subject(subject)
        self._start = self._validate_start(start)
        self._room = self._validate_room(room)

    # --- инкапсуляция: доступ только через свойства ---

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def start(self) -> str:
        return self._start

    @property
    def start_minutes(self) -> int:
        """Время в минутах с полуночи — для сравнений и сортировки."""
        hours, minutes = self._start.split(":")
        return int(hours) * 60 + int(minutes)

    @property
    def room(self) -> str:
        return self._room

    # --- валидация при создании ---

    @staticmethod
    def _validate_subject(subject: str) -> str:
        subject = subject.strip()
        if not subject:
            raise ValueError("предмет не может быть пустым")
        return subject

    @staticmethod
    def _validate_start(start: str) -> str:
        parts = start.split(":")
        if len(parts) != 2:
            raise ValueError(f"некорректное время: {start!r} (ожидается ЧЧ:ММ)")
        hours, minutes = int(parts[0]), int(parts[1])
        if not (0 <= hours <= 23 and 0 <= minutes <= 59):
            raise ValueError(f"время вне диапазона: {start!r}")
        return f"{hours:02d}:{minutes:02d}"

    @staticmethod
    def _validate_room(room: str) -> str:
        room = room.strip()
        if not room:
            raise ValueError("аудитория не может быть пустой")
        return room

    def starts_at(self, start: str) -> bool:
        return self._start == Lesson._validate_start(start)

    def same_subject(self, subject: str) -> bool:
        return self._subject.casefold() == subject.strip().casefold()

    def __str__(self) -> str:
        return f"{self._start}  {self._subject} — ауд. {self._room}"


class Schedule:
    """Расписание дня: коллекция пар + операции над ней."""

    def __init__(self) -> None:
        self._lessons: list[Lesson] = []

    @property
    def size(self) -> int:
        return len(self._lessons)

    def add(self, lesson: Lesson) -> bool:
        """Добавляет пару. False — если пара с таким предметом уже есть."""
        if self.find_by_subject(lesson.subject) is not None:
            return False
        self._lessons.append(lesson)
        return True

    def remove_by_subject(self, subject: str) -> bool:
        """Удаляет пару по предмету. False — если предмет не найден."""
        for i, lesson in enumerate(self._lessons):
            if lesson.same_subject(subject):
                del self._lessons[i]
                return True
        return False

    def find_by_subject(self, subject: str) -> Lesson | None:
        for lesson in self._lessons:
            if lesson.same_subject(subject):
                return lesson
        return None

    def find_at_time(self, start: str) -> Lesson | None:
        """Находит пару, начинающуюся в указанное время (или None)."""
        wanted = Lesson._validate_start(start)
        for lesson in self._lessons:
            if lesson.starts_at(wanted):
                return lesson
        return None

    def sorted_lessons(self) -> list[Lesson]:
        """Пары по возрастанию времени (исходный порядок не меняется)."""
        return sorted(self._lessons, key=lambda lesson: lesson.start_minutes)

    def __str__(self) -> str:
        if not self._lessons:
            return "  (расписание пусто)"
        return "\n".join(f"  {lesson}" for lesson in self.sorted_lessons())


# ---------- Демонстрационный сценарий ----------

def demo(title: str, actions: list) -> None:
    """Прогоняет один набор действий и печатает итоговое расписание."""
    schedule = Schedule()
    print(f"\n=== {title} ===")
    for action in actions:
        op = action[0]
        if op == "add":
            try:
                ok = schedule.add(Lesson(action[1], action[2], action[3]))
                note = "ok" if ok else "отклонено (предмет уже есть)"
            except ValueError as exc:
                note = f"ошибка: {exc}"
            print(f"добавить {action[1]!r} {action[2]} -> {note}")
        elif op == "del":
            ok = schedule.remove_by_subject(action[1])
            print(f"удалить предмет {action[1]!r} -> {'удалено' if ok else 'не найдено'}")
        elif op == "find":
            lesson = schedule.find_at_time(action[1])
            print(f"поиск на {action[1]} -> {lesson if lesson else 'ничего не найдено'}")
    print("Итоговое расписание:")
    print(schedule)


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

    demo("Пример 3: ошибка валидации и пустое расписание", [
        ("add", "Английский", "25:99", "12"),  # некорректное время
        ("find", "08:30"),
        ("del", "Физика"),
    ])
