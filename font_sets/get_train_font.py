import re
import requests
import logging

from typing import List
from fontTools.ttLib import TTFont

logging.basicConfig(level=logging.CRITICAL)
_fonts_path = "./font_sets"

_brand_url = "https://maoyan.com/board/1"

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


def get_font_content() -> bytes:
    response = requests.get(
        url=_brand_url,
        headers=headers
    )
    try:
        woff_url = re.findall(r"url\('(.*?\.woff)'\)", response.text)[0]
        font_url = f"http:{woff_url}"
    except Exception:
        raise

    return requests.get(font_url).content


def save_font() -> None:
    for i in range(7):
        font_content = get_font_content()

        with open(_fonts_path / f'{i + 1}.woff', 'wb') as f:
            f.write(font_content)


def get_coor_info(font, cli):
    glyf_order = font.getGlyphOrder()[2:]
    info = list()

    for i, g in enumerate(glyf_order):
        coors = font['glyf'][g].coordinates
        coors = [_ for c in coors for _ in c]
        coors.insert(0, cli[i])
        info.append(coors)

    return info


def get_font_data() -> List[List[List[int]]]:
    font_1 = TTFont(_fonts_path + "/1.woff")
    cli_1 = [2, 5, 8, 4, 1, 0, 3, 6, 9, 7]
    coor_info_1 = get_coor_info(font_1, cli_1)

    font_2 = TTFont(_fonts_path + "/2.woff")
    cli_2 = [5, 3, 9, 7, 4, 0, 1, 8, 2, 6]
    coor_info_2 = get_coor_info(font_2, cli_2)

    font_3 = TTFont(_fonts_path + "/3.woff")
    cli_3 = [2, 3, 1, 4, 5, 9, 6, 0, 7, 8]
    coor_info_3 = get_coor_info(font_3, cli_3)

    font_4 = TTFont(_fonts_path + "/4.woff")
    cli_4 = [3, 2, 4, 0, 8, 1, 7, 9, 6, 5]
    coor_info_4 = get_coor_info(font_4, cli_4)

    font_5 = TTFont(_fonts_path + "/5.woff")
    cli_5 = [3, 2, 5, 6, 8, 7, 4, 0, 9, 1]
    coor_info_5 = get_coor_info(font_5, cli_5)

    font_6 = TTFont(_fonts_path + "/6.woff")
    cli_6 = [4, 7, 9, 6, 1, 8, 2, 3, 5, 0]
    coor_info_6 = get_coor_info(font_6, cli_6)

    font_7 = TTFont(_fonts_path + "/7.woff")
    cli_7 = [5, 3, 9, 7, 4, 0, 1, 8, 2, 6]
    coor_info_7 = get_coor_info(font_7, cli_7)

    font_8 = TTFont(_fonts_path + "/8.woff")
    cli_8 = [4, 0, 6, 5, 2, 1, 9, 3, 8, 7]
    coor_info_8 = get_coor_info(font_8, cli_8)

    font_9 = TTFont(_fonts_path + "/9.woff")
    cli_9 = [2, 6, 3, 9, 1, 0, 8, 5, 7, 4]
    coor_info_9 = get_coor_info(font_9, cli_9)

    infos = coor_info_1 + coor_info_2 + coor_info_3 + coor_info_4 + coor_info_5 + coor_info_6 + \
            coor_info_7 + coor_info_8 + coor_info_9
    return infos
