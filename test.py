import json
from googletrans import Translator

from playwright.sync_api import sync_playwright


translator = Translator()


def pars_taobao(link: str):
    with (sync_playwright() as playwright):
        browser = playwright.firefox.launch(headless=False)
        context = browser.new_context()
        with open('taobao_cookies.json', 'r', encoding='utf-8') as f:
            context.add_cookies(json.load(f))

        page = context.new_page()
        page.goto(link)
        page.wait_for_selector('div[class="SkuContent--content--2UKSo-9"]')
        sort = page.query_selector('div[class="SkuContent--content--2UKSo-9"]')
        if sort:
            sort = translator.translate(sort.inner_text(), dest='ru').text
        size = page.query_selector('div[class="SkuContent--skuItem--3Nb1tMw"]')
        if size:
            size = translator.translate(size.inner_text(), dest='ru').text
        text = size + sort
        print(text)


pars_taobao('https://item.taobao.com/item.htm?id=772490903597&spm=a2141.241046-global.feeds.11&eurl=http://click.mz'
            '.simba.taobao.com/necpm&country=GLOBAL&itemIds=772490903597&scm=1007.35313.250647.0')
