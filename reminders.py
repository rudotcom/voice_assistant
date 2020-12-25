
""" 
Получить из бд список напоминаний на текущее время (дату, день недели)
у которых дата-время "напомнено" не моложе времени заданного напоминания
По списку выдать текст напоминания и пометить как напомненное
    CREATE TABLE `reminders` (
    `id` SMALLINT AUTO_INCREMENT PRIMARY NOT NULL,
    `date` DATE() NULL,
    `weekday` SET(... дни недели ...) NULL,
    `time` TIME NOT NULL,
    `text` TEXT NOT NULL
    );
Таблица "Напомнено"
    CREATE TABLE `reminded` (
    `id` SMALLINT() PRIMARY NOT NULL,
    `time_reminded` TIMESTAMP() NULL,
    );
"""


def db_get_reminder():
    pass
