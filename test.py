import json
import re
from googletrans import Translator

from playwright.sync_api import sync_playwright


translator = Translator()


def pars_taobao(link: str):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()
        with open('taobao_cookies.json', 'r', encoding='utf-8') as f:
            context.add_cookies(json.load(f))

        page = context.new_page()

        try:
            page.goto(link)

            out = {'ok': True}
            page.wait_for_selector('div[class="ItemHeader--root--DXhqHxP"]')
            title = page.query_selector('div[class="ItemHeader--root--DXhqHxP"]').inner_text()
            out['title'] = translator.translate(title, dest='ru').text
            price = page.query_selector('span[class="Price--priceText--2nLbVda"]').inner_text()
            out['price'] = f'{price} ¥'
            img_box = page.query_selector('ul[class="PicGallery--thumbnails--1cEhJzK"]').query_selector_all('img')
            out['img'] = []
            for i in img_box:
                out['img'].append(i.get_attribute('src')[:-23])
            description = page.query_selector('div[class="ItemDetail--attrs--3t-mTb3"]').inner_text()
            out['description'] = translator.translate(description, dest='ru').text
        except Exception as e:
            out = {'ok': False, 'error': e}
        return out
