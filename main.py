class Task():
    tasks = []

    def __init__(self, opis, srok, status=False):
        self.opis = opis
        self.srok = srok
        self.status = status
        Task.tasks.append(self)

    def add_task(self, opis, srok):
        Task(opis, srok)

    def mark_completed(self):
        self.status = True

    def show_current_tasks(self):
        for task in Task.tasks:
            if task.status == False:
                print(f"Описание: {task.opis}, Срок: {task.srok}")


manager = Task("", "")
manager.add_task("Купить молоко", "2024-01-15")
manager.add_task("Сделать уроки", "2024-01-16")
manager.add_task("Позвонить маме", "2024-01-17")

Task.tasks[1].mark_completed()
manager.show_current_tasks()