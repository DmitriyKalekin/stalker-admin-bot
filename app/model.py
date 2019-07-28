# from async_generator import asynccontextmanager
import aiomysql
from aiomysql import Warning as MysqlWarning
from app.telebot import GroupChatTele, UserTele

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

async def get_artefact_by_search_code(app, code: str):
    code = code.strip().upper()
    async with app.pool.acquire() as conn:    
        async with conn.cursor(aiomysql.DictCursor) as cur:
            q = f"""
                SELECT 
                    t1.id,
                    t1.title,
                    t1.artefact_class_id,
                    t1.descr,
                    t1.code_found,
                    t2.name as class_name,
                    t2.class_descr as class_descr 
                FROM artefacts t1
                INNER JOIN artefact_class t2
                ON t1.artefact_class_id = t2.id
                WHERE code_found={conn.escape(code)}
                LIMIT 1;
            """        
            # try:
            # print(q)
            await cur.execute(q)
            r = await cur.fetchall()
            if r and len(r) > 0:
                return r[0]
    return False




async def get_user_rank(user_id: int) -> str:
    assert type(user_id) == int
    assert user_id > 0
    return "рядовой"

async def group_create(app, team: GroupChatTele, admin: UserTele):
    async with app.pool.acquire() as conn:    
        async with conn.cursor() as cur:
            q = f"""
                INSERT IGNORE INTO teams 
                SET
                    id={int(team.id)}, 
                    name={conn.escape(team.title)},
                    admin_id={int(admin.id)};
            """        
            # try:
            await cur.execute(q)
            # except MysqlWarning as e:
            #     print("MysqlWarning:", e, q)
            #     return False
            # except Exception as e:
            #     print("Exception:", e, q)
            #     return False                
    return True

async def group_rename(app, team: GroupChatTele, new_chat_title: str):
    async with app.pool.acquire() as conn:    
        async with conn.cursor() as cur:
            q = f"""
                UPDATE teams 
                SET name={conn.escape(new_chat_title)}
                WHERE id={int(team.id)}
                LIMIT 1;
            """        
            # try:
            await cur.execute(q)
            # except MysqlWarning as e:
            #     print("MysqlWarning:", e, q)
            #     return False
            # except Exception as e:
            #     print("Exception:", e, q)
            #     return False                
    return True    

async def group_add_members(app, team: GroupChatTele, members: list):
    async with app.pool.acquire() as conn:    
        async with conn.cursor() as cur:
            for m in members:
                user = UserTele(m)
                if user.is_bot:
                    continue
                q = f"""
                    INSERT IGNORE INTO teams_players 
                    SET
                        team_id={int(team.id)}, 
                        team_name={conn.escape(team.title)},
                        player_id={int(user.id)},
                        player_name={conn.escape(user.full_name)};
                """            
                try:
                    await cur.execute(q)
                except MysqlWarning as e:
                    print("MysqlWarning:", e, q)
                    return False
                except Exception as e:
                    print("Exception:", e, q)
                    return False                
    return True
    

async def group_kick_member(app, team_id: int, user: UserTele):
    async with app.pool.acquire() as conn:    
        async with conn.cursor() as cur:
            await cur.execute(f"""
                DELETE FROM teams_players 
                    WHERE team_id={int(team_id)}  
                    AND player_id={int(user.id)}
                LIMIT 100;
            """)
    return True

