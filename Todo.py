import time
import threading

class Task:
    def __init__(self, description, category="Общее", priority=3, reminder_time=None):
        self.description = description
        self.category = category
        self.priority = priority  # 1 - Высокий, 2 - Средний, 3 - Низкий
        self.completed = False
        self.reminder_time = reminder_time
        if reminder_time:
            threading.Thread(target=self.set_reminder, daemon=True).start()

    def mark_completed(self):
        self.completed = True

    def set_reminder(self):
        time.sleep(self.reminder_time)
        if not self.completed:
            print(f"\n🔔⌚️ Напоминание: {self.description} (Категория: {self.category})")

    def __str__(self):
        status = "✅" if self.completed else "❌"
        priority_map = {1: "🔴 Высокий", 2: "🟠 Средний", 3: "🟢 Низкий"}
        return f"{status} [{self.category}] ({priority_map[self.priority]}) {self.description}"


class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, description, category="Общее", priority=3, reminder_time=None):
        self.tasks.append(Task(description, category, priority, reminder_time))
        print(f"Задача '{description}' добавлена в категорию '{category}' с приоритетом {priority}.")

    def mark_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()
            print(f"Задача '{self.tasks[index].description}' выполнена.")
        else:
            print("Ошибка: Неверный индекс задачи.")

    def show_tasks(self, show_completed=None, category=None):
        filtered_tasks = [
            (i, task)
            for i, task in enumerate(self.tasks)
            if (show_completed is None or task.completed == show_completed)
            and (category is None or task.category.lower() == category.lower())
        ]

        if not filtered_tasks:
            print("Нет задач.")
        else:
            for i, task in sorted(filtered_tasks, key=lambda t: t[1].priority):
                print(f"{i}. {task}")

    def run(self):
        while True:
            print("\nВыберите действие:")
            print("1. Добавить задачу")
            print("2. Отметить задачу как выполненную")
            print("3. Показать список задач")
            print("4. Выйти")

            command = input("Введите номер действия: ").strip()

            if command == "1":
                desc = input("Введите описание задачи: ").strip()
                
                print("Выберите категорию:")
                print("1. 💼 Работа")
                print("2. 👀 Личные дела")
                print("3. 😁 Другое")
                category_choice = input("Введите номер категории: ").strip()
                category_map = {"1": "Работа", "2": "Личные дела", "3": "Другое"}
                category = category_map.get(category_choice, "Другое")

                print("Выберите приоритет:")
                print("1. 🔴 Высокий")
                print("2. 🟠 Средний")
                print("3. 🟢 Низкий")
                priority_choice = input("Введите номер приоритета: ").strip()
                try:
                    priority = int(priority_choice)
                    if priority not in [1, 2, 3]:
                        raise ValueError
                except ValueError:
                    print("Ошибка: Приоритет должен быть 1, 2 или 3.")
                    continue

                print("Хотите установить напоминание?")
                print("1. ✅ Да")
                print("2. ❌ Нет")
                reminder_choice = input("Введите номер: ").strip()
                reminder_time = None
                if reminder_choice == "1":
                    try:
                        reminder_time = int(input("Напоминание через (секунды): ").strip())
                    except ValueError:
                        print("Ошибка: Введите число.")
                        continue

                self.add_task(desc, category, priority, reminder_time)

            elif command == "2":
                try:
                    index = int(input("Введите номер задачи: "))
                    self.mark_completed(index)
                except ValueError:
                    print("Ошибка: Введите число.")

            elif command == "3":
                print("\nВыберите фильтр задач:")
                print("1. Все задачи")
                print("2. Только выполненные")
                print("3. Только невыполненные")
                print("4. По категории")

                filter_option = input("Введите номер фильтра: ").strip()

                if filter_option == "2":
                    self.show_tasks(True)
                elif filter_option == "3":
                    self.show_tasks(False)
                elif filter_option == "4":
                    print("Выберите категорию:")
                    print("1. 💼 Работа")
                    print("2. 👀 Личные дела")
                    print("3. 😁 Другое")
                    category_choice = input("Введите номер категории: ").strip()
                    category_map = {"1": "Работа", "2": "Личные дела", "3": "Другое"}
                    category = category_map.get(category_choice, None)
                    self.show_tasks(category=category)
                else:
                    self.show_tasks()

            elif command == "4":
                print("Выход из программы.")
                break

            else:
                print("Ошибка: Неверный ввод.")

if __name__ == "__main__":
    ToDoList().run()
