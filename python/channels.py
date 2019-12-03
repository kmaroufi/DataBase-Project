from util import *

conn = None
cur = None
user_tel_number = None


def handle_channels(cmd, db_conn):
    global conn, cur, user_tel_number
    conn = db_conn
    cur = conn.cursor()
    tmp = cmd.split()
    task = tmp[1]
    if task == "addChannel":
        return add_channel(cmd)
    if task == "alterChannel":
        return alter_channel(cmd)
    if task == "rmChannel":
        return rm_channel(cmd)
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
    if task == "addPmChannel":
        return add_pm_channel(cmd)
    if task == "addForwardedPmChannel":
        return add_forwarded_pm_channel(cmd)
    if task == "rmPmChannel":
        return rm_pm_channel(cmd)
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
    if task == "getPmChannels":
        return get_pm_channels(cmd)
    if task == "addPin":
        return add_pin(cmd)
    if task == "rmPin":
        return rm_pin(cmd)
    if task == "getPin":
        return get_pin(cmd)
    print("unknown command!")
    return


def add_channel(cmd):
    params = splitter(cmd)
    name = params[0]
    c_tel_number = params[1]
    channel_id = params[2]

    if execute("INSERT INTO channel_table (channel_id, name, creator_tel_number) VALUES (%s, %s, %s)",
               (channel_id, name, c_tel_number)):
        print(1)
        conn.commit()
    return True


def alter_channel(cmd):
    params = splitter(cmd)
    name = params[0]
    return True


def rm_channel(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    channel_id = params[1]

    if execute(
            "SELECT * FROM channel_creator_view WHERE channel_id = %s AND tel_number=%s",
            (channel_id, tel_number)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not creator!")
            return

    if execute("DELETE FROM channel_table WHERE channel_id = %s", (channel_id,)):
        print(1)
        conn.commit()
    return True


def add_blocked_user(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    channel_id = params[2]

    if execute(
            "SELECT tel_number FROM subscribe_table WHERE channel_id = %s AND is_admin = TRUE AND tel_number=%s",
            (channel_id, tel_number)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not admin!")
            return

    if execute("INSERT INTO channel_blocked_users_table (tel_number, channel_id) VALUES (%s, %s)", (tel_number2, channel_id)):
        print(1)
        conn.commit()
    return True


def rm_blocked_user(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    tel_number2 = params[1]
    channel_id = params[2]

    if execute(
            "SELECT tel_number FROM subscribe_table WHERE channel_id = %s AND is_admin = TRUE AND tel_number=%s",
            (channel_id, tel_number)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not admin!")
            return

    if execute("DELETE FROM channel_blocked_users_table WHERE channel_id = %s AND tel_number = %s", (channel_id, tel_number2)):
        print(1)
        conn.commit()
    return True


def add_admin(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    channel_id = params[1]
    return True


def rm_admin(cmd):
    params = splitter(cmd)
    tel_number = params[0]
    channel_id = params[1]
    return True


def add_pic(cmd):
    params = splitter(cmd)
    channel_id = params[0]
    file_address = params[1]
    return True


def rm_pic(cmd):
    params = splitter(cmd)
    channel_id = params[0]
    media_id = params[1]
    date = params[2]
    return True


def add_pm_channel(cmd):
    params = splitter(cmd)
    cs_tel_number = params[0]
    channel_id = params[1]
    text = params[2]
    file_address = params[3]
    type = params[4]
    message_id = -1
    if execute(
            "SELECT * FROM subscribe_table WHERE tel_number=%s AND channel_id=%s AND is_admin=TRUE",
            (cs_tel_number, channel_id)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not admin!")
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
                "INSERT INTO channel_sends_table(tel_number, channel_id, creator_tel_number, message_id) VALUES (%s, %s, %s, %s)",
                (cs_tel_number, channel_id, cs_tel_number, message_id)):
            print(1)
            conn.commit()

    return True


def add_forwarded_pm_channel(cmd):
    params = splitter(cmd)
    s_tel_number = params[0]
    channel_id = params[1]
    c_tel_number = params[2]
    message_id = params[3]
    if execute(
            "SELECT * FROM subscribe_table WHERE tel_number=%s AND channel_id=%s AND is_admin=TRUE",
            (s_tel_number, channel_id)):
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
            "INSERT INTO channel_sends_table(tel_number, channel_id, creator_tel_number, message_id) VALUES (%s, %s, %s, %s)",
            (s_tel_number, channel_id, c_tel_number, message_id)):
        print(1)
        conn.commit()
    return True


def rm_pm_channel(cmd):
    params = splitter(cmd)
    s_tel_number = params[0]
    channel_id = params[1]
    c_tel_number = params[2]
    message_id = params[3]
    send_time = params[4]
    return True


def add_seen(cmd):
    params = splitter(cmd)
    s_tel_number = params[0]
    channel_id = params[1]
    c_tel_number = params[2]
    message_id = params[3]
    send_time = params[4]
    v_tel_number = params[5]
    return True


def get_profile(cmd):
    params = splitter(cmd)
    channel_id = params[0]

    if execute("SELECT * FROM channel_profile_view WHERE channel_id = %s", (channel_id,)):
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
    channel_id = params[1]

    if execute(
            "SELECT tel_number FROM subscribe_table WHERE channel_id = %s AND is_admin = TRUE AND tel_number=%s",
            (channel_id, tel_number)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not admin!")
            return

    if execute("SELECT * FROM channel_subscribes_view WHERE channel_id = %s", (channel_id,)):
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
    channel_id = params[1]

    if execute(
            "SELECT tel_number FROM subscribe_table WHERE channel_id = %s AND is_admin = TRUE AND tel_number=%s",
            (channel_id, tel_number)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not admin!")
            return

    if execute("SELECT * FROM channel_blocked_view WHERE channel_id = %s", (channel_id,)):
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
    channel_id = params[1]

    if execute(
            "SELECT tel_number FROM subscribe_table WHERE channel_id = %s AND is_admin = TRUE AND tel_number=%s",
            (channel_id, tel_number)):
        if len(cur.fetchall()) == 0:
            print(0)
            print("you are not admin!")
            return

    if execute("SELECT * FROM channel_subscribes_view WHERE channel_id = %s AND is_admin = TRUE", (channel_id,)):
        print(1)
        rows = cur.fetchall()
        print(len(rows))
        for row in rows:
            for item in row:
                print(item, end=";")
            print()
    return True


def get_pm_channels(cmd):
    params = splitter(cmd)
    channel_id = params[0]

    if execute("SELECT * FROM channel_messages_view WHERE channel_id = %s", (channel_id,)):
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
    channel_id = params[0]
    c_tel_number = params[1]
    message_id = params[2]
    send_time = params[3]
    s_tel_number = params[4]
    return True


def rm_pin(cmd):
    params = splitter(cmd)
    channel_id = params[0]
    c_tel_number = params[1]
    message_id = params[2]
    send_time = params[3]
    s_tel_number = params[4]
    return True


def get_pin(cmd):
    params = splitter(cmd)
    channel_id = params[0]

    if execute("SELECT * FROM channel_messages_view WHERE channel_id = %s", (channel_id,)):
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
