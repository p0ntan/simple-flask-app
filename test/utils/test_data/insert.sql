-- insert test data.

-- users

INSERT INTO user (id, username, role) VALUES (1, "admin", "admin");
INSERT INTO user (id, username, role) VALUES (3, "moderator", "moderator");
INSERT INTO user (id, username) VALUES (5, "johndoe");

-- topic

INSERT INTO topic (id, created_by, category, title) VALUES (1, 1, 2, "Donald Trump");
INSERT INTO topic (id, created_by, category, title) VALUES (2, 3, 2, "Joe Biden");
INSERT INTO topic (id, created_by, category, title) VALUES (4, 1, 4, "Magnus Tolander");

-- post

INSERT INTO post (user_id, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-08 14:20:31");
INSERT INTO post (user_id, topic_id, title, body, created) VALUES (3, 1, "Joe Biden", "Has title.", "2024-06-02 14:10:31");
INSERT INTO post (user_id, topic_id, body, created, deleted) VALUES (5, 1, "Is deleted.", "2024-06-04 12:10:31", "2024-06-05 14:10:31");
INSERT INTO post (user_id, topic_id, body) VALUES (3, 4, "Är han rolig eller?");
INSERT INTO post (user_id, topic_id, body) VALUES (3, 4, "Vad har vi för skit här?");
