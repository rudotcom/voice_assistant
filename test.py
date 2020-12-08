import pymysql

connection = pymysql.connect('localhost', 'dude', 'StqMwx4DRdKrc6WWGcw2w8nZh', 'assistant')

try:
    # with connection.cursor() as cursor:
    #     # Create a new record
    #     sql = "INSERT INTO `citation` (`quoteText`, `quoteAuthor`) VALUES (%s, %s)"
    #     cursor.execute(sql, (quote_text, quote_author))
    #
    # # connection is not autocommit by default. So you must commit to save
    # # your changes.
    # connection.commit()

import random,os,sys

folder=os.listdir(os.getcwd())
file=random.choice(folder)
ext3=['.mp3']
print('First random pick: '+file)

while file[-4:] not in ext3 :
    print('Not an MP3 file  : '+file)
    file=random.choice(folder)
else:
    os.startfile(file)
    print('Song name: '+file)

sys.exit()

##os.startfile(random.choice(folder))