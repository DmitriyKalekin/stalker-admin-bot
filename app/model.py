# from async_generator import asynccontextmanager
# import aiomysql
from aiomysql import Warning as MysqlWarning

# @asynccontextmanager
# async def init_pool(app):
#     try:
#         if not app["pool"]:
#             app["pool"] = await aiomysql.create_pool(host=app["cfg"].MYSQL_HOST, port=app["cfg"].MYSQL_PORT,
#                             user=app["cfg"].MYSQL_USER, password=app["cfg"].MYSQL_PASS,
#                             db=app["cfg"].MYSQL_DBNM, loop=app["loop"], autocommit=True)
#         yield app["pool"]
#     finally:
#         if app["pool"]:
#             await app["pool"].close()
#     return


async def add_members(app, team_chat_id, members: list):
    async with app["conn"].cursor() as cur:
        for m in members:
            try:
                await cur.execute(f"""
                    INSERT IGNORE INTO teams_players 
                    SET
                        team_chat_id={int(team_chat_id)}, 
                        player_chat_id={int(m["id"])};
                """)
            except MysqlWarning:
                pass
    return True
    

async def kick_member(app, team_chat_id, m: dict):
    async with app["conn"].cursor() as cur:
        await cur.execute(f"""
            DELETE FROM teams_players 
                WHERE team_chat_id={int(team_chat_id)}  
                AND player_chat_id={int(m["id"])}
            LIMIT 100;
        """)
    return True

