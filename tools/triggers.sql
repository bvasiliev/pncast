CREATE OR REPLACE FUNCTION update_theme_count() RETURNS TRIGGER AS $$
BEGIN
 UPDATE theme SET count = theme_to_video.count 
 FROM (SELECT theme_id, count(*) as count FROM theme_to_video GROUP BY theme_id) theme_to_video
 WHERE theme.id = theme_to_video.theme_id
 AND theme.id = NEW.theme_id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_theme
AFTER INSERT OR UPDATE ON theme_to_video 
FOR EACH ROW 
EXECUTE PROCEDURE update_theme_count ();



CREATE OR REPLACE FUNCTION update_author_count() RETURNS TRIGGER AS $$
BEGIN
 UPDATE author
 SET count = videos.count
 FROM (SELECT author_id, count(*) as count FROM video GROUP BY author_id) videos
 WHERE author.id = videos.author_id
 AND author.id = NEW.author_id;
RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER insert_video
AFTER INSERT OR UPDATE ON video 
FOR EACH ROW 
EXECUTE PROCEDURE update_author_count ();
