SELECT
    tbl_users.id
    ,tbl_users.password
    ,tbl_users.email
FROM tbl_users
INNER JOIN authtoken_token
ON tbl_users.id = authtoken_token.user_id
WHERE authtoken_token.key = "Authorization";
