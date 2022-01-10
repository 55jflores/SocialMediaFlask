import sqlite3
# Creating the DB
conn = sqlite3.connect('socialMedia.db')
c = conn.cursor()


c.execute("""CREATE TABLE socialposts(
    username text,
    userimage text,
    usercaption text,
    the_datetime text
)
""")
conn.commit()
