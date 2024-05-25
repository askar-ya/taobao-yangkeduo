import json
import requests
import re
from googletrans import Translator

from playwright.sync_api import sync_playwright


translator = Translator()


def pars_yangkeduo():
    with sync_playwright() as playwright:
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()
        with open('yangkeduo.json', 'r', encoding='utf-8') as f:
            context.add_cookies(json.load(f))

        page = context.new_page()
        page.goto('https://mobile.yangkeduo.com/goods.html?_wvx=10&refer_share_uin=TBGCYJCYIJXDUZWAGIBABL34XQ'
                  '_GEXDA&_oak_share_time=1716353890&share_uin=TBGCYJCYIJXDUZWAGIBABL34XQ_GEXDA&page_from=26&'
                  '_wv=41729&refer_share_channel=copy_link&refer_share_id=WRS3wI6mey9yLMc1zjAPtUMm9frcFCyr&_oak'
                  '_share_snapshot_num=9800&pxq_secret_key=DOVJTWHFI5F3Q2E3RANKTPKSTU5BEF474SJDYJ7VBCTH6OJVMPCA'
                  '&goods_id=579761211467')
        img_box = page.query_selector('._2wJiTrdH').query_selector_all('img')
        img = []
        for pic in img_box:
            if pic.get_attribute('src') is not None:
                img.append(pic.get_attribute('src'))
            if pic.get_attribute('data-src') is not None:
                img.append(pic.get_attribute('data-src'))
        print(img)
        print(len(img))
        price = page.query_selector('._15NyfC_w').inner_text()
        print(price)

        description = page.query_selector('._1fdrZL9O.enable-select').inner_text()
        print(description)

        page.wait_for_timeout(10000)
        # ---------------------
        context.close()
        browser.close()


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
