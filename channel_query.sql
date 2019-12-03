--add_channel
INSERT INTO channel_table (channel_id, name, creator_tel_number)
    VALUES (%s, %s, khode yaru);

--remove_channel
SELECT creator_tel_number FROM channel_creator_view
WHERE channel_id = %s;
--agar pak konande khod sazande bood:
DELETE FROM channel_table
WHERE channel_id = %s;

--add_blocked_user_to_channel
SELECT tel_number FROM channel_subscribes_view
WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud va shavande tuye in nabud:
INSERT INTO channel_blocked_users_table (tel_number, channel_id)
    VALUES (%s, %s);

--remove_blocked_user_from_channel
SELECT tel_number FROM channel_subscribes_view
WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
DELETE FROM channel_blocked_users_table
WHERE channel_id = %s AND tel_number = %s;

--add_admin_to_channel
SELECT creator_tel_number FROM channel_creator_view
WHERE channel_id = %s;
--agar konande in bud:
UPDATE subscribe_table
SET is_admin = TRUE
WHERE channel_id = %s AND tel_number = %s;

--remove_admin_from_channel
SELECT creator_tel_number FROM channel_creator_view
WHERE channel_id = %s;
--agar konande in bud:
UPDATE subscribe_table
SET is_admin = FALSE
WHERE channel_id = %s AND tel_number = %s;

--add_profile_pic_channel
SELECT tel_number FROM channel_subscribes_view
WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
SELECT file_address FROM image_table
  WHERE file_address = %s;
--agar file in tu nabud bayad upload shavad:
INSERT INTO media_table (file_address, type)
    VALUES (%s, 'image');
INSERT INTO image_table (file_address)
    VALUES (%s);
--hal ezafe mikonim:
INSERT INTO channel_profile_table (channel_id, image_address)
    VALUES (%s, %s);

--remove_profile_pic_channel
SELECT tel_number FROM channel_subscribes_view
WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
DELETE FROM channel_profile_table
WHERE channel_id = %s AND image_address = %s AND date = %s;

--add_pm_channel
INSERT INTO media_table (file_address, type)
    VALUES (%s, %s);
--agar aks bud:
INSERT INTO image_table (file_address)
    VALUES (%s);
SELECT max(message_id) FROM message_table
  WHERE creator_tel_number = khode yaru;
INSERT INTO message_table (creator_tel_number, message_id, message_text, media_address)
    VALUES (khode yaru, max+1, %s, %s);
INSERT INTO channel_sends_table (tel_number, channel_id, creator_tel_number, message_id)
    VALUES (khode yaru, %s, khode yaru, max + 1);

--add_forwarded_pm_channel
INSERT INTO channel_sends_table (tel_number, channel_id, creator_tel_number, message_id)
    VALUES (khode yaru, %s, %s, %s);

--remove_pm_channel
SELECT tel_number FROM subscribe_table
  WHERE channel_id = %s AND (tel_number = %s OR is_admin = TRUE);
--agar konande tuye in bud:
DELETE FROM channel_sends_table
  WHERE channel_id = %s AND tel_number = %s AND creator_tel_number = %s AND message_id = %s AND send_time = %s;

--add_seen_channel
INSERT INTO channel_seen_table (tel_number, channel_id, creator_tel_number, message_id, send_time, viewer_tel_number)
    VALUES (%s, %s, %s, %s, %s, khode yaru);

--get_channel_profile
SELECT * FROM channel_profile_view
WHERE channel_id = %s;

--get_channel_subscribes
SELECT tel_number FROM subscribe_table
  WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
SELECT * FROM channel_subscribes_view
WHERE channel_id = %s;

--get_blocked_users_channel
SELECT tel_number FROM subscribe_table
  WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
SELECT * FROM channel_blocked_view
WHERE channel_id = %s;

--get_admins_channel
SELECT tel_number FROM subscribe_table
  WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
SELECT * FROM channel_subscribes_view
WHERE channel_id = %s AND is_admin = TRUE;

--get_pm_channel
SELECT * FROM channel_messages_view
WHERE channel_id = %s;

--add_pin_channel
SELECT tel_number FROM subscribe_table
  WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
INSERT INTO channel_pin_table (tel_number, channel_id, creator_tel_number, message_id, send_time)
    VALUES (%s, %s, %s, %s, %s);

--remove_pin_channel
SELECT tel_number FROM subscribe_table
  WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
DELETE FROM channel_pin_table
WHERE channel_id = %s;

--get_pin_channel
SELECT * FROM channel_pin_view
WHERE channel_id = %s;

--get_creator_channel
SELECT tel_number FROM subscribe_table
  WHERE channel_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
SELECT * FROM channel_creator_view
WHERE channel_id = %s;