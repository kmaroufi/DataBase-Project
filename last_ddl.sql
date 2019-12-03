CREATE DOMAIN PHONE VARCHAR(16) CHECK (VALUE ~ '^[0-9]+$');

CREATE DOMAIN CHARNAME VARCHAR(32);

CREATE DOMAIN TIMEDATE TIMESTAMP DEFAULT now();

CREATE SEQUENCE GROUPIDSEQ;
CREATE DOMAIN GROUPID INT DEFAULT NEXTVAL('GROUPIDSEQ') NOT NULL;

CREATE DOMAIN NUMBER BIGINT DEFAULT 0 CHECK (VALUE >= 0);

CREATE DOMAIN ADDRESS VARCHAR(64);

CREATE DOMAIN MEDIATYPE CHAR(5)
  CHECK (VALUE IN ('video', 'audio', 'image'));


CREATE TABLE user_table(
  tel_number PHONE,
  user_name CHARNAME UNIQUE,
  name CHARNAME NOT NULL,
  last_name CHARNAME,
  last_seen TIMEDATE,
  PRIMARY KEY (tel_number)
);

CREATE TABLE contacts_table(
  tel_number PHONE,
  contact_tel_number PHONE,
  contact_name CHARNAME,
  PRIMARY KEY (tel_number, contact_tel_number),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (contact_tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE blocked_contacts_table(
  tel_number PHONE,
  contact_tel_number PHONE,
  PRIMARY KEY (tel_number, contact_tel_number),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (contact_tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE group_table(
  group_id GROUPID,
  name CHARNAME,
  member_count NUMBER,
  creator_tel_number PHONE,
  PRIMARY KEY (group_id),
  FOREIGN KEY (creator_tel_number) REFERENCES user_table(tel_number)
  ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE membership_table(
  tel_number PHONE,
  group_id GROUPID,
  is_admin BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (tel_number, group_id),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (group_id) REFERENCES group_table(group_id)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE group_blocked_users_table(
  tel_number PHONE,
  group_id GROUPID,
  PRIMARY KEY (tel_number, group_id),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (group_id) REFERENCES group_table(group_id)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE channel_table (
  channel_id CHARNAME,
  name CHARNAME,
  member_count NUMBER,
  creator_tel_number PHONE,
  PRIMARY KEY (channel_id),
  FOREIGN KEY (creator_tel_number) REFERENCES user_table(tel_number)
  ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE subscribe_table (
  tel_number PHONE,
  channel_id CHARNAME,
  is_admin BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (tel_number, channel_id),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (channel_id) REFERENCES channel_table(channel_id)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE channel_blocked_users_table (
  tel_number PHONE,
  channel_id CHARNAME,
  PRIMARY KEY (tel_number, channel_id),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (channel_id) REFERENCES channel_table(channel_id)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE message_table (
  creator_tel_number PHONE,
  message_id NUMBER,
  message_text TEXT,
  create_time TIMEDATE,
  media_address ADDRESS DEFAULT NULL,
  PRIMARY KEY (creator_tel_number, message_id),
  FOREIGN KEY (creator_tel_number) REFERENCES user_table(tel_number)
  ON DELETE RESTRICT ON UPDATE RESTRICT,
  FOREIGN KEY (media_address) REFERENCES media_table(file_address)
  ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE media_table (
  file_address ADDRESS,
  upload_time TIMEDATE,
  type MEDIATYPE,
  PRIMARY KEY (file_address)
);

CREATE TABLE image_table (
  file_address ADDRESS,
  PRIMARY KEY (file_address),
  FOREIGN KEY (file_address) REFERENCES media_table(file_address)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE user_profile_table (
  tel_number PHONE,
  image_address ADDRESS,
  date TIMEDATE,
  PRIMARY KEY (tel_number, image_address, date),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (image_address) REFERENCES image_table(file_address)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE group_profile_table (
  group_id GROUPID,
  image_address ADDRESS,
  date TIMEDATE,
  PRIMARY KEY (group_id, image_address, date),
  FOREIGN KEY (group_id) REFERENCES group_table(group_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (image_address) REFERENCES image_table(file_address)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE channel_profile_table (
  channel_id CHARNAME,
  image_address ADDRESS,
  date TIMEDATE,
  PRIMARY KEY (channel_id, image_address, date),
  FOREIGN KEY (channel_id) REFERENCES channel_table(channel_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (image_address) REFERENCES image_table(file_address)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE group_sends_table (
  tel_number PHONE,
  group_id GROUPID,
  creator_tel_number PHONE,
  message_id NUMBER,
  send_time TIMEDATE,
  PRIMARY KEY (tel_number, group_id, creator_tel_number, message_id, send_time),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (group_id) REFERENCES group_table(group_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (creator_tel_number, message_id) REFERENCES message_table(creator_tel_number, message_id)
  ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE group_seen_table (
  tel_number PHONE,
  group_id GROUPID,
  creator_tel_number PHONE,
  message_id NUMBER,
  send_time TIMEDATE,
  viewer_tel_number PHONE,
  PRIMARY KEY (tel_number, group_id, creator_tel_number, message_id, send_time, viewer_tel_number),
  FOREIGN KEY (tel_number, group_id, creator_tel_number, message_id, send_time) REFERENCES group_sends_table(tel_number, group_id, creator_tel_number, message_id, send_time)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (viewer_tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE channel_sends_table (
  tel_number PHONE,
  channel_id CHARNAME,
  creator_tel_number PHONE,
  message_id NUMBER,
  send_time TIMEDATE,
  PRIMARY KEY (tel_number, channel_id, creator_tel_number, message_id, send_time),
  FOREIGN KEY (tel_number) REFERENCES user_table(tel_number)
  ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (channel_id) REFERENCES channel_table(channel_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (creator_tel_number, message_id) REFERENCES message_table(creator_tel_number, message_id)
  ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE channel_seen_table (
  tel_number PHONE,
  channel_id CHARNAME,
  creator_tel_number PHONE,
  message_id NUMBER,
  send_time TIMEDATE,
  viewer_tel_number PHONE,
  PRIMARY KEY (tel_number, channel_id, creator_tel_number, message_id, send_time, viewer_tel_number),
  FOREIGN KEY (tel_number, channel_id, creator_tel_number, message_id, send_time) REFERENCES channel_sends_table(tel_number, channel_id, creator_tel_number, message_id, send_time)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (viewer_tel_number) REFERENCES user_table(tel_number)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE chat_table (
  sender_tel_number PHONE,
  receiver_tel_number PHONE,
  creator_tel_number PHONE,
  message_id NUMBER,
  send_time TIMEDATE,
  seen BOOLEAN,
  PRIMARY KEY (sender_tel_number, receiver_tel_number, creator_tel_number, message_id, send_time),
  FOREIGN KEY (sender_tel_number) REFERENCES user_table(tel_number)
  ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (receiver_tel_number) REFERENCES user_table(tel_number)
  ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (creator_tel_number, message_id) REFERENCES message_table(creator_tel_number, message_id)
  ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE group_pin_table (
  tel_number PHONE,
  group_id GROUPID,
  creator_tel_number PHONE,
  message_id NUMBER,
  send_time TIMEDATE,
  PRIMARY KEY (group_id),
  FOREIGN KEY (group_id) REFERENCES group_table(group_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (tel_number, group_id, creator_tel_number, message_id, send_time) REFERENCES group_sends_table(tel_number, group_id, creator_tel_number, message_id, send_time)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE channel_pin_table (
  tel_number PHONE,
  channel_id CHARNAME,
  creator_tel_number PHONE,
  message_id NUMBER,
  send_time TIMEDATE,
  PRIMARY KEY (channel_id),
  FOREIGN KEY (channel_id) REFERENCES channel_table(channel_id)
  ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (tel_number, channel_id, creator_tel_number, message_id, send_time) REFERENCES channel_sends_table(tel_number, channel_id, creator_tel_number, message_id, send_time)
  ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE VIEW user_profile_view (tel_number, user_name, name, last_name, last_seen, profile_image)
  AS SELECT user_table.tel_number, user_table.user_name, user_table.name, user_table.last_name, now() - user_table.last_seen, user_profile_table.image_address
  FROM user_table LEFT OUTER JOIN user_profile_table ON user_table.tel_number = user_profile_table.tel_number
  WHERE date >= ALL (
      SELECT upt.date FROM user_profile_table AS upt
      WHERE user_table.tel_number = upt.tel_number
  );

CREATE VIEW contact_profile_view (tel_number, contact_tel_number, contact_name, user_name, last_seen, profile_image)
  AS SELECT contacts_table.tel_number, contacts_table.contact_tel_number, contacts_table.contact_name, user_profile_view.user_name, user_profile_view.last_seen, user_profile_view.profile_image
  FROM contacts_table JOIN user_profile_view ON (contact_tel_number = user_profile_view.tel_number);

CREATE VIEW chat_view (sender_tel_number, receiver_tel_number, creator_tel_number, message_id, send_time, seen, text, media_address)
  AS SELECT chat_table.sender_tel_number, chat_table.receiver_tel_number, message_table.creator_tel_number, message_table.message_id, chat_table.send_time, chat_table.seen, message_text, message_table.media_address
  FROM chat_table NATURAL JOIN message_table;

CREATE VIEW group_list_view (tel_number, group_id, name, image_address)
  AS SELECT tel_number, group_table.group_id, name, image_address
  FROM (membership_table NATURAL JOIN group_table) LEFT OUTER JOIN group_profile_table ON group_table.group_id = group_profile_table.group_id
  WHERE date >= ALL (
    SELECT gpt.date FROM group_profile_table AS gpt
    WHERE group_profile_table.group_id = gpt.group_id
  );

CREATE VIEW channel_list_view (tel_number, channel_id, name, image_address)
  AS SELECT tel_number, channel_table.channel_id, name, image_address
  FROM (subscribe_table NATURAL JOIN channel_table) LEFT OUTER JOIN channel_profile_table ON channel_table.channel_id = channel_profile_table.channel_id
  WHERE date >= ALL (
    SELECT cpt.date FROM channel_profile_table AS cpt
    WHERE channel_profile_table.channel_id = cpt.channel_id
  );

CREATE VIEW group_profile_view (group_id, name, member_count, image_address)
  AS SELECT group_table.group_id, name, member_count, image_address
  FROM group_table LEFT OUTER JOIN group_profile_table ON group_table.group_id = group_profile_table.group_id
  WHERE date >= ALL (
    SELECT gpt.date FROM group_profile_table AS gpt
    WHERE group_profile_table.group_id = gpt.group_id
  );

CREATE VIEW group_members_view (group_id, tel_number, user_name, name, last_name, last_seen, profile_image, is_admin)
  AS SELECT group_id, tel_number, user_name, name, last_name, last_seen, profile_image, is_admin
  FROM membership_table NATURAL JOIN user_profile_view;

CREATE VIEW group_blocked_view (group_id, tel_number, user_name, name, last_name, last_seen, profile_image)
  AS SELECT group_id, tel_number, user_name, name, last_name, last_seen, profile_image
  FROM group_blocked_users_table NATURAL JOIN user_profile_view;

CREATE VIEW group_creator_view (group_id, creator_tel_number, user_name, name, last_name, last_seen, profile_image)
  AS SELECT group_id, creator_tel_number, user_name, user_profile_view.name, last_name, last_seen, profile_image
  FROM group_table JOIN user_profile_view ON creator_tel_number = tel_number;

CREATE VIEW group_pin_view (group_id, tel_number, creator_tel_number, message_id, send_time, text, media_address)
  AS SELECT group_id, tel_number, creator_tel_number, message_id, send_time, message_text, media_address
  FROM group_pin_table NATURAL JOIN message_table;

CREATE VIEW group_messages_view (group_id, tel_number, name, last_name, profile_image, creator_tel_number, message_id, text, media_address, send_time)
  AS SELECT group_id, tel_number, name, last_name, profile_image, creator_tel_number, message_id, message_text, media_address, send_time
  FROM user_profile_view NATURAL JOIN group_sends_table NATURAL JOIN message_table;

CREATE VIEW channel_profile_view (channel_id, name, member_count, image_address)
  AS SELECT channel_table.channel_id, name, member_count, image_address
  FROM channel_table LEFT OUTER JOIN channel_profile_table ON channel_table.channel_id = channel_profile_table.channel_id
  WHERE date >= ALL (
    SELECT cpt.date FROM channel_profile_table AS cpt
    WHERE channel_profile_table.channel_id = cpt.channel_id
  );

CREATE VIEW channel_subscribes_view (channel_id, tel_number, user_name, name, last_name, last_seen, profile_image, is_admin)
  AS SELECT channel_id, tel_number, user_name, name, last_name, last_seen, profile_image, is_admin
  FROM subscribe_table NATURAL JOIN user_profile_view;

CREATE VIEW channel_blocked_view (channel_id, tel_number, user_name, name, last_name, last_seen, profile_image)
  AS SELECT channel_id, tel_number, user_name, name, last_name, last_seen, profile_image
  FROM channel_blocked_users_table NATURAL JOIN user_profile_view;

CREATE VIEW channel_creator_view (channel_id, creator_tel_number, user_name, name, last_name, last_seen, profile_image)
  AS SELECT channel_id, creator_tel_number, user_name, user_profile_view.name, last_name, last_seen, profile_image
  FROM channel_table JOIN user_profile_view ON creator_tel_number = tel_number;

CREATE VIEW channel_pin_view (channel_id, tel_number, creator_tel_number, message_id, send_time, message_text, media_address)
  AS SELECT channel_id, tel_number, creator_tel_number, message_id, send_time, message_text, media_address
  FROM channel_pin_table NATURAL JOIN message_table;

CREATE VIEW channel_messages_view (channel_id, tel_number, name, last_name, profile_image, creator_tel_number, message_id, text, media_address, send_time)
  AS SELECT channel_id, tel_number, name, last_name, profile_image, creator_tel_number, message_id, message_text, media_address, send_time
  FROM user_profile_view NATURAL JOIN channel_sends_table NATURAL JOIN message_table;

CREATE FUNCTION inc_group_member_count()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    UPDATE group_table
      SET member_count = member_count + 1
      WHERE group_table.group_id = NEW.group_id;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER group_add_member_trigger
  AFTER INSERT
  ON membership_table
  FOR EACH ROW
  EXECUTE PROCEDURE inc_group_member_count();

CREATE FUNCTION dec_group_member_count()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    UPDATE group_table
      SET member_count = member_count - 1
      WHERE group_table.group_id = OLD.group_id;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER group_leave_member_trigger
  AFTER DELETE
  ON membership_table
  FOR EACH ROW
  EXECUTE PROCEDURE dec_group_member_count();

CREATE FUNCTION inc_channel_subscribe_count()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    UPDATE channel_table
      SET member_count = member_count + 1
      WHERE channel_table.channel_id = NEW.channel_id;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER channel_add_subscribe_trigger
  AFTER INSERT
  ON subscribe_table
  FOR EACH ROW
  EXECUTE PROCEDURE inc_channel_subscribe_count();

CREATE FUNCTION dec_channel_subscribe_count()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    UPDATE channel_table
      SET member_count = member_count + 1
      WHERE channel_table.channel_id = OLD.channel_id;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER channel_leave_subscribe_trigger
  AFTER DELETE
  ON subscribe_table
  FOR EACH ROW
  EXECUTE PROCEDURE dec_channel_subscribe_count();

CREATE FUNCTION set_creator_as_member_admin_group()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    INSERT INTO membership_table
      VALUES (NEW.creator_tel_number, NEW.group_id, TRUE);
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER set_creator_as_member_admin_group_trigger
  AFTER INSERT
  ON group_table
  FOR EACH ROW
  EXECUTE PROCEDURE set_creator_as_member_admin_group();

CREATE FUNCTION set_creator_as_member_admin_channel()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    INSERT INTO subscribe_table
      VALUES (NEW.creator_tel_number, NEW.channel_id, TRUE);
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER set_creator_as_member_admin_channel_trigger
  AFTER INSERT
  ON channel_table
  FOR EACH ROW
  EXECUTE PROCEDURE set_creator_as_member_admin_channel();

CREATE FUNCTION delete_group_zero_member()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    DELETE FROM group_table AS gt
      WHERE gt.group_id = NEW.group_id;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER delete_group_zero_member_trigger
  AFTER UPDATE OF member_count
  ON group_table
  FOR EACH ROW
  WHEN (NEW.member_count = 0)
  EXECUTE PROCEDURE delete_group_zero_member();

CREATE FUNCTION delete_channel_zero_member()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    DELETE FROM channel_table AS ct
      WHERE ct.channel_id = NEW.channel_id;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER delete_channel_zero_member_trigger
  AFTER UPDATE OF member_count
  ON channel_table
  FOR EACH ROW
  WHEN (NEW.member_count = 0)
  EXECUTE PROCEDURE delete_channel_zero_member();

CREATE FUNCTION self_seen_sender_group()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    INSERT INTO group_seen_table
      VALUES (NEW.tel_number, NEW.group_id, NEW.creator_tel_number, NEW.message_id, NEW.send_time, NEW.tel_number);
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER self_seen_sender_group_trigger
  AFTER INSERT
  ON group_sends_table
  FOR EACH ROW
  EXECUTE PROCEDURE self_seen_sender_group();

CREATE FUNCTION self_seen_sender_channel()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    INSERT INTO channel_seen_table
      VALUES (NEW.tel_number, NEW.channel_id, NEW.creator_tel_number, NEW.message_id, NEW.send_time, NEW.tel_number);
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER self_seen_sender_channel_trigger
  AFTER INSERT
  ON channel_sends_table
  FOR EACH ROW
  EXECUTE PROCEDURE self_seen_sender_channel();

CREATE FUNCTION delete_on_blocked_group()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    DELETE FROM membership_table AS mt
      WHERE mt.group_id = NEW.group_id AND mt.tel_number = NEW.tel_number;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER delete_on_blocked_group_trigger
  AFTER INSERT
  ON group_blocked_users_table
  FOR EACH ROW
  EXECUTE PROCEDURE delete_on_blocked_group();

CREATE FUNCTION delete_on_blocked_channel()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    DELETE FROM subscribe_table AS st
      WHERE st.channel_id = NEW.channel_id AND st.tel_number = NEW.tel_number;
    RETURN NULL;
  END;
  $$;

CREATE TRIGGER delete_on_blocked_channel_trigger
  AFTER INSERT
  ON channel_blocked_users_table
  FOR EACH ROW
  EXECUTE PROCEDURE delete_on_blocked_channel();

CREATE FUNCTION raise_exception_blocked_user()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    IF (exists(
        SELECT * FROM blocked_contacts_table
        WHERE tel_number = NEW.receiver_tel_number AND contact_tel_number = NEW.sender_tel_number))
      THEN
      RAISE EXCEPTION 'This user is blocked!';
    END IF;
    RETURN NEW;
  END;
  $$;

CREATE TRIGGER user_blocked_send_trigger
  BEFORE INSERT
  ON chat_table
  FOR EACH ROW
  EXECUTE PROCEDURE raise_exception_blocked_user();

CREATE FUNCTION raise_exception_blocked_user_group()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    IF (exists(
        SELECT * FROM group_blocked_users_table
        WHERE tel_number = NEW.tel_number AND group_id = NEW.group_id))
      THEN
      RAISE EXCEPTION 'This user is blocked!';
    END IF;
    RETURN NEW;
  END;
  $$;

CREATE TRIGGER group_blocked_member_trigger
  BEFORE INSERT
  ON membership_table
  FOR EACH ROW
  EXECUTE PROCEDURE raise_exception_blocked_user_group();

CREATE FUNCTION raise_exception_blocked_user_channel()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    IF (exists(
        SELECT * FROM channel_blocked_users_table
        WHERE tel_number = NEW.tel_number AND channel_id = NEW.channel_id))
      THEN
      RAISE EXCEPTION 'This user is blocked!';
    END IF;
    RETURN NEW;
  END;
  $$;

CREATE TRIGGER channel_blocked_member_trigger
  BEFORE INSERT
  ON subscribe_table
  FOR EACH ROW
  EXECUTE PROCEDURE raise_exception_blocked_user_channel();

CREATE FUNCTION raise_exception_non_admin_sender_channel()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    IF (NOT exists(
        SELECT * FROM subscribe_table
        WHERE tel_number = NEW.tel_number AND channel_id = NEW.channel_id AND is_admin = TRUE))
      THEN
      RAISE EXCEPTION 'This user is not admin of channel!';
    END IF;
    RETURN NEW;
  END;
  $$;

CREATE TRIGGER admin_sender_channel_trigger
  BEFORE INSERT
  ON channel_sends_table
  FOR EACH ROW
  EXECUTE PROCEDURE raise_exception_non_admin_sender_channel();

CREATE FUNCTION raise_exception_non_member_sender_group()
  RETURNS TRIGGER
  LANGUAGE plpgsql
  AS $$ BEGIN
    IF (NOT exists(
        SELECT * FROM membership_table
        WHERE tel_number = NEW.tel_number AND group_id = NEW.group_id))
      THEN
      RAISE EXCEPTION 'This user is not member of group!';
    END IF;
    RETURN NEW;
  END;
  $$;

CREATE TRIGGER member_sender_group_trigger
  BEFORE INSERT
  ON group_sends_table
  FOR EACH ROW
  EXECUTE PROCEDURE raise_exception_non_member_sender_group();
