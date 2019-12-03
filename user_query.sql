--get_group_list
SELECT * FROM group_list_view
WHERE tel_number = khode yaru;

--get_channel_list
SELECT * FROM channel_list_view
WHERE tel_number = khode yaru;

--add_group_membership
--agar konande = shavande:
INSERT INTO membership_table (tel_number, group_id)
    VALUES (khode yaru, %s);
--dar gheyre in surat:
SELECT tel_number FROM membership_table
WHERE group_id = %s AND is_admin = TRUE;
--agar konande in tu bud:
INSERT INTO membership_table (tel_number, group_id)
  VALUES (%s, %s);

--add_channel_subscribe
--agar konande = shavande:
INSERT INTO subscribe_table (tel_number, channel_id)
    VALUES (khode yaru, %s);
--dar gheyre in surat:
SELECT tel_number FROM subscribe_table
WHERE channel_id = %s AND is_admin = TRUE;
--agar konande in tu bud:
INSERT INTO subscribe_table (tel_number, channel_id)
  VALUES (%s, %s);

--remove_group_membership
--agar konande = shavande:
DELETE FROM membership_table
WHERE group_id = %s AND tel_number = khode yaru;
--dar gheyre in surat:
SELECT tel_number FROM membership_table
WHERE group_id = %s AND is_admin = TRUE;
--agar konande in tu bud:
DELETE FROM membership_table
WHERE group_id = %s AND tel_number = %s;

--remove_channel_subscribe
--agar konande = shavande:
DELETE FROM subscribe_table
WHERE channel_id = %s AND tel_number = khode yaru;
--dar gheyre in surat:
SELECT tel_number FROM subscribe_table
WHERE channel_id = %s AND is_admin = TRUE;
--agar konande in tu bud:
DELETE FROM subscribe_table
WHERE channel_id = %s AND tel_number = %s;
