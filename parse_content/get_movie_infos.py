# @Time    : 2023/3/13 0:03
# @Author  : tamya2020
# @File    : get_movie_infos.py
# @Description :
import io
import random
import re
import itertools
import requests
import execjs
from fontTools.ttLib import TTFont

from parse_content.knn_font_crack import FontClassify
from parse_content.ohRequest import LoadUserAgent


class KnnMaoYanTop100:
    def __init__(self):
        # https://www.maoyan.com/ajax/films/1200486?timeStamp=1678722467126&index=8&signKey=9918ed19ac879c705d12c5cb6e436ac6&channelId=40011&sVersion=1&webdriver=false
        self.obj = FontClassify()
        self.UAS = LoadUserAgent()

    @staticmethod
    def get_ajax_params():
        with open('./parse_content/params_crack.js', 'r', encoding='utf-8') as f:
            maoyan_js = f.read()
        params = execjs.compile(maoyan_js).call('getParams')
        print("11111111")
        return params

    @staticmethod
    def get_ajax_url_params():
        resp = requests.get("http://127.0.0.1:2229/encrypt")
        params = resp.json()
        return params

    @staticmethod
    def get_font_coordinate_list(font_obj, uni_list):
        """
        获取字体文件的坐标信息列表
        :param font_obj: 字体文件对象
        :param uni_list: 总体文件包含字体的编码列表或元祖
        :return: 字体文件所包含字体的坐标信息列表
        """
        font_coordinate_list = list()
        for uni in uni_list:
            # 每个字的GlyphCoordinates对象，包含连线位置坐标（x,y）元组信息
            word_glyph = font_obj['glyf'][uni].coordinates
            # 将[(147, 151), (154, 89),]转化为[ ,]
            coordinate_list = list(itertools.chain(*word_glyph))
            # 汇总所有文字坐标信息
            font_coordinate_list.append(coordinate_list)

        return font_coordinate_list

    @staticmethod
    def get_font_content(response):
        """

        :param response:
        :return: 原始自定义字体的二进制文件内容
        """
        new_font_url = re.findall(r'format\("embedded-opentype"\).*?url\("(.*?)"\)', response, re.S)
        assert len(new_font_url) > 0, "Not Found Font File"
        bytes_font = requests.get("https:" + new_font_url[0]).content

        return bytes_font

    def get_map(self, font_coordinate_list, glyf_order):
        """

        :param font_coordinate_list:
        :param glyf_order:
        :return:
        """
        map_li = map(lambda x: str(int(x)), self.obj.knn_predict(font_coordinate_list))
        uni_li = map(lambda x: x.lower().replace('uni', '&#x') + ';', glyf_order)
        return dict(zip(uni_li, map_li))

    def replace_font_text(self, url, refer_url):
        """

        :param url:
        :param refer_url:
        :return:
        """
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
            # "Cookie": "uuid_n_v=v1; uuid=4E14D470C1B611EDAA5BB1A1595AB3D2E5BF520CAE4B4E168F76DD58295DC82D; _lxsdk_cuid=186010599f3c8-010c4f4df5e3d2-26021051-1fa400-186010599f3c8; __mta=143422090.1675054390092.1678723877215.1678723905548.63; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1678455655,1678497758,1678710297,1678785144; _csrf=998113eb6edb3a9d9a6841a011af0b58985fed43fe1578853805605ba6898f4d; WEBDFPID=2v13891971y3534yy0u26zuxv01w29v7813v9v33xw8979589zv9ww17-1994170442679-1678810442679AEIYUKWfd79fef3d01d5e9aadc18ccd4d0c95074352; token=AgG7IIWzRz7k1EgWyQDaZIfxYadu823QdBbqEyKigoZx8-hZWTaoEDsTno-5rks8Mn_ZO0fX4yCizgAAAABPFwAA4KazWVaoRXBwYyfojR5LXXAaywHyJfPuIz2QH48BOWfez5O2tbVz65lDObFKiD1D; uid=2561278301; uid.sig=IsKWaOWGuz3PIjnWSh10CS6NMqc; _lxsdk=4E14D470C1B611EDAA5BB1A1595AB3D2E5BF520CAE4B4E168F76DD58295DC82D; _lxsdk_s=186e0e646af-31d-fe7-4ec%7C%7C9; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1678810574"
            # 'Referer': refer_url
        }
        # params = self.get_ajax_params()
        params = self.get_ajax_url_params()
        print(params)
        resp = requests.get(url=url, headers=headers, params=params)

        text = resp.text
        print(f"text:{len(text)}")
        b_font = self.get_font_content(text)

        new_font = TTFont(io.BytesIO(b_font))
        # 读取新字体坐标,去除第一个空值
        glyf_order = new_font.getGlyphOrder()[2:]
        font_coordinate_list = self.get_font_coordinate_list(new_font, glyf_order)
        map_dict = self.get_map(font_coordinate_list, glyf_order)

        for uni in map_dict.keys():
            text = text.replace(uni, map_dict[uni])

        return text
