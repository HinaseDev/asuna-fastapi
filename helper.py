from fastapi import Depends
from asqlite import Connection as get_conn
from globs import images_directory
import asyncio
from log import logger
class GetSet:
    """
    Simple descriptor class to allow for get/set functionality.
    Usage:
    ```
    class Example:
        def __init__(self, value):
            self.attr = GetSet(value)

        @property
        def attr(self):
            return self.attr.get()

        @attr.setter
        def attr(self, value):
            self.attr.set(value)
    ```
    """
    def __init__(self, value):
        self.attrval = value

    def __get__(self, instance, owner):
        return self.attrval

    def __set__(self, instance, value):
        self.attrval = value

    def get(self):
        return self.attrval

    def set(self, value):
        self.attrval = value

def generate_cache(ep_cache: GetSet, ti_cache: GetSet):
    endpoints = {}
    logger.debug("Generating cache")
    total_images = 0

    # Iterate over directories inside 'images'
    for image_type_dir in images_directory.iterdir():
        if image_type_dir.is_dir():
            images = [img for img in image_type_dir.iterdir() if img.is_file()]
            image_count = len(images)
            endpoints[image_type_dir.name] = {"url": f"/api/{image_type_dir.name}", "imageCount": image_count}
            total_images += image_count
    ep_cache.set(endpoints)
    ti_cache.set(total_images)
    logger.debug("Cache generated! Total images: %d", total_images)

async def generate_cache_async(ep_cache: GetSet, ti_cache: GetSet):
    await asyncio.to_thread(lambda: generate_cache(ep_cache, ti_cache))

def get_particular_data(table):
    async def wrapper(conn=Depends(get_conn)):
        async with conn.cursor() as cursor:
            result = await cursor.execute(f"SELECT * FROM {table}")
            return [x[0] for x in await result.fetchall()]

    return wrapper