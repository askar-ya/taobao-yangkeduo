import requests

import json
import re

from datetime import datetime

unix_time = int(datetime.now().timestamp() * 1000)


url = 'https://item.taobao.com/item.htm?app=chrome&bxsign=scdSa82St1NDXcCoJIm4M2P1ShNdAwoh9xWCVxUtQNZvK8tCv__m_0wZ6vjHUgRNCyDj-221lGv17ZZkFR_kujWIf4i0sDF-Oc7oZ0MOujcEiP9DaPlKgj2btIbXXfpixEDv6umBnGDy-mwtXS9IPwBbQ&cpp=1&id=769485838542&price=79&shareUniqueId=26801758149&share_crt_v=1&shareurl=true&short_name=h.gdStrWK2Sgj0pHE&sourceType=item&sp_tk=YzhmdVd2dUNEVG0=&spm=a2159r.13376460.0.0&suid=D13A5196-98DE-4D8B-B7F2-9FABC0572243&tbSocialPopKey=shareItem&tk=c8fuWvuCDTm&un=05b06129597522dc922338b8dff87dc9&un_site=0&ut_sk=1.ZMPh53VP/EADAKvVDYyt/w63_21380790_1716430758696.Copy.1'


url_params = {}
for param in ['id', 'bxsign', 'shareUniqueId', 'short_name', 'sp_tk', 'spm', 'suid', 'tk', 'un', 'price']:
    url_params[param] = re.search(f'&{param}=(.+?)&', url).group(1)

url_params['ut_sk'] = re.search('&ut_sk=(.+?)$', url).group(1)
url_params['queryParams'] = url[33:]
# url_params['unix_time'] = str(unix_time)

with open('requests_auth.json', 'r', encoding='utf-8') as f:
    requests_data = json.load(f)

cookies = requests_data['taobao']['cookies']

headers = requests_data['taobao']['headers']

params = requests_data['taobao']['params']
params['t'] = str(unix_time)
param_data = params['data']

for param in list(url_params):
    param_value = url_params[param]
    param_data = param_data.replace(f'{param}_value', param_value)

params['data'] = param_data
params['sign'] = '4c134979860e1a28ceec5ee6c5ab90bb'
print(params)

response = requests.get(
    'https://h5api.m.taobao.com/h5/mtop.taobao.pcdetail.data.get/1.0/',
    params=params,
    cookies=cookies,
    headers=headers,
)

print(response.text)
