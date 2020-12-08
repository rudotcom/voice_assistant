import pymysql

connection = pymysql.connect('localhost', 'dude', 'StqMwx4DRdKrc6WWGcw2w8nZh', 'assistant')

# try:
    # with connection.cursor() as cursor:
    #     # Create a new record
    #     sql = "INSERT INTO `citation` (`quoteText`, `quoteAuthor`) VALUES (%s, %s)"
    #     cursor.execute(sql, (quote_text, quote_author))
    #
    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()

