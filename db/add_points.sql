CREATE OR REPLACE FUNCTION add_points(user_email TEXT, pts_amnt INT) RETURNS VOID AS $$
  declare 
  c1 CURSOR for SELECT id, email, username, points FROM players WHERE email = user_email;
  
  temp_id INT;
  temp_email TEXT;
  temp_username TEXT;
  temp_points INT;

  begin
    open c1;
    LOOP 
      fetch c1 into temp_id, temp_email, temp_username, temp_points;
      exit when not found;
      update players set points = points + pts_amnt where email = user_email;
    end LOOP; 
    close c1;
  end;
$$
LANGUAGE 'plpgsql';
