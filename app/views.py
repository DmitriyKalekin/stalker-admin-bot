from aiohttp import web
# import random
import app.controller as ctl
# from app.telebot import Callback, Message
# from app.commands import MessageInvoker, CallbackInvoker
# from app.events import EventMessage, EventCallback


async def index(request):
    # query_string lat=55.0514272&lng=82.8938919&time=2019-07-23T09:43:11.236Z&s=0.0

    # print(request.app.router.__dict__["_resources"])
    print("--INDEX----")
    # r = await request.json()
    # print(r)
    # print(type(request))
    # print("DICT", request.__dict__)
    # r = await request.text()  #json()  #.json()
    # r2 = await request.release()
    # print("=====")
    # print("TEXT", r)
    # print("REL", r2)
    try:
        pass
        # print("query_string", request.query_string)
    except:
        pass
    try:
        print("JSON", await request.json())
    except:
        pass       
    try:
        pass
        # print("TEXT", await request.text())
    except:
        pass              
    # lat = request.rel_url.query['lat']
    # lng = request.rel_url.query['lng']
    # time = request.rel_url.query['time']
    # s = request.rel_url.query['s']
    # print("lat:", lat)
    # print("lng:", lng)
    # print("time:", time)
    # print("s:", s)
    # print("GET", await request.get("id"))
    # ppp = await request.post()
    # print("POST", ppp, request.POST)
    # print(request.app.router.__dict__["_resources"][3].__dict__)
    return web.json_response({
        "status": 200, 
        "_resources": [str(s._path) for s in request.app.router.__dict__["_resources"]], 
        "_named_resources": [str(s._path) for s in request.app.router.__dict__["_named_resources"]]
        })


async def run_wh(request):
    r = await request.json()
    print("---- /run_wh -----")
    print(r)
    if "message" not in r:
        return web.json_response({"status": 200, "details": "no_message"})
    if "chat" not in r["message"]:
        return web.json_response({"status": 200, "details": "no_chat"})    
    await ctl.process_command(request.app, r)
    return web.json_response({"status": 200, "details": "ok"})  

    # if "message" in r:
    #     user_id = r["message"]["from"]["id"]
    #     r = await request.app.telebot.sendMessage(user_id, f"Тест инициации ботом общения.")
    #     print("====ANS:====")
    #     print(r)
    # main_key = "message"
    # if main_key not in r:
    #     main_key = "edited_message"
    # if main_key not in r:
    #     return web.json_response({"status": 400, "index": "no message"})
    # if "id" not in r[main_key]["from"]:
    #     return web.json_response({"status": 400, "index": "no chat_id"})

    # chat_id = r[main_key]["from"]["id"]
    # username = r[main_key]["from"].get("first_name", "") + " " + r[main_key]["from"].get("last_name", "")
    # if username.strip() == "":
    #     username = "Боец"

    # if "location" not in r[main_key]:
    #     await request.app.telebot.sendMessage(chat_id, f"Привет, *{username}*!\nЯ мастер над квестами, ты должен меня слушаться. Можешь называть меня `Мастер` или `Отец`.")
    #     await request.app.telebot.sendMessage(chat_id, f"*Первое задание*\nВот твоё первое задание. Нажми с мобильного телефона в этом чате на скрепку, выбери `Геопозиция` и выбери `Отправить свою геопозицию`")
    # else:
    #     lat = r[main_key]["location"]["latitude"] - 0.005
    #     lng = r[main_key]["location"]["longitude"] - 0.005
    #     await request.app.telebot.sendMessage(
    #         chat_id, 
    #         f"`Квест активирован`\nОтлично! Вот тебе точка на карте, куда нужно добраться",
    #         reply_markup={
    #             "inline_keyboard": [
    #                 [{"text": "🎯 Твоя цель на карте", "url": f"https://eva-bot.ru/map/index.php?quest_lat={lat}&quest_lng={lng}&nocache={random.random()}"}]      
    #             ]
    #         },
    #         parse_mode="markdown"  
    #     )

    return web.json_response({"status": 200, "index": "ok"})


async def set_wh(request):
    res = await request.app["telebot"].setWebhook(request.app["cfg"].WH_URL)
    return web.json_response(res)


async def get_wh(request):
    return web.json_response(await request.app["telebot"].getWebhookInfo())


async def del_wh(request):
    return web.json_response(await request.app["telebot"].deleteWebhook())


async def start_job(request):
    # player_id = 32768
    # payload = {}
    # await request.app.model.create_job(player_id, payload)
    return web.json_response({"status": 200})


# async def bad_request(e):
#     return web.json_response({
#         "status":   {
#             "code": 400,
#             "errorType": "bad_request",
#             "errorDetails": "Bad request"
#         }
#     }), 400


# async def page_not_found(e):
#     return web.json_response({
#         "status":   {
#             "code": 404,
#             "errorType": "not_found",
#             "errorDetails": "Not found this API section"
#         }
#     }), 404


# async def internal_server_error(e):
#     return web.json_response({
#         "status":   {
#             "code": 500,
#             "errorType": "not_supported",
#             "errorDetails": "This query is not supported"
#         }
#     }), 500