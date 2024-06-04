-- insert example data.

-- users

INSERT INTO user (id, username, role) VALUES (1, "admin", "admin");
INSERT INTO user (id, username, role) VALUES (3, "moderator", "moderator");
INSERT INTO user (username) VALUES ("johndoe");

-- topic

INSERT INTO topic (id, created_by, category, title) VALUES (1, 1, 2, "Donald Trump");
INSERT INTO topic (id, created_by, category, title) VALUES (2, 3, 2, "Joe Biden");
INSERT INTO topic (id, created_by, category, title) VALUES (4, 1, 4, "Magnus Tolander");

-- post

INSERT INTO post (user_id, topic_id, body, created) VALUES (1, 2, "Är han världens bästa president?", "2024-06-08 14:20:31");
INSERT INTO post (user_id, topic_id, title, body) VALUES (1, 2, "Joe Biden", "Är nog bättre.");
INSERT INTO post (user_id, topic_id, body) VALUES (3, 4, "Är han rolig eller?");
INSERT INTO post (user_id, topic_id, body) VALUES (3, 4, "Vad har vi för skit här?");
