from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "first_name" VARCHAR(255) NOT NULL,
    "last_name" VARCHAR(255) NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_staff" BOOL NOT NULL DEFAULT False,
    "picture" VARCHAR(255),
    "phone" VARCHAR(20),
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "post" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "text" TEXT NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "comment" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "comment" TEXT NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "post_id" BIGINT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "comment_likes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_like" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "comment_id" BIGINT NOT NULL REFERENCES "comment" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "likes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_like" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "post_id" BIGINT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "images" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "image" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "post_id" BIGINT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
