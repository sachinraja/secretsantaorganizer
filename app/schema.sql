CREATE SCHEMA IF NOT EXISTS app;

CREATE TABLE IF NOT EXISTS app.group (
    group_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    group_title varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS app.user (
    user_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_email varchar(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS app.user_group (
    user_id int REFERENCES app.user,
    group_id int REFERENCES app.group
);

CREATE TABLE IF NOT EXISTS app.participant (
    group_id int REFERENCES app.group,
    participant_id int NOT NULL,
    participant_name varchar(50) NOT NULL,
    participant_email varchar(100),
    recipient_id int NOT NULL
);

CREATE TABLE IF NOT EXISTS app.participant_restriction (
    group_id int REFERENCES app.group,
    participant_id int NOT NULL,
    restriction varchar(50)
)
