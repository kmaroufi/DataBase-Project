import datetime
import psycopg2
from util import *

conn = None
cur = None
user_tel_number = None


def handle_users(cmd, db_conn):
    global conn, cur, user_tel_number
    conn = db_conn
    cur = conn.cursor()
    tmp = cmd.split()
    task = tmp[1]
    if task == "checkUserExistence":
        return check_user_existence(cmd)
    if task == "addUser":
        return add_user(cmd)
    if task == "alterUser":
        return alter_user(cmd)
    if task == "updateLastSeen":
        return update_last_seen(cmd)
    if task == "addContact":
        return add_contact(cmd)
    if task == "addBlockedContact":
        return add_blocked_contact(cmd)
    if task == "addPmChat":
        return add_pm_chat(cmd)
    if task == "forwardPmChat":
        return forward_pm_chat(cmd)
    if task == "addGroupMembership":
        return add_group_membership(cmd)  # /
    if task == "addChannelSubscribe":
        return add_channel_subscribe(cmd)  # /
    if task == "rmContact":
        return rm_contact(cmd)
    if task == "rmBlockedContact":
        return rm_blocked_contact(cmd)
    if task == "rmPmChat":
        return rm_pm_chat(cmd)
    if task == "rmGroupMembership":
        return rm_group_membership(cmd)  # /
    if task == "rmChannelSubscribe":
        return rm_channel_subscribe(cmd)  # /
    if task == "addPic":
        return add_pic(cmd)
    if task == "rmPic":
        return rm_pic(cmd)
    if task == "getProfile":
        return get_profile(cmd)
    if task == "getPics":
        return get_pics(cmd)
    if task == "getContacts":
        return get_contacts(cmd)
    if task == "getBlockedContacts":
        return get_blocked_contacts(cmd)
    if task == "getChatMessages":
        return get_chat_messages(cmd)
    if task == "getChats":
        return get_chats(cmd)
    if task == "getGroups":
        return get_groups(cmd)
    if task == "getChannels":
        return get_channels(cmd)
    print("unknown command!")
    return


def check_user_existence(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    res = execute("SELECT * FROM user_table WHERE tel_number=(%s)", (tel_number,))
    if res:
        rows = cur.fetchall()
        if len(rows) == 1:
            print("1")
        else:
            print("0")
    return True


def add_user(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    user_name = params[1]
    name = params[2]
    last_name = params[3]
    res = execute(
        "INSERT INTO user_table(tel_number, user_name, name, last_name) VALUES(%s, %s, %s, %s)",
        (tel_number, user_name, name, last_name))

    if res:
        print(1)
        conn.commit()
    return True


def alter_user(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    user_name = params[1]
    name = params[2]
    last_name = params[3]
    if tel_number == "":
        print("telnumber is null")
        return False
    res1, res2, res3 = False, False, False
    if user_name != "":
        res1 = execute("UPDATE user_table SET user_name=%s WHERE tel_number=%s", (user_name, tel_number))
        if res1 and name != "":
            res2 = execute("UPDATE user_table SET name=%s WHERE tel_number=%s", (name, tel_number))
            if res2 and last_name != "":
                res3 = execute("UPDATE user_table SET last_name=%s WHERE tel_number=%s", (last_name, tel_number))
    if res1 and res2 and res3:
        print(1)
        conn.commit()
    else:
        conn.rollback()
    return True


def update_last_seen(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    last_seen = datetime.datetime.now()
    if tel_number == "":
        print("telnumber is null")
        return False
    execute("UPDATE user_table SET last_seen=%s WHERE tel_number=%s", (last_seen, tel_number))
    conn.commit()
    return True


def add_contact(cmd):
    params = splitter(cmd)
    tel_number1 = params[0]
    tel_number2 = params[1]
    contact_name = params[2]
    if execute("SELECT * FROM user_table WHERE tel_number=%s", (tel_number2,)):
        if len(cur.fetchall()) == 0:
            print("0")
            print("that tel number doesn't exist!")
            return
        if execute("INSERT INTO contacts_table VALUES (%s, %s, %s)", (tel_number1, tel_number2, contact_name)):
            print(1)
            conn.commit()
    return True


def add_blocked_contact(cmd):
    params = splitter(cmd)
    tel_number1 = params[0]
    tel_number2 = params[1]
    if execute("SELECT * FROM user_table WHERE tel_number=%s", (tel_number2,)):
        if len(cur.fetchall()) == 0:
            print("0")
            print("that tel number doesn't exist!")
            return
        if execute("INSERT INTO blocked_contacts_table VALUES (%s, %s)", (tel_number1, tel_number2)):
            print(1)
            conn.commit()
    return True


def add_pm_chat(cmd):
    params = splitter(cmd)
    cs_tel_number = params[0]
    text = params[1]
    file_address = params[2]
    type = params[3]
    r_tel_number = params[4]
    message_id = -1
    upload_time = datetime.datetime.now()
    # first, find out message_id
    execute("SELECT MAX(message_id) FROM message_table WHERE creator_tel_number=%s", (cs_tel_number))
    rows = cur.fetchall()
    if len(rows) > 1:
        print(0)
        print("add_pm_chat: strange error")
        return
    elif rows[0][0] is not None:
        message_id = int(rows[0][0]) + 1
    else:
        message_id = 1

    if file_address != "":
        if execute("SELECT * FROM media_table WHERE file_address=%s", (file_address,)):
            if len(cur.fetchall()) == 0:
                if not execute("INSERT INTO media_table(file_address, type) VALUES (%s, %s)", (file_address, 'image')):
                    return
        else:
            return
    else:
        file_address = None

    if execute(
            "INSERT INTO message_table(creator_tel_number, message_id, message_text, media_address) VALUES (%s, %s, %s, %s)",
            (cs_tel_number, message_id, text, file_address)):
        if execute(
                "INSERT INTO chat_table(sender_tel_number, receiver_tel_number, creator_tel_number, message_id, seen) VALUES (%s, %s, %s, %s, %s)",
                (cs_tel_number, r_tel_number, cs_tel_number, message_id, False)):
            print(1)
            conn.commit()

    return True


def forward_pm_chat(cmd):
    params = splitter(cmd)
    c_tel_number = params[0]
    message_id = params[1]
    s_tel_number = params[2]
    r_tel_number = params[3]

    if execute("SELECT * FROM message_table WHERE creator_tel_number=%s AND message_id=%s", (c_tel_number, message_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("this message doesn't exist!")
            return
    else:
        return

    if execute(
            "INSERT INTO chat_table(sender_tel_number, receiver_tel_number, creator_tel_number, message_id, seen) VALUES (%s, %s, %s, %s, %s)",
            (s_tel_number, r_tel_number, c_tel_number, message_id, False)):
        print(1)
        conn.commit()
    return True


def add_group_membership(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    group_id = params[2]
    if tel_number == tel_number2:
        if execute("INSERT INTO membership_table VALUES (%s, %s)", (tel_number, group_id)):
            print(1)
    else:
        if execute(
                "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
                (tel_number, group_id, True)):
            if len(cur.fetchall()) == 1:
                if execute("INSERT INTO membership_table (tel_number, group_id) VALUES (%s, %s)",
                           (tel_number2, group_id)):
                    print(1)
            else:
                print(0)
                print("you are not admin!")

    return True


def add_channel_subscribe(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    channel_id = params[2]
    if tel_number == tel_number2:
        if execute("INSERT INTO subscribe_table VALUES (%s, %s)", (tel_number, channel_id)):
            print(1)
    else:
        if execute(
                "SELECT * FROM subscribe_table WHERE tel_number=%s AND channel_id=%s AND is_admin=%s",
                (tel_number, channel_id, True)):
            if len(cur.fetchall()) == 1:
                if execute("INSERT INTO subscribe_table (tel_number, channel_id) VALUES (%s, %s)",
                           (tel_number2, channel_id)):
                    print(1)
            else:
                print(0)
                print("you are not admin!")

    return True


def rm_contact(cmd):
    params = splitter(cmd)
    tel_number1 = params[0]
    tel_number2 = params[1]
    if execute("SELECT * FROM user_table WHERE tel_number=%s", (tel_number2,)):
        if len(cur.fetchall()) == 0:
            print("0")
            print("that tel number doesn't exist!")
            return
        if execute("DELETE FROM contacts_table WHERE tel_number=%s AND contact_tel_number=%s",
                   (tel_number1, tel_number2)):
            print(1)
            conn.commit()
    return True


def rm_blocked_contact(cmd):
    params = splitter(cmd)
    tel_number1 = params[0]
    tel_number2 = params[1]
    if execute("SELECT * FROM user_table WHERE tel_number=%s", (tel_number2,)):
        if len(cur.fetchall()) == 0:
            print("0")
            print("that tel number doesn't exist!")
            return
        if execute("DELETE FROM blocked_contacts_table WHERE tel_number=%s AND contact_tel_number=%s",
                   (tel_number1, tel_number2)):
            print(1)
            conn.commit()
    return True


def rm_pm_chat(cmd):
    params = splitter(cmd)
    s_tel_number = params[0]
    r_tel_number = params[1]
    c_tel_number = params[2]
    message_id = params[3]
    send_time = params[4]

    if execute('''DELETE FROM chat_table WHERE sender_tel_number=%s
            AND chat_table.receiver_tel_number=%s
            AND chat_table.creator_tel_number=%s
            AND chat_table.message_id=%s
            AND chat_table.send_time=%s''', (s_tel_number, r_tel_number, c_tel_number, message_id, send_time)):
        print(1)
    return True


def rm_group_membership(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    group_id = params[2]
    if tel_number == tel_number2:
        if execute("DELETE FROM membership_table VALUES (%s, %s)", (tel_number, group_id)):
            print(1)
    else:
        if execute(
                "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
                (tel_number, group_id, True)):
            if len(cur.fetchall()) == 1:
                if execute("DELETE FROM membership_table (tel_number, group_id) VALUES (%s, %s)",
                           (tel_number2, group_id)):
                    print(1)
            else:
                print(0)
                print("you are not admin!")

    return True


def rm_channel_subscribe(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    channel_id = params[2]
    if tel_number == tel_number2:
        if execute("DELETE FROM subscribe_table VALUES (%s, %s)", (tel_number, channel_id)):
            print(1)
    else:
        if execute(
                "SELECT * FROM subscribe_table WHERE tel_number=%s AND channel_id=%s AND is_admin=%s",
                (tel_number, channel_id, True)):
            if len(cur.fetchall()) == 1:
                if execute("DELETE FROM subscribe_table (tel_number, channel_id) VALUES (%s, %s)",
                           (tel_number2, channel_id)):
                    print(1)
            else:
                print(0)
                print("you are not admin!")

    return True


def add_pic(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    file_address = params[1]

    execute("SELECT * FROM media_table WHERE file_address=%s", (file_address,))
    if len(cur.fetchall()) == 0:
        res = execute("INSERT INTO media_table(file_address, type) VALUES(%s, %s)", (file_address, 'image'))
        if not res:
            return
        res = execute("INSERT INTO image_table(file_address) VALUES(%s)", (file_address,))
        if not res:
            conn.rollback()
            return

    res = execute("INSERT INTO user_profile_table(tel_number, image_address) VALUES(%s, %s)",
                  (tel_number, file_address))
    if res:
        print(1)
        conn.commit()
    else:
        conn.rollback()

    return True


def rm_pic(cmd):
    # TODO
    params = splitter(cmd)
    tel_number = params[0]
    image_address = params[1]
    date = params[2]

    res = execute("DELETE FROM user_profile_table WHERE tel_number=%s AND image_address=%s AND date=%s",
                  (tel_number, image_address, datetime._build_struct_time(2018)))
    if res:
        print(1)
        conn.commit()
    else:
        conn.rollback()
    return True


def get_profile(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    execute("SELECT * FROM user_profile_view WHERE tel_number=%s", (tel_number))
    rows = cur.fetchall()
    if len(rows) == 1:
        for item in rows[0]:
            print(item, end="-")
    else:
        print("0")
    return True


def get_pics(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    execute("SELECT * FROM user_profile_table WHERE tel_number=%s", (tel_number))
    rows = cur.fetchall()
    print("1")
    print(len(rows))
    for row in rows:
        for item in row:
            print(item, end="-")
        print()
    else:
        print("0")
    return True


def get_contacts(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    res = execute("SELECT contact_tel_number, contact_name FROM contacts_table WHERE tel_number=%s",
                  (tel_number,))
    if res:
        rows = cur.fetchall()
        print("1")
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end="-")
            print()
    else:
        print("0")
    return True


def get_blocked_contacts(cmd):
    params = splitter(cmd)
    tel_number = params[0]

    res = execute("SELECT contact_tel_number FROM blocked_contacts_table WHERE tel_number=%s",
                  (tel_number,))
    if res:
        rows = cur.fetchall()
        print("1")
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end="-")
            print()
    else:
        print("0")
    return True


def get_chat_messages(cmd):
    params = splitter(cmd)
    tel_number1 = params[0]
    tel_number2 = params[1]

    u_res = []

    if execute("SELECT * FROM chat_view WHERE receiver_tel_number=%s AND sender_tel_number=%s",
               (tel_number2, tel_number1)):
        for tl in cur.fetchall():
            u_res.append(tl)
        if execute("SELECT * FROM chat_view WHERE sender_tel_number=%s AND receiver_tel_number=%s",
                   (tel_number2, tel_number1)):
            for tl in cur.fetchall():
                u_res.append(tl)
            print(1)
            print(len(u_res))
            for tl in u_res:
                for item in tl:
                    print(item, end=";")
                print()
        return True


def get_chats(cmd):
    params = splitter(cmd)
    tel_number1 = params[0]

    u_res = {0}
    u_res.remove(0)

    if execute("SELECT receiver_tel_number FROM chat_table WHERE sender_tel_number=%s", (tel_number1,)):
        for tl in cur.fetchall():
            u_res.add(tl[0])
        if execute("SELECT sender_tel_number FROM chat_table WHERE receiver_tel_number=%s", (tel_number1,)):
            for tl in cur.fetchall():
                u_res.add(tl[0])
            print(1)
            print(len(u_res))
            for tl in u_res:
                print(tl)

    return True


def get_groups(cmd):
    params = splitter(cmd)
    tel_number = params[0]

    if execute("SELECT * FROM group_list_view WHERE tel_number=%s", (tel_number,)):
        rows = cur.fetchall()
        print(1)
        print(len(rows))
        for row in rows:
            for x in row:
                print(x, end=";")
            print()
    return True


def get_channels(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    return True


def execute(sql_cmd, args):
    try:
        cur.execute(sql_cmd, args)
        return True
    except Exception as e:
        x = 0
        print("0")
        print(e)
        return False
