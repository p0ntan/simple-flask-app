DROP TRIGGER IF EXISTS trg_update_post;
DROP TRIGGER IF EXISTS trg_update_topic;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS topic;
DROP TABLE IF EXISTS category;
DROP TABLE IF EXISTS user;

-- tables 

-- "user" definition

CREATE TABLE "user" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL UNIQUE,
	password TEXT,
	role TEST(15) DEFAULT "author" NOT NULL,
	signature TEXT(150),
	avatar TEXT(150)
);

CREATE UNIQUE INDEX user_id_IDX ON "user" (id);

-- category definition

CREATE TABLE category (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	category TEXT(35) NOT NULL,
	description TEXT
);

CREATE UNIQUE INDEX category_id_IDX ON category (id);

-- topic definition

CREATE TABLE topic (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	created_by INTEGER NOT NULL,
	category INTEGER NOT NULL,
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	last_edited TIMESTAMP,
	deleted TIMESTAMP,
	disabled BOOLEAN,
	title TEXT NOT NULL,
	CONSTRAINT topic_user_FK FOREIGN KEY (created_by) REFERENCES "user"(id),
	CONSTRAINT topic_category_FK FOREIGN KEY (category) REFERENCES "category"(id)
);

CREATE UNIQUE INDEX topic_id_IDX ON topic (id);

-- post definition

CREATE TABLE post (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	topic_id INTEGER NOT NULL,
	created TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
	last_edited TIMESTAMP,
	deleted TIMESTAMP,
	title TEXT,
	body TEXT NOT NULL,
	CONSTRAINT post_user_FK FOREIGN KEY (user_id) REFERENCES "user"(id)
	CONSTRAINT post_topic_FK FOREIGN KEY (topic_id) REFERENCES "topic"(id)
);

CREATE UNIQUE INDEX post_id_IDX ON post (id);

-- triggers

CREATE TRIGGER trg_update_topic AFTER UPDATE OF title ON topic
	BEGIN
		UPDATE topic SET last_edited = CURRENT_TIMESTAMP WHERE id = new.id;
	END;

CREATE TRIGGER trg_update_post AFTER UPDATE OF body, title ON post
	BEGIN
		UPDATE post SET last_edited = CURRENT_TIMESTAMP WHERE id = new.id;
	END;
