from tortoise import Tortoise
from environs import Env

env = Env()
env.read_env()

DATABASE_URL = env.str("DATABASE_URL")

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "app.models.user",
                "app.models.post",
                "app.models.comment",
                "app.models.comment_likes",
                "app.models.likes",
                "app.models.images",
                "aerich.models",
            ],
            "default_connection": "default",
        },
    },
}


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
