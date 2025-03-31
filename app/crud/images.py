from typing import Optional, List
from app.models.images import Images
from app.schemas.images import ImagesCreate
from app.models.post import Post


async def create_image(image: ImagesCreate, post_id: int) -> Images:
    if not await Post.filter(id=post_id).exists():
        raise ValueError("Post not found")

    db_image = Images(**image.model_dump(), post_id=post_id)
    await db_image.save()
    return db_image


async def get_image(image_id: int) -> Optional[Images]:
    return await Images.get_or_none(id=image_id)


async def get_images_by_post(post_id: int) -> List[Images]:
    if not await Post.filter(id=post_id).exists():
        raise ValueError("Post not found")
    return await Images.filter(post_id=post_id).all()


async def delete_image(image_id: int) -> bool:
    db_image = await Images.get_or_none(id=image_id)
    if db_image is None:
        raise ValueError("Image not found")
    await db_image.delete()
    return True
