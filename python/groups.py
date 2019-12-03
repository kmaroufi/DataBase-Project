from util import *

conn = None
cur = None
user_tel_number = None


def handle_groups(cmd, db_conn):
    global conn, cur, user_tel_number
    conn = db_conn
    cur = conn.cursor()
    tmp = cmd.split()
    task = tmp[1]
    if task == "addGroup":
        return add_group(cmd)  # /
    if task == "alterGroup":
        return alter_group(cmd)
    if task == "rmGroup":
        return rm_group(cmd)
    if task == "addBlockedUser":
        return add_blocked_user(cmd)
    if task == "rmBlockedUser":
        return rm_blocked_user(cmd)
    if task == "addAdmin":
        return add_admin(cmd)
    if task == "rmAdmin":
        return rm_admin(cmd)
    if task == "addPic":
        return add_pic(cmd)
    if task == "addUploadedPic":
        return add_uploaded_pic(cmd)
    if task == "rmPic":
        return rm_pic(cmd)
    if task == "addPmGroup":
        return add_pm_group(cmd)
    if task == "addForwardedPmGroup":
        return add_forwarded_pm_group(cmd)
    if task == "rmPmGroup":
        return rm_pm_group(cmd)
    if task == "addSeen":
        return add_seen(cmd)
    if task == "getProfile":
        return get_profile(cmd)
    if task == "getUsers":
        return get_users(cmd)
    if task == "getBlockedUsers":
        return get_blocked_users(cmd)
    if task == "getAdminUsers":
        return get_admin_users(cmd)
    if task == "getPmGroups":
        return get_pm_groups(cmd)
    if task == "addPin":
        return add_pin(cmd)
    if task == "rmPin":
        return rm_pin(cmd)
    if task == "getPin":
        return get_pin(cmd)
    if task == "getCreator":
        return get_creator(cmd)
    print("unknown command!")
    return


def add_group(cmd):
    params = splitter(cmd)
    name = params[0]
    c_tel_number = params[1]

    if execute("INSERT INTO group_table (name, creator_tel_number) VALUES (%s, %s)", (name, c_tel_number)):
        print(1)
        conn.commit()
    return True


def alter_group(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]
    name = params[2]

    # TODO

    # if execute("UPDATE group_table SET name=%s WHERE group_id=%s", (name, group_id)):

    return True


def rm_group(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute("SELECT creator_tel_number FROM group_creator_view WHERE creator_tel_number= %s AND group_id = %s",
               (tel_number, group_id)):
        if len(cur.fetchall()) == 1:
            if execute("DELETE FROM group_table WHERE group_id = %s", (group_id,)):
                print(1)
                conn.commit()
    else:
        print("you are not creator")
    return True


def add_blocked_user(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    group_id = params[2]

    if tel_number == tel_number2:
        print(0)
        print("what are you doing?")
    else:
        if execute(
                "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
                (tel_number, group_id, True)):
            if len(cur.fetchall()) == 1:
                if execute(
                        "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
                        (tel_number2, group_id, True)):
                    if len(cur.fetchall()) == 0:
                        if execute("INSERT INTO group_blocked_users_table (tel_number, group_id) VALUES (%s, %s)",
                                   (tel_number2, group_id)):
                            print(1)
                            conn.commit()
                    else:
                        print(0)
                        print("you can't block another admin!")
            else:
                print(0)
                print("you are not admin!")
    return True


def rm_blocked_user(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    group_id = params[2]

    if tel_number == tel_number2:
        print(0)
        print("what are you doing?")
    else:
        if execute(
                "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
                (tel_number, group_id, True)):
            if len(cur.fetchall()) == 1:
                if execute(
                        "DELETE FROM group_blocked_users_table (tel_number, group_id) WHERE (%s, %s)",
                        (tel_number2, group_id)):
                    print(1)
                    conn.commit()
                else:
                    print(0)
                    print("this person is not in blocked list!")
            else:
                print(0)
                print("you are not admin!")
    return True


def add_admin(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    group_id = params[2]

    if tel_number == tel_number2:
        print(0)
        print("what are you doing?")
    else:
        if execute(
                "SELECT creator_tel_number FROM group_creator_view WHERE creator_tel_number=%s AND group_id = %s",
                (tel_number, group_id)):
            if len(cur.fetchall()) == 1:
                if execute(
                        "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
                        (tel_number2, group_id)):
                    if len(cur.fetchall()) == 1:
                        if execute(
                                "UPDATE membership_table SET is_admin=TRUE WHERE group_id=%s AND tel_number=%s",
                                (group_id, tel_number2)):
                            print(1)
                            conn.commit()
                    else:
                        print(0)
                        print("this person is not in the group!")
            else:
                print(0)
                print("you are not group's creator!")
    return True


def rm_admin(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    group_id = params[2]

    if tel_number == tel_number2:
        print(0)
        print("what are you doing?")
    else:
        if execute(
                "SELECT creator_tel_number FROM group_creator_view WHERE creator_tel_number=%s AND group_id = %s",
                (tel_number, group_id)):
            if len(cur.fetchall()) == 1:
                if execute(
                        "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
                        (tel_number2, group_id, True)):
                    if len(cur.fetchall()) == 1:
                        if execute(
                                "UPDATE membership_table SET is_admin=FALSE WHERE group_id=%s AND tel_number=%s",
                                (group_id, tel_number2)):
                            print(1)
                            conn.commit()
                    else:
                        print(0)
                        print("this person is not an admin!")
            else:
                print(0)
                print("you are not group's creator!")
    return True


def add_pic(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]
    file_address = params[2]

    if execute("SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
               (tel_number, group_id, True)):
        if len(cur.fetchall()) == 1:
            if execute("SELECT * FROM media_table WHERE file_address=%s", (file_address,)):
                if len(cur.fetchall()) == 0:
                    res = execute("INSERT INTO media_table(file_address, type) VALUES(%s, %s)", (file_address, 'image'))
                    if not res:
                        return
                    res = execute("INSERT INTO image_table(file_address) VALUES(%s)", (file_address,))
                    if not res:
                        return
                if execute("INSERT INTO group_profile_table(group_id, image_address) VALUES(%s, %s)",
                           (group_id, file_address)):
                    print(1)
                    conn.commit()
        else:
            print(0)
            print("you are not group's admin!")
    return True


def rm_pic(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]
    file_address = params[2]
    date = params[3]

    if execute("SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s AND membership_table.is_admin=%s",
               (tel_number, group_id, True)):
        if len(cur.fetchall()) == 1:
            if execute("SELECT * FROM media_table WHERE file_address=%s", (file_address,)):
                if len(cur.fetchall()) == 0:
                    print(0)
                    print("this pic is not in data base!")
                if execute("DELETE FROM group_profile_table WHERE group_id=%s AND image_address=%s",
                           (group_id, file_address)):
                    print(1)
                    conn.commit()
        else:
            print(0)
            print("you are not group's admin!")
    return True


def add_pm_group(cmd):
    params = splitter(cmd)
    cs_tel_number = params[0]
    group_id = params[1]
    text = params[2]
    file_address = params[3]
    type = params[4]
    message_id = -1
    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (cs_tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return
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
                "INSERT INTO group_sends_table(tel_number, group_id, creator_tel_number, message_id) VALUES (%s, %s, %s, %s)",
                (cs_tel_number, group_id, cs_tel_number, message_id)):
            print(1)
            conn.commit()

    return True


def add_forwarded_pm_group(cmd):
    params = splitter(cmd)
    s_tel_number = params[0]
    group_id = params[1]
    c_tel_number = params[2]
    message_id = params[3]
    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (s_tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM message_table WHERE creator_tel_number=%s AND message_id=%s", (c_tel_number, message_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("this message doesn't exist!")
            return
    else:
        return

    if execute(
            "INSERT INTO group_sends_table(tel_number, group_id, creator_tel_number, message_id) VALUES (%s, %s, %s, %s)",
            (s_tel_number, group_id, c_tel_number, message_id)):
        print(1)
        conn.commit()
    return True


def rm_pm_group(cmd):
    params = splitter(cmd)
    s_tel_number = params[0]
    group_id = params[1]
    c_tel_number = params[2]
    message_id = params[3]
    send_time = params[4]
    return True


def add_seen(cmd):
    params = splitter(cmd)
    s_tel_number = params[0]
    group_id = params[1]
    c_tel_number = params[2]
    message_id = params[3]
    send_time = params[4]
    v_tel_number = params[5]
    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (v_tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("INSERT INTO group_seen_table (tel_number, group_id, creator_tel_number, message_id, send_time, viewer_tel_number) VALUES (%s, %s, %s, %s, %s, %s)",
               {s_tel_number, group_id, c_tel_number, message_id, send_time, v_tel_number}):
        print(1)
        conn.commit()
    return True

def get_profile(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM group_profile_view WHERE group_id = %s", (group_id, )):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
    return True


def get_users(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM group_members_view WHERE group_id = %s", (group_id,)):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
    return True


def get_blocked_users(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM group_blocked_view WHERE group_id = %s", (group_id,)):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
    return True


def get_admin_users(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM group_members_view WHERE group_id = %s AND is_admin = TRUE", (group_id,)):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
    return True


def get_pm_groups(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM group_messages_view WHERE group_id = %s", (group_id,)):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
    return True


def add_pin(cmd):
    params = splitter(cmd)
    group_id = params[0]
    c_tel_number = params[1]
    message_id = params[2]
    send_time = params[3]
    s_tel_number = params[4]
    return True


def rm_pin(cmd):
    params = splitter(cmd)
    group_id = params[0]
    c_tel_number = params[1]
    message_id = params[2]
    send_time = params[3]
    s_tel_number = params[4]
    return True


def get_pin(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM group_pin_view WHERE group_id = %s", (group_id,)):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
    return True


def get_creator(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    group_id = params[1]

    if execute(
            "SELECT * FROM membership_table WHERE tel_number=%s AND group_id=%s",
            (tel_number, group_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not in the group!")
            return

    if execute("SELECT * FROM group_creator_view WHERE group_id = %s", (group_id,)):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
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
