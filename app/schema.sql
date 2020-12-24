CREATE SCHEMA IF NOT EXISTS app;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS app.group (
    group_id int GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    group_title varchar(50) NOT NULL,
    participant_text_message text NOT NULL,
    participant_html_message text NOT NULL,
    sent_emails boolean NOT NULL DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS app.user (
    user_email varchar(200) NOT NULL PRIMARY KEY,
    user_password varchar(72) NOT NULL,
    user_session_id uuid DEFAULT uuid_generate_v4()
);

CREATE TABLE IF NOT EXISTS app.user_group (
    user_email varchar(200) REFERENCES app.user,
    group_id int REFERENCES app.group
);

CREATE TABLE IF NOT EXISTS app.participant (
    group_id int REFERENCES app.group,
    participant_id int NOT NULL,
    participant_name varchar(50) NOT NULL,
    participant_email varchar(200),
    recipient_id int NOT NULL
);

CREATE TABLE IF NOT EXISTS app.participant_restriction (
    group_id int REFERENCES app.group,
    participant_id int NOT NULL,
    restriction varchar(50)
);
