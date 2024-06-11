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

INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-08 14:20:31");
INSERT INTO post (author, topic_id, title, body, created) VALUES (3, 1, "Joe Biden", "Has title.", "2024-06-02 14:10:31");
INSERT INTO post (author, topic_id, body, created, deleted) VALUES (5, 1, "Is deleted.", "2024-06-04 12:10:31", "2024-06-05 14:10:31");
INSERT INTO post (author, topic_id, body) VALUES (3, 4, "Är han rolig eller?");
INSERT INTO post (author, topic_id, body) VALUES (3, 4, "Vad har vi för skit här?");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-01 14:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-02 14:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-02 12:20:31");
INSERT INTO post (author, topic_id, body, created, deleted) VALUES (1, 1, "Has no title", "2024-06-11 12:20:31", "2024-06-10 12:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-08 00:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-03 12:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-07 14:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-06 10:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Is the last of first ten", "2024-06-10 14:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-11 11:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Is the first of second ten.", "2024-06-11 10:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Has no title", "2024-06-11 13:20:31");
INSERT INTO post (author, topic_id, body, created) VALUES (1, 1, "Is the last of second ten.", "2024-06-11 14:20:31");
