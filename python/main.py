import psycopg2
from users import handle_users
from groups import handle_groups
from channels import handle_channels
import sys


def handle_cmd(cmd, ):
    tmp = cmd.split()
    if tmp[0].lower() == "users":
        handle_users(cmd, conn)
    elif tmp[0].lower() == "groups":
        handle_groups(cmd, conn)
    elif tmp[0].lower() == "channels":
        handle_channels(cmd, conn)


def show_result(res):
    pass


conn = psycopg2.connect(database="project", user="asus-pc", password="1", host="127.0.0.1", port="5432")
# conn.autocommit = True
cur = conn.cursor()
# cur.execute("CREATE DATABASE Project")

# print("please enter your tel number: +", end="")
# user_tel_number = input()
# input_cmd = "users addUser 7464-dhdhf-dfs-df"
# input_cmd = "users checkUserExistence 7464"
# input_cmd = "users getProfile 1"
# input_cmd = "users addPmChat 2 - alo2 - www.wiki.com - image - 1"
# input_cmd = "users getChatMessages 1 - 2"
# input_cmd = "users forwardPmChat 2 - 4 - 1 - 2"
# input_cmd = "groups addGroup dbzzz - 1"
# input_cmd = "users getGroups 1"
input_cmd = sys.argv[1]
res = handle_cmd(input_cmd)
# while True:
#     cmd = input()
#     if cmd == "exit":
#         break

    # res = handle_cmd(cmd)
    # if type == "query":
    #     show_result(res)

# cur.execute("SELECT id, name, address, salary  from COMPANY")
# rows = cur.fetchall()
# for row in rows:
#    print("ID = ", row[0])
#    print("NAME = ", row[1])
#    print("ADDRESS = ", row[2])
#    print("SALARY = ", row[3], "\n")

# conn.commit()
# print("Operation done successfully")
conn.close()
