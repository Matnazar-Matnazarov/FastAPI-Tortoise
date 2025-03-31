from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" ADD "updated" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "comment" ADD "updated" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "comment_likes" ADD "updated" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "likes" ADD "updated" TIMESTAMPTZ NOT NULL;
        ALTER TABLE "images" ADD "updated" TIMESTAMPTZ NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "users" DROP COLUMN "updated";
        ALTER TABLE "likes" DROP COLUMN "updated";
        ALTER TABLE "images" DROP COLUMN "updated";
        ALTER TABLE "comment" DROP COLUMN "updated";
        ALTER TABLE "comment_likes" DROP COLUMN "updated";"""
