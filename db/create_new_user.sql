-- Usage: select create_new_user('email', 'username', points)
CREATE OR REPLACE FUNCTION create_new_user(new_email TEXT, new_username TEXT, set_points INT) RETURNS VOID AS $$
  begin
    INSERT INTO players (email, username, points) VALUES (new_email, new_username, set_points);
  end;
$$
LANGUAGE 'plpgsql';
