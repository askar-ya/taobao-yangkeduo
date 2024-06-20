import json
from googletrans import Translator

from playwright.sync_api import sync_playwright


translator = Translator()


def pars_yangkeduo(link: str):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context()
        with open('yangkeduo.json', 'r', encoding='utf-8') as f:
            context.add_cookies(json.load(f))

        page = context.new_page()
        try:
            page.goto(link)

            img_box = page.query_selector('._2wJiTrdH').query_selector_all('img')
            img = []
            for pic in img_box:
                if pic.get_attribute('src') is not None:
                    img.append(pic.get_attribute('src'))
                if pic.get_attribute('data-src') is not None:
                    img.append(pic.get_attribute('data-src'))
            if len(img) == 0:
                img = None
            price = page.query_selector('._1vQZeIX1').inner_text()

            description = page.query_selector('._1fdrZL9O.enable-select').inner_text()

            ok = True
        except Exception as e:
            print(e)
            ok = False

        # ---------------------
        context.close()
        browser.close()

    if ok:
        return {
            'ok': True,
            'price': f'{price} ¥',
            'description': translator.translate(description, dest='ru').text,
            'img': img
        }
    else:
        return {'ok': False}


def pars_taobao(link: str):
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=True)
        context = browser.new_context()
        with open('taobao_cookies.json', 'r', encoding='utf-8') as f:
            context.add_cookies(json.load(f))

        page = context.new_page()

        page.goto(link)
        try:
            out = {'ok': True}
            page.wait_for_selector('div[class="ItemHeader--root--kdR5m3q"]')
            title = page.query_selector('div[class="ItemHeader--root--kdR5m3q"]').inner_text()
            out['title'] = translator.translate(title, dest='ru').text
            price = page.query_selector('span[class="Price--priceText--1oEHppn"]').inner_text()
            out['price'] = f'{price} ¥'
            img_box = page.query_selector('ul[class="PicGallery--thumbnails--3EG14Q2"]').query_selector_all('img')
            out['img'] = []
            for i in img_box:
                out['img'].append('https:' + i.get_attribute('src'))

            sort = page.query_selector('div[class="SkuContent--content--2UKSo-9"]')
            if sort:
                sort = translator.translate(sort.inner_text(), dest='ru').text
            size = page.query_selector('div[class="SkuContent--skuItem--3Nb1tMw"]')
            if size:
                size = translator.translate(size.inner_text(), dest='ru').text
            specifications = size + sort
            out['specifications'] = specifications
        except Exception as e:
            print(e)
            out = {'ok': False}
        return out
