print("Hi..")
# import pymysql

# connection = pymysql.connect(
#     host="127.0.0.1",
#     user="root",
#     password="Mysql@0195",
#     database="attendance_db"
# )

# print("Connection successful!")
# connection.close()

import mysql.connector
global cnx

cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Mysql@0195",
    database="pandeyji_eatery"
)

print(cnx)

# cursor = cnx.cursor()

# print(cursor)