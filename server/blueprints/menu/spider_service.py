# coding=utf-8
import re
import requests
from bs4 import BeautifulSoup, element


class SpiderService:
    def __init__(self, url):
        self.url = url
        # header and timeout, 防止网站屏蔽
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.6.3",
            "Content-Type": "text/plain; charset=utf-8",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Accept": "*/*"
        }
        html = requests.get(url, headers=headers, timeout=1).text
        self.soup = BeautifulSoup(html)

    def get_menus(self):
        item = self.soup.find('div', attrs={'id': 'cate_view'})
        sections = item.findAll('section')
        if not item:
            return 'error:"cate_view"not found'
        menus = []
        for section in sections:
            menu = {}
            classname = section.h2.text  # example:馄饨系列
            menu['classname'] = classname
            menu['dishs'] = []
            dishlists = section.findAll('ul')  # ul, class=rst-menu-img-list or rst-menu-list
            for dishlist in dishlists:
                foods = dishlist.findAll('li')
                for food in foods:
                    # print food
                    dish = dict()
                    dish['name'] = food.find('a', {'class': 'rst-d-name'}).text
                    if food.find('span', {'class': 'rst-d-sales'}) is None:
                        dish['sales'] = None
                    else:
                        dish['sales'] = food.find('span', {'class': 'rst-d-sales'}).text

                    if food.find('span', {'class': 'symbol-rmb'}) is None:  # if None means sale out
                        continue
                    else:
                        dish['price'] = food.find('span', {'class': 'symbol-rmb'}).text

                    dish['img'] = food.find('img', {'class': 'rst-d-img'}).get('srcset')  # meybe None
                    menu['dishs'].append(dish)

            menus.append(menu)
        return menus


# 单个【food】页面结构如下：
# <li class="rst-dish-img-item eleme_view" id="food_view_13565105">
# <a class="dish-favor favor_btn" title="收藏">♥</a>
# <a class="rst-d-img-wrapper food_img">
# <img alt="青岛冰纯" class="rst-d-img" srcset="http://fuss10.elemecdn.com/a/84/b7fc142738f556c646f9e25f29a1bjpeg.jpeg?w=240&amp;h=180 1x,http://fuss10.elemecdn.com/a/84/b7fc142738f556c646f9e25f29a1bjpeg.jpeg?w=480&amp;h=360 2x"/></a>
# <div class="rst-d-img-dish">
# <a class="rst-d-name food_name" title="青岛冰纯">青岛冰纯</a>
# <br>
# <span class="rst-d-rating food_rating cmt_block">
# <i class="icon-d-star s10 i_s"></i>(1)</span><br>
# <span class="rst-d-sales cmt_block">月售7份</span><div class="rst-d-action r_d_a">
# <div class="rst-d-act narrow act_btns"><a class="rst-d-act-add add_btn" role="button" title="点击饿一份"><span class="rst-d-act-glyph"></span><span class="price symbol-rmb">4</span></a><a class="rst-d-act-toggle caret add_main_btn" role="button"></a></div> </div><div class="rst-d-note">
# <span class="rst-d-ordered dish_state hide"></span>
# </div></br></br></div>
# </li>



