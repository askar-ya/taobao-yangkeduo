import re

import requests
from datetime import datetime

url = 'https://item.taobao.com/item.htm?app=chrome&bxsign=scdSa82St1NDXcCoJIm4M2P1ShNdAwoh9xWCVxUtQNZvK8tCv__m_0wZ6vjHUgRNCyDj-221lGv17ZZkFR_kujWIf4i0sDF-Oc7oZ0MOujcEiP9DaPlKgj2btIbXXfpixEDv6umBnGDy-mwtXS9IPwBbQ&cpp=1&id=769485838542&price=79&shareUniqueId=26801758149&share_crt_v=1&shareurl=true&short_name=h.gdStrWK2Sgj0pHE&sourceType=item&sp_tk=YzhmdVd2dUNEVG0=&spm=a2159r.13376460.0.0&suid=D13A5196-98DE-4D8B-B7F2-9FABC0572243&tbSocialPopKey=shareItem&tk=c8fuWvuCDTm&un=05b06129597522dc922338b8dff87dc9&un_site=0&ut_sk=1.ZMPh53VP/EADAKvVDYyt/w63_21380790_1716430758696.Copy.1'

url_params = {}
for param in ['id', 'bxsign', 'shareUniqueId', 'short_name', 'sp_tk', 'spm', 'suid', 'tk', 'un', 'price']:
    url_params[param] = re.search(f'&{param}=(.+?)&', url).group(1)

url_params['ut_sk'] = re.search('&ut_sk=(.+?)$', url).group(1)
url_params['queryParams'] = url[33:]

unix_time = int(datetime.now().timestamp() * 1000)

cookies = {
    'cookie2': '1e13b4f53d7ed52978e8126ed249a23e',
    't': 'ede510087c406ad82e9a7a289b168919',
    '_tb_token_': '31be7305be6b3',
    'hng': 'GLOBAL%7Czh-CN%7CUSD%7C999',
    'cna': 'FoDXHnL9YhYCAbJDhG+NAIVp',
    'xlly_s': '1',
    'thw': 'xx',
    '_samesite_flag_': 'true',
    '3PcFlag': '1716556339825',
    'unb': '2217953195578',
    'lgc': 'tb748025844907',
    'cancelledSubSites': 'empty',
    'cookie17': 'UUpgQcuYWbg1GGzUGA%3D%3D',
    'dnk': 'tb748025844907',
    'tracknick': 'tb748025844907',
    '_l_g_': 'Ug%3D%3D',
    'sg': '789',
    '_nk_': 'tb748025844907',
    'cookie1': 'BqPjxUXRk095jVsKveL1OibkScUEjZcFpS0EwmFGMFw%3D',
    'sgcookie': 'E100UOZjhInsKpLALhFDcTfsOHDiXnYh%2B5gmSBC0edlzOYA7ECSNIcUNs5rk9bt%2BvuBkgJqOKYRDZOp%2F6eRaF3kxqENs0W%2BpqaGJwR%2Fh%2BoMV7xQ%3D',
    'havana_lgc2_0': 'eyJoaWQiOjIyMTc5NTMxOTU1NzgsInNnIjoiZjY1ZmIwODhiY2E2NTQ0MmExZWY5NTRlZDk0YzEyMTMiLCJzaXRlIjowLCJ0b2tlbiI6IjFoUFc5d0VhMU0xUTlHWGZ0TzFVeGZBIn0',
    '_hvn_lgc_': '0',
    'havana_lgc_exp': '1715742541667',
    'cookie3_bak': '1e13b4f53d7ed52978e8126ed249a23e',
    'cookie3_bak_exp': '1716815676259',
    'wk_cookie2': '16d44228c3bf34a853967a45b773da09',
    'wk_unb': 'UUpgQcuYWbg1GGzUGA%3D%3D',
    'uc1': 'cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&pas=0&cookie14=UoYfp3HmwApjkg%3D%3D&cookie21=UtASsssmfufd&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false',
    'uc3': 'nk2=F5RCYRM7j8AVo2ib938%3D&lg2=Vq8l%2BKCLz3%2F65A%3D%3D&id2=UUpgQcuYWbg1GGzUGA%3D%3D&vt3=F8dD3eK0QfEcNhiT8BM%3D',
    'csg': 'fd5a29d2',
    'env_bak': 'FM%2BgytvMDRTiR2rW7D3DfjL5cqvezVHYqeeFZbrvHGTi',
    'skt': 'b7ecf64376c47260',
    'existShop': 'MTcxNjU1NjQ3Ng%3D%3D',
    'uc4': 'nk4=0%40FY4Jj1yMJc7hesWCVMxt9WVXGvwPnDfXbw%3D%3D&id4=0%40U2gqztLVmFUk0Vrp7iok47eCBnLL5gyL',
    '_cc_': 'U%2BGCWk%2F7og%3D%3D',
    '_uetsid': 'f4ec7120185111efadd3fdc16b6aee3b',
    '_uetvid': 'f4ec93a0185111efb45a954ff33fee33',
    'mtop_partitioned_detect': '1',
    '_m_h5_tk': '49eac2f27532ee5ddfcd42af790c9007_1716639056954',
    '_m_h5_tk_enc': '1f50b8f6b1bd63bec839f885702e2a4a',
    'tfstk': 'fmX-sZDbXr4lZ0PhFgNc8NKrhTq0iTIPDaSsKeYoOZQArG1kZMTHpwQdJUAQzLXdkaj1ZQjCKH6pUtfoKU4ypM_MpP4gIRjP4BJQSPYsejbkdHwHRZxsNR9edP4mivOzBp7M4VZ3eiZvxHhIPwt5coKylYtIFHgbDH8XRptWAxgXYHmSNeGTR7L3oFkdn2vK6OkelvMCh7RJWgGndv6v2QBCVECcitKJwFOc84DVFZjCETR4TXvFm1QdOZwxewQPV9OAKrmX6KTp1UW7xb85EHd6dInIdip2owtDCRgv0sslOT7-vvtPEOAp7IEILBvfIC11yDrNcLtC8CW37Y85AGWNsdeKhLdC4OBGBTUnSFKnNoExTXRWmP4gMnf5ub6BDFq0mXleMaKvSoExOXg36nLgmocETIQR.',
    'isg': 'BBsbL2n4-fOhsgUY7-3BcvVYqn-F8C_ysoTTBQ1Y95ox7DvOlcC_QjlqhlTiTIfq',
}

headers = {
    'authority': 'h5api.m.taobao.com',
    'accept': 'application/json',
    'accept-language': 'ru,en;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://item.taobao.com',
    'referer': 'https://item.taobao.com/',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
}

params = {
    'jsv': '2.6.1',
    'appKey': '12574478',
    't': str(unix_time),
    'sign': '4c134979860e1a28ceec5ee6c5ab90bb',
    'api': 'mtop.taobao.pcdetail.data.get',
    'v': '1.0',
    'isSec': '0',
    'ecode': '0',
    'timeout': '10000',
    'ttid': '2022@taobao_litepc_9.17.0',
    'AntiFlood': 'true',
    'AntiCreep': 'true',
    'dataType': 'json',
    'valueType': 'string',
    'preventFallback': 'true',
    'type': 'json',
    'data': '{"id":"769485838542","detail_v":"3.3.2","exParams":"{\\"app\\":\\"chrome\\",\\"bxsign\\":\\"scdSa82St1NDXcCoJIm4M2P1ShNdAwoh9xWCVxUtQNZvK8tCv__m_0wZ6vjHUgRNCyDj-221lGv17ZZkFR_kujWIf4i0sDF-Oc7oZ0MOujcEiP9DaPlKgj2btIbXXfpixEDv6umBnGDy-mwtXS9IPwBbQ\\",\\"cpp\\":\\"1\\",\\"id\\":\\"769485838542\\",\\"price\\":\\"79\\",\\"shareUniqueId\\":\\"26801758149\\",\\"share_crt_v\\":\\"1\\",\\"shareurl\\":\\"true\\",\\"short_name\\":\\"h.gdStrWK2Sgj0pHE\\",\\"sourceType\\":\\"item\\",\\"sp_tk\\":\\"YzhmdVd2dUNEVG0=\\",\\"spm\\":\\"a2159r.13376460.0.0\\",\\"suid\\":\\"D13A5196-98DE-4D8B-B7F2-9FABC0572243\\",\\"tbSocialPopKey\\":\\"shareItem\\",\\"tk\\":\\"c8fuWvuCDTm\\",\\"un\\":\\"05b06129597522dc922338b8dff87dc9\\",\\"un_site\\":\\"0\\",\\"ut_sk\\":\\"1.ZMPh53VP/EADAKvVDYyt/w63_21380790_1716430758696.Copy.1\\",\\"queryParams\\":\\"app=chrome&bxsign=scdSa82St1NDXcCoJIm4M2P1ShNdAwoh9xWCVxUtQNZvK8tCv__m_0wZ6vjHUgRNCyDj-221lGv17ZZkFR_kujWIf4i0sDF-Oc7oZ0MOujcEiP9DaPlKgj2btIbXXfpixEDv6umBnGDy-mwtXS9IPwBbQ&cpp=1&id=769485838542&price=79&shareUniqueId=26801758149&share_crt_v=1&shareurl=true&short_name=h.gdStrWK2Sgj0pHE&sourceType=item&sp_tk=YzhmdVd2dUNEVG0%3D&spm=a2159r.13376460.0.0&suid=D13A5196-98DE-4D8B-B7F2-9FABC0572243&tbSocialPopKey=shareItem&tk=c8fuWvuCDTm&un=05b06129597522dc922338b8dff87dc9&un_site=0&ut_sk=1.ZMPh53VP%2FEADAKvVDYyt%2Fw63_21380790_1716430758696.Copy.1\\",\\"domain\\":\\"https://item.taobao.com\\",\\"path_name\\":\\"/item.htm\\"}"}',
}

# params['data'] = params['data'].replace('id_value', url_params['id'])
# params['data'] = params['data'].replace('bxsign_value', url_params['bxsign'])

response = requests.get(
    'https://h5api.m.taobao.com/h5/mtop.taobao.pcdetail.data.get/1.0/',
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response.json())
