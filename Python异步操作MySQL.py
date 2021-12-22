# -*- coding: utf-8 -*-
"""
Python异步操作MySQL

"""
import asyncio
import sqlalchemy as sa
import asyncio
import aiomysql
import nest_asyncio
nest_asyncio.apply ( )


async def test_example(loop):
    pool = await aiomysql.create_pool(host='localhost', port=3306,
                   user='root', password='sunboy',
                   db='test1', loop=loop)
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * from testa")
            # print(cur.description)
            r = await cur.fetchone()
            print (r)

 
    pool.close()
    await pool.wait_closed()
loop = asyncio.get_event_loop()
loop.run_until_complete(test_example(loop))

