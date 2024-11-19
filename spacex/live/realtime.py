import json
import asyncio
from playwright.async_api import async_playwright

import sys,os
sys.path.append("/".join(os.path.abspath(__file__).split("\\")[:-3]))
from utils import sql

async def screen_shot_1(page, name,uid):
    while True:
        img = await page.screenshot(type="jpeg", full_page=True, quality=100)
        sql.insert_img(name,uid, img)
        await asyncio.sleep(10)

async def screen_shot_2(page, name):
    while True:
        await page.screenshot(path=f'../views/live/data/{name}.jpeg',
                              type="jpeg", quality=100)
        await asyncio.sleep(1.5)

async def open_live(rooms_id,rooms_name):
    with open('../config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        #bili_cookies = config["cookies"]["bili"][0]
        executable_path = config["executable_path"]

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=executable_path, headless=False)
        context = await browser.new_context()
        #await context.add_cookies(bili_cookies)
        tasks = []
        for id in rooms_id:
            page = await context.new_page()
            await page.goto(f'https://live.bilibili.com/{id}')
            tasks.append(asyncio.create_task(screen_shot_1(page,rooms_name[id],id)))
            tasks.append(asyncio.create_task(screen_shot_2(page, rooms_name[id])))
        await asyncio.gather(*tasks)

if __name__ == '__main__':


    with open('config/rooms.json', 'r', encoding='utf-8') as f:
        a = json.load(f)['rooms']
    rooms_id = [a[i] for i in a]
    rooms_name = {a[i]: i for i in a}

    asyncio.run(open_live(rooms_id,rooms_name))
