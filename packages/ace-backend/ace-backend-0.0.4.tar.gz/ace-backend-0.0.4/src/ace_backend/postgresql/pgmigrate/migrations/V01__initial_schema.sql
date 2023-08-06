CREATE SCHEMA sync;

CREATE TABLE sync.picture
(
    id             BIGSERIAL PRIMARY KEY,

    name           VARCHAR NOT NULL,
    imgurl         VARCHAR NOT NULL,
    thumburl       VARCHAR NOT NULL,
    filedata       VARCHAR NOT NULL,
    imgw           VARCHAR NOT NULL,
    imgh           VARCHAR NOT NULL,
    thumbw         VARCHAR NOT NULL,
    thumbh         VARCHAR NOT NULL,

    UNIQUE(name)
);

CREATE TABLE sync.message
(
    id             BIGSERIAL PRIMARY KEY,

    external_id    BIGINT NOT NULL,
    type           VARCHAR NOT NULL,
    time           TIMESTAMPTZ NOT NULL,
    text           VARCHAR NOT NULL,
    user_id        VARCHAR NOT NULL,
    avatar         VARCHAR,
    picture_id     BIGINT REFERENCES sync.picture(id),

    UNIQUE (external_id)
);
