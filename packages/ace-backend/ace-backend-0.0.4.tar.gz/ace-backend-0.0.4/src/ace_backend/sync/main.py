import logging

import asyncio

from ace_backend.sync import message
from ace_backend.lib import pg


logging.basicConfig(level=logging.DEBUG)


async def main_impl() -> None:
    pool = await pg.get_connection_pool()

    tasks = [message.sync_messages(pool)]

    await asyncio.gather(*tasks)


def main():
    asyncio.run(main_impl())


if __name__ == '__main__':
    main()
