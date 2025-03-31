from app.models.images import Images
from app.schemas.images import ImagesCreate


async def create_image(image: ImagesCreate, post_id: int):
    db_image = Images(**image.dict(), post_id=post_id)
    await db_image.save()
    return db_image
