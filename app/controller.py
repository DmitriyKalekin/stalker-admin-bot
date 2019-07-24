import app.model as model


async def process_command(app, r: dict):
    if "new_chat_members" in r["message"]:
        return await add_members(app, r)
    if "left_chat_member" in r["message"]:
        return await kick_member(app, r)
    return False


async def add_members(app, r: dict):
    return await model.add_members(app, r["message"]["chat"]["id"], list(r["message"]["new_chat_members"]))


async def kick_member(app, r: dict):
    return await model.kick_member(app, r["message"]["chat"]["id"], dict(r["message"]["left_chat_member"]))   