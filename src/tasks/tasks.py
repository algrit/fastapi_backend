from time import sleep
import asyncio
import os
import logging

from PIL import Image

from src.database import async_session_maker_null_pool
from src.tasks.celery_app import celery_instance
from src.utils.db_manager import DBManager


# @celery_instance.task
def resize_image(image_path: str):
    logging.debug(f"resize_image function launched with {image_path=}")
    sizes = [1000, 500, 200]
    output_folder = "src/static/images"

    img = Image.open(image_path)

    base_name = os.path.basename(image_path)
    name, ext = os.path.splitext(base_name)

    for size in sizes:
        img_resized = img.resize(
            (size, int(img.height * (size / img.width))), Image.Resampling.LANCZOS
        )

        new_file_name = f"{name}_{size}px{ext}"

        output_path = os.path.join(output_folder, new_file_name)

        img_resized.save(output_path)

    logging.info(f"Изображение сохранено в следующих размерах: {sizes} в папке {output_folder}")


@celery_instance.task
def test_celery():
    sleep(5)
    logging.info("Celery Worker works")


async def send_email_to_users_with_today_checkin_helper():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        logging.info("Celery Beat starts")
        today_bookings = await db.bookings.get_bookings_with_today_checkin()
        logging.info(f"Celery Beat: {today_bookings=}")
        return today_bookings


@celery_instance.task(name="today_checkin")
def send_email_to_users_with_today_checkin():
    asyncio.run(send_email_to_users_with_today_checkin_helper())
