import app.model as model
from app.telebot import GroupChatTele, UserTele
# import inspect

async def process(app, r: dict):
    print("CTL HERE")
    if "new_chat_members" in r["message"]:
        print("CTL:", "on_group_add_members")
        return await on_group_add_members(app, r)
    if "left_chat_member" in r["message"]:
        print("CTL:", "on_group_kick_member")
        return await on_group_kick_member(app, r)
    if "group_chat_created" in r["message"] and r["message"]["group_chat_created"]:
        print("CTL:", "on_group_create")
        return await on_group_create(app, r)
    if "new_chat_title" in r["message"]:
        print("CTL:", "on_group_rename")
        return await on_group_rename(app, r)
    if "text" in r["message"] and r["message"]["text"][:3] == "ПСК":
        return await on_object_found(app, r)
    return False

async def on_object_found(app, r: dict):
    # https://www.google.com/maps/@54.9774488,73.3911583,19z
    group_chat = GroupChatTele(r["message"]["chat"])
    user = UserTele(r["message"]["from"])
    rank = str(await model.get_user_rank(user.id))
    rank = rank[0].upper() + rank[1:]      
    code = r["message"]["text"].strip().upper()
    obj = await model.get_artefact_by_search_code(app, code)
    if not obj:
        resp = await app.telebot.sendMessage(group_chat.id, f"🚫 Артефакт с кодом: `{code}` не обнаружен!")
    else:
        resp = await app.telebot.sendMessage(group_chat.id, f"*Новости ЗОНЫ 27.07.2019*\n🔍 Обнаружен артефакт: № `{obj['id']}`\n👨‍🦰 Нашедший: `{rank}` *{user.full_name}*\n⭐️ Слава героям!")
        resp = await app.telebot.sendPhoto(group_chat.id, photo=f"https://eva-bot.ru/img/{obj['id']}.jpg", caption=f"Артефакт №`{obj['id']}`: {obj['title']}")
        resp = await app.telebot.sendMessage(group_chat.id, f"*Информация об артефакте:*\nID: {obj['id']}\nКласс: {obj['class_name']}\n```\n{obj['descr']}\n```\nСПРАВКА ИЗ АРХИВА:\n```\n{obj['class_descr']}\n```\n")
        resp = await app.telebot.sendMessage(group_chat.id, f"🎯*Приказ №1073 на уничтожение*\nСОВЕРШЕННО СЕКРЕТНО!\nЗа контакт с опасным артефактом № `{obj['id']}` необходимо уничтожить военного группы КРАСНЫЕ.\nОбъект `{rank} {user.full_name}` подлежит уничтожению.\nОбъект вооружён, представляет опасность и способен к мутации. Сохраняйте осторожность!\n🎖 Военный комитет контроля Зоны")


async def on_group_create(app, r: dict):
    group_chat = GroupChatTele(r["message"]["chat"])
    admin = UserTele(r["message"]["from"])
    await model.group_create(app, group_chat, admin)
    resp = await app.telebot.sendMessage(
        group_chat.id, 
        f"""
        ❗️ Отряд `{group_chat.title}` зарегистрирован командиром *{admin.full_name}*.\nМне нужно лично осмотреть всех бойцов.\n1. Пусть каждый напишет мне в личку: https://t.me/StalkerAdminBot\n2. Каждый подтвердит участие в этом групповом чате, написав `/j`.
        """)
    return True

async def on_group_rename(app, r: dict):    
    group_chat = GroupChatTele(r["message"]["chat"])
    new_chat_title = str(r["message"]["new_chat_title"])
    await model.group_rename(app, group_chat, new_chat_title)
    resp = await app.telebot.sendMessage(
        group_chat.id, 
        f"❗️ Новое название отряда: `{new_chat_title}`")
    return True

async def on_bot_added_to_group(app, r: dict):
    """
    DEPRECATED
    """
    pass



async def on_group_add_members(app, r: dict):
    group_chat = GroupChatTele(r["message"]["chat"])
    members = list(r["message"]["new_chat_members"])
    add_success = await model.group_add_members(app, group_chat, members)
    if not add_success:
        return False
    if len(members) == 0:
        return False
    txt = ""
    for m in members:
        user = UserTele(m)
        if user.is_bot:
            txt += f"👁 `Наблюдатель` *{user.full_name}* присоединился в отряд"
            await model.group_create(app, group_chat, UserTele(r["message"]["from"]))
        else:
            rank = str(await model.get_user_rank(user.id))
            rank = rank[0].upper() + rank[1:]    
            txt += f"⭐️ `{rank}` *{user.full_name}* присоединился в отряд"
    await app.telebot.sendMessage(group_chat.id, txt)
    return True

async def on_group_kick_member(app, r: dict):
    group_chat = GroupChatTele(r["message"]["chat"])
    user = UserTele(r["message"]["left_chat_member"])
    rank = str(await model.get_user_rank(user.id))
    rank = rank[0].upper() + rank[1:]
    kick_success = await model.group_kick_member(app, group_chat.id, user) 
    txt = f"❌ `{rank}` *{user.full_name}* покинул отряд"
    await app.telebot.sendMessage(group_chat.id, txt)  
    return kick_success

async def on_group_mention_member(app, r: dict):
    group_chat_id = r["message"]["chat"]["id"]
    await model.kick_member(app, group_chat_id, dict(r["message"]["left_chat_member"]))   
    return True    

