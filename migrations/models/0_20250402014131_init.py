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
    "created" TIMESTAMPTZ NOT NULL,
    "updated" TIMESTAMPTZ NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_users_is_staf_c3d475" ON "users" ("is_staff");
CREATE INDEX IF NOT EXISTS "idx_users_usernam_df2ee6" ON "users" ("username", "email");
CREATE TABLE IF NOT EXISTS "post" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(255) NOT NULL,
    "title" VARCHAR(255) NOT NULL,
    "text" TEXT NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL,
    "updated" TIMESTAMPTZ NOT NULL,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_post_is_acti_eec515" ON "post" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_post_user_id_db59ab" ON "post" ("user_id", "created", "is_active");
CREATE TABLE IF NOT EXISTS "comment" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "comment" TEXT NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL,
    "updated" TIMESTAMPTZ NOT NULL,
    "post_id" BIGINT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_comment_post_id_298e22" ON "comment" ("post_id");
CREATE INDEX IF NOT EXISTS "idx_comment_is_acti_8b4013" ON "comment" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_comment_user_id_4b96a3" ON "comment" ("user_id", "post_id", "is_active", "created");
CREATE TABLE IF NOT EXISTS "comment_likes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_like" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL,
    "updated" TIMESTAMPTZ NOT NULL,
    "comment_id" BIGINT NOT NULL REFERENCES "comment" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_comment_lik_comment_9e9836" ON "comment_likes" ("comment_id");
CREATE INDEX IF NOT EXISTS "idx_comment_lik_is_like_8bec58" ON "comment_likes" ("is_like");
CREATE INDEX IF NOT EXISTS "idx_comment_lik_user_id_74f5af" ON "comment_likes" ("user_id", "comment_id", "is_like");
CREATE INDEX IF NOT EXISTS "idx_comment_lik_user_id_c5ddd0" ON "comment_likes" ("user_id", "comment_id", "created");
CREATE TABLE IF NOT EXISTS "likes" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "is_like" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL,
    "updated" TIMESTAMPTZ NOT NULL,
    "post_id" BIGINT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE,
    "user_id" BIGINT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_likes_post_id_ba1812" ON "likes" ("post_id");
CREATE INDEX IF NOT EXISTS "idx_likes_is_like_2c8d6b" ON "likes" ("is_like");
CREATE INDEX IF NOT EXISTS "idx_likes_user_id_31fec2" ON "likes" ("user_id", "post_id");
CREATE TABLE IF NOT EXISTS "images" (
    "id" BIGSERIAL NOT NULL PRIMARY KEY,
    "image" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created" TIMESTAMPTZ NOT NULL,
    "updated" TIMESTAMPTZ NOT NULL,
    "post_id" BIGINT NOT NULL REFERENCES "post" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_images_post_id_41348c" ON "images" ("post_id");
CREATE INDEX IF NOT EXISTS "idx_images_is_acti_35ab10" ON "images" ("is_active");
CREATE INDEX IF NOT EXISTS "idx_images_post_id_f9a17e" ON "images" ("post_id", "is_active");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
