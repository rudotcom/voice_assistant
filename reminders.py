"""
Получить из бд список напоминаний на текущее время (дату, день недели)
у которых дата-время "напомнено" не моложе времени заданного напоминания
По списку выдать текст напоминания и пометить как напомненное

"""
import pymysql
from APIKeysLocal import mysql_pass as pwd


def db_get_reminder():
    """ SQL по дню недели: """
    sql = 'SELECT reminders.id, text, time_reminded FROM reminders LEFT JOIN reminded ON reminders.id=reminded.id \
           WHERE weekday & POW(2, WEEKDAY(CURDATE())) AND time < CURTIME() \
           AND (time_reminded IS NULL OR DATE(time_reminded) < CURDATE());'
    sql_insert = 'INSERT INTO reminded (id, time_reminded) VALUES ({}, CURTIME()) ' \
                 'ON DUPLICATE KEY UPDATE time_reminded=CURTIME();'
    connection = pymysql.connect('localhost', 'assistant', pwd, 'assistant')
    reminders = []
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            for result in results:
                reminders.append(result[1])
                # print(sql_insert.format(result[0]))
                cursor.execute(sql_insert.format(result[0]))
                connection.commit()
    finally:
        connection.close()
    return reminders
