from fastapi import FastAPI, Request, Query
import uvicorn
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
from bot.pydantic_models import log_models
from bot.pydantic_models import user_models
from bot.db.user_db import User_DB
from bot.db.slaves import Slaves_DB
import logging
from fastapi.responses import JSONResponse
from aiogram.utils.deep_linking import create_start_link, decode_payload
from bot.create_bot import bot

app = FastAPI()
# Настройка Jinja2
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "site/templates"))
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "site/static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})


@app.get("/slaves", response_class=HTMLResponse)
async def read_slaves(request: Request):
    return templates.TemplateResponse("slaves.html", {"request": request})


@app.get("/top_players", response_class=HTMLResponse)
async def read_top_players(request: Request):
    return templates.TemplateResponse("top_players.html", {"request": request})


@app.post("/logs/")
async def logs(log: log_models.Log):
    logger.info(log.data)
    return JSONResponse(content={'success': True})


@app.post('/check_user/')
async def check_user(user: user_models.UserData):
    status = User_DB().check_user(user)

    return JSONResponse(content={'success': status, 'user_id': user.user_id,
                                 'username': user.username})


@app.get('/invite_link/')
async def get_invite_link(user_id: int = Query(...)):
    try:
        link = await create_start_link(bot, str(user_id), encode=True)
        link_id = link.split('=')[-1]
        status = User_DB().check_invite_link(user_id, link_id)
        if status == 1:
            logger.info('Пользователь добавил свою ссылку впервые')
        return JSONResponse(content={'success': 1, 'invite_link': link})
    except Exception as e:
        return JSONResponse(content={'success': 0, 'error': str(e)})
@app.get('/get_slaves/')
async def get_slaves(user_id: int = Query(...)):
    try:
        slaves = Slaves_DB().get_slaves(user_id)
        data = []
        for slave in slaves:
            user_info = User_DB().get_user_info_by_id(slave['slave_id'])
            data.append({'user_id': user_info['user_id'],
                'first_name': user_info['first_name'],
                         'photo_url': user_info['photo_url']})
        return JSONResponse(content={'success': True, 'slaves': data})
    except Exception as e:
        return JSONResponse(content={'success': False, 'error': str(e)})


def run_fastapi():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO

    )

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )


logger = logging.getLogger(__name__)
if __name__ == "__main__":
    run_fastapi()
