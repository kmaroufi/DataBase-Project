--add_group
INSERT INTO group_table (name, creator_tel_number)
    VALUES (%s, %s);

--remove_group
SELECT creator_tel_number FROM group_creator_view
WHERE group_id = %s;
--agar pak konande khod sazande bood:
DELETE FROM group_table
WHERE group_id = %s;

--add_blocked_user_to_group
SELECT tel_number FROM group_members_view
WHERE group_id = %s AND is_admin = TRUE;
--agar konande tuye in bud va shavande tuye in nabud:
INSERT INTO group_blocked_users_table (tel_number, group_id)
    VALUES (%s, %s);

--remove_blocked_user_from_group
SELECT tel_number FROM group_members_view
WHERE group_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
DELETE FROM group_blocked_users_table
WHERE group_id = %s AND tel_number = %s;

--add_admin_to_group
SELECT creator_tel_number FROM group_creator_view
WHERE group_id = %s;
--agar konande in bud:
UPDATE membership_table
SET is_admin = TRUE
WHERE group_id = %s AND tel_number = %s;

--remove_admin_from_group
SELECT creator_tel_number FROM group_creator_view
WHERE group_id = %s;
--agar konande in bud:
UPDATE membership_table
SET is_admin = FALSE
WHERE group_id = %s AND tel_number = %s;

--add_profile_pic_group
SELECT tel_number FROM group_members_view
WHERE group_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
SELECT file_address FROM image_table
  WHERE file_address = %s;
--agar file in tu nabud bayad upload shavad:
INSERT INTO media_table (file_address, type)
    VALUES (%s, 'image');
INSERT INTO image_table (file_address)
    VALUES (%s);
--hal ezafe mikonim:
INSERT INTO group_profile_table (group_id, image_address)
    VALUES (%s, %s);

--remove_profile_pic_group
SELECT tel_number FROM group_members_view
WHERE group_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
DELETE FROM group_profile_table
WHERE group_id = %s AND image_address = %s AND date = %s;

--add_pm_group
INSERT INTO media_table (file_address, type)
    VALUES (%s, %s);
--agar aks bud:
INSERT INTO image_table (file_address)
    VALUES (%s);
SELECT max(message_id) FROM message_table
  WHERE creator_tel_number = khode yaru;
INSERT INTO message_table (creator_tel_number, message_id, message_text, media_address)
    VALUES (khode yaru, max+1, %s, %s);
INSERT INTO group_sends_table (tel_number, group_id, creator_tel_number, message_id)
    VALUES (khode yaru, %s, khode yaru, max + 1);

--add_forwarded_pm_group
INSERT INTO group_sends_table (tel_number, group_id, creator_tel_number, message_id)
    VALUES (khode yaru, %s, %s, %s);

--remove_pm_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s AND (tel_number = %s OR is_admin = TRUE);
--agar konande tuye in bud:
DELETE FROM group_sends_table
  WHERE group_id = %s AND tel_number = %s AND creator_tel_number = %s AND message_id = %s AND send_time = %s;

--add_seen_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
INSERT INTO group_seen_table (tel_number, group_id, creator_tel_number, message_id, send_time, viewer_tel_number)
    VALUES (%s, %s, %s, %s, %s, khode yaru);

--get_group_profile
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
SELECT * FROM group_profile_view
WHERE group_id = %s;

--get_group_members
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
SELECT * FROM group_members_view
WHERE group_id = %s;

--get_blocked_users_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
SELECT * FROM group_blocked_view
WHERE group_id = %s;

--get_admins_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
SELECT * FROM group_members_view
WHERE group_id = %s AND is_admin = TRUE;

--get_pm_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
SELECT * FROM group_messages_view
WHERE group_id = %s;

--add_pin_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
INSERT INTO group_pin_table (tel_number, group_id, creator_tel_number, message_id, send_time)
    VALUES (%s, %s, %s, %s, %s);

--remove_pin_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s AND is_admin = TRUE;
--agar konande tuye in bud:
DELETE FROM group_pin_table
WHERE group_id = %s;

--get_pin_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
SELECT * FROM group_pin_view
WHERE group_id = %s;

--get_creator_group
SELECT tel_number FROM membership_table
  WHERE group_id = %s;
--agar konande tuye in bud:
SELECT * FROM group_creator_view
WHERE group_id = %s;