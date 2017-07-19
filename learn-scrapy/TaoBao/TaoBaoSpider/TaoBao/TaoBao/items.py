# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class TmallAndTaoBaoItem(scrapy.Item):
    """
    淘宝天猫数据Item
    """
    p_name = Field()
    p_comment_count = Field()
    p_sale_count = Field()
    p_shop_price = Field()
    p_standard_price = Field()
    p_collect_count = Field()
    # 商品ID
    p_nid = Field()
    # 商品类目
    p_cid = Field()
    p_pay_count = Field()
    p_url = Field()
    p_raw_html = Field()
    p_month_sale_count = Field()
    p_search_key = Field()

    s_name = Field()
    #  商店类目ID
    s_rid = Field()
    s_created = Field()
    s_modified = Field()
    s_shop_id = Field()
    s_seller_id = Field()
    s_seller_nick = Field()
    s_search_key = Field()
    s_type = Field()
    s_url = Field()
    s_raw_html = Field()
