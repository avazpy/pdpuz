# import psycopg2
#
#
# user_agent = ("Chrome Os"
#               "iPhone 14"
#               "1400 $")
#
#
# conn = psycopg2.connect(
#     dbname="pdp",
#     user="postgres",
#     password=1,
#     host="localhost",
#     port="5432"
# )
# cursor = conn.cursor()
#
# # Ma'lumotlar bazasida foydalanuvchi ma'lumotlarini saqlash
# cursor.execute("CREATE TABLE IF NOT EXISTS user_agents (id SERIAL PRIMARY KEY, user_agent TEXT)")
# cursor.execute("INSERT INTO user_agents (user_agent) VALUES (%s)", (user_agent,))
#
# conn.commit()
# conn.close()
#
# print("Ma'lumotlar bazasiga foydalanuvchi ma'lumotlari muvaffaqiyatli saqlandi.")
