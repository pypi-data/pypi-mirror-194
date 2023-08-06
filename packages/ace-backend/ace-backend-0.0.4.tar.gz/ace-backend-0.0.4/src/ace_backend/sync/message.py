import aiohttp
import asyncio
import asyncpg
import datetime as dt
import logging
from typing import Dict
from typing import List

logger = logging.getLogger(__name__)


async def _fetch_messages(session: aiohttp.ClientSession, last: int) -> List[Dict]:
    result: List[Dict] = []
    while True:
        response = await session.get(f'https://tuzach.in/api/?app=chat&last={last}')
        response_json = await response.json(content_type=None)

        if not response_json['data']:
            return result

        result.extend(response_json['data'])
        last = result[-1]['id']


async def _get_db_last(pool: asyncpg.Pool) -> int:
    external_id = await pool.fetchval('SELECT MAX(external_id) FROM sync.message')

    return external_id or 0


async def _insert_messages(pool: asyncpg.Pool, messages: List[Dict]) -> None:
    if not messages:
        return

    query_pictures = []
    query_messages = []
    for message in messages:
        picture = message.get('picture', {})
        if picture:
            query_pictures.append(
                [
                    picture['name'],
                    picture['imgurl'],
                    picture['thumburl'],
                    picture['filedata'],
                    picture['imgw'],
                    picture['imgh'],
                    picture['thumbw'],
                    picture['thumbh'],
                ]
            )

        query_messages.append(
            [
                int(message['id']),
                message['type'],
                dt.datetime.fromisoformat(message['time']),
                message['text'],
                message['user_id'],
                message.get('avatar'),
                picture.get('name'),
            ]
        )

    pictures_args = tuple(zip(*query_pictures))
    if not pictures_args:
        pictures_args = ([],) * 8

    args = pictures_args + tuple(zip(*query_messages))

    await pool.execute(
        '''
        WITH picture AS (
            INSERT INTO sync.picture
                (
                    name,
                    imgurl,
                    thumburl,
                    filedata,
                    imgw,
                    imgh,
                    thumbw,
                    thumbh
                )
            VALUES 
                (
                    UNNEST($1::VARCHAR[]),
                    UNNEST($2::VARCHAR[]),
                    UNNEST($3::VARCHAR[]),
                    UNNEST($4::VARCHAR[]),
                    UNNEST($5::VARCHAR[]),
                    UNNEST($6::VARCHAR[]),
                    UNNEST($7::VARCHAR[]),
                    UNNEST($8::VARCHAR[])
                )
            ON CONFLICT (name) DO UPDATE
                SET name = EXCLUDED.name 
            RETURNING id, name
        )
        INSERT INTO sync.message
            (
                external_id,
                type,
                time,
                text,
                user_id,
                avatar,
                picture_id
            )
        SELECT 
            m.external_id,
            m.type,
            m.time,
            m.text,
            m.user_id,
            m.avatar,
            p.id
        FROM picture AS p
        RIGHT JOIN (
             SELECT
                UNNEST($9::BIGINT[]) AS external_id,
                UNNEST($10::VARCHAR[]) AS type,
                UNNEST($11::TIMESTAMPTZ[]) AS time,
                UNNEST($12::VARCHAR[]) AS text,
                UNNEST($13::VARCHAR[]) AS user_id,
                UNNEST($14::VARCHAR[]) AS avatar,
                UNNEST($15::VARCHAR[]) AS picture_name
        ) AS m
            ON p.name = m.picture_name
        ON CONFLICT DO NOTHING
    ''',
        *args,
    )


async def do_sync(pool: asyncpg.Pool, session: aiohttp.ClientSession) -> None:
    last = await _get_db_last(pool)
    messages = await _fetch_messages(session, last)
    await _insert_messages(pool, messages)


async def sync_messages(pool: asyncpg.Pool):
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        while True:
            try:
                await do_sync(pool, session)
            except Exception:
                logger.exception('messages sync iteration failed')

            await asyncio.sleep(5)
