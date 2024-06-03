DROP TABLE post;
DROP TABLE topic;
DROP TABLE user;

-- "user" definition

CREATE TABLE "user" (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	username TEXT NOT NULL,
	password TEXT,
	signature TEXT(150),
	avatar TEXT(150)
);

CREATE UNIQUE INDEX user_id_IDX ON "user" (id);

-- topic definition

CREATE TABLE topic (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	created_by INTEGER NOT NULL,
	category INTEGER NOT NULL,
	deleted TEXT,
	created TEXT,
	disabled BOOLEAN,
	title TEXT NOT NULL,
	CONSTRAINT topic_user_FK FOREIGN KEY (created_by) REFERENCES "user"(id)
);

CREATE UNIQUE INDEX topic_id_IDX ON topic (id);

-- post definition

CREATE TABLE post (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER NOT NULL,
	topic_id INTEGER NOT NULL,
	deleted TEXT,
	created TEXT,
	last_edited TEXT,
	title TEXT,
	body TEXT NOT NULL,
	CONSTRAINT post_user_FK FOREIGN KEY (user_id) REFERENCES "user"(id)
);

CREATE UNIQUE INDEX post_id_IDX ON post (id);
