import json
import re
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

        def check_res(res):
            try:
                if res.json()['ret'] == ["SUCCESS::调用成功"]:
                    return True
            except Exception as esx:
                print(esx)

        try:
            page.goto(link)
            with page.expect_response(
                    lambda response:
                    (response.url[:26] == "https://h5api.m.taobao.com") and check_res(response)
            ) as response_info:
                data = response_info.value.json()['data']
                link = page.url
                price = re.search('&price=(.+?)&', link).group(1)
        except Exception as es:
            print(es)
            data = False

    if data is not False:
        out = {'ok': True}
        if 'images' in data['item']:
            out['img'] = data['item']['images']
        if 'videos' in data['item']:
            out['videos'] = []
            for video in data['item']['videos']:
                out['videos'].append(video['url'])
        out['title'] = translator.translate(data['item']['title'], dest='ru').text
        out['price'] = f'{price} ¥'
        try:
            description = ''
            raw = data['componentsVO']['extensionInfoVO']['infos'][2]['items']
            for text in raw:
                description += text['text'][0]
                out['description'] = translator.translate(description, dest='ru').text
        except Exception as e:
            print(e)
        return out

    else:
        return {'ok': False}
