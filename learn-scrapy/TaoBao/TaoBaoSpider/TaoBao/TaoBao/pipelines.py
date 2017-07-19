# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from uuid import uuid1

import pymysql
from scrapy.exceptions import DropItem

from TaoBao import conf
from TaoBao.beans.Product import Product
from TaoBao.beans.Shop import Shop
from TaoBao.daos.ProductDao import ProductDao
from TaoBao.daos.ShopDao import ShopDao
from tools import text_utils


class TaobaoPipeline(object):
    def process_item(self, item, spider):
        return item


class TTDataHandlerPipeline(object):
    """
    淘宝天猫数据处理
    """

    def process_item(self, item, spider):
        class__ = self.__class__
        if item is not None:
            if item["p_standard_price"] is None:
                item["p_standard_price"] = item["p_shop_price"]
            if item["p_shop_price"] is None:
                item["p_shop_price"] = item["p_standard_price"]

            item["p_collect_count"] = text_utils.to_int(item["p_collect_count"])
            item["p_comment_count"] = text_utils.to_int(item["p_comment_count"])
            item["p_month_sale_count"] = text_utils.to_int(item["p_month_sale_count"])
            item["p_sale_count"] = text_utils.to_int(item["p_sale_count"])
            item["p_standard_price"] = text_utils.to_string(item["p_standard_price"], "0")
            item["p_shop_price"] = text_utils.to_string(item["p_shop_price"], "0")
            item["p_pay_count"] = item["p_pay_count"] if item["p_pay_count"] is not "-" else "0"
            return item
        else:
            raise DropItem("Item is None %s" % item)


class MysqlPipeline(object):
    """
    存入数据库
    """
    count = 0

    def process_item(self, item, spider):
        db_connect = pymysql.connect(conf.DB.host, conf.DB.user_name, conf.DB.password, conf.DB.db_name, charset="utf8mb4")
        cursor = db_connect.cursor()
        self.count += 1
        print("第%s条" % self.count)
        shop = Shop()
        shop.id = uuid1()
        shop.type = item["s_type"]
        shop.rid = item["s_rid"]
        shop.created = item["s_created"]
        shop.modified = item["s_modified"]
        shop.shop_id = item["s_shop_id"]
        shop.shop_name = item["s_name"]
        shop.seller_id = item["s_seller_id"]
        shop.seller_nick = item["s_seller_nick"]
        shop.url = item["s_url"]
        shop.search_key = item["s_search_key"]
        shop.raw_html = item["s_raw_html"]

        shop_dao = ShopDao(cursor)
        by_shop_id = shop_dao.select_by_shop_id(shop.shop_id, shop.search_key)
        if by_shop_id[0] <= 0:
            shop_dao.insert(shop)

        product = Product()
        product.name = item["p_name"]
        product.standard_price = item["p_standard_price"]
        product.price = item["p_shop_price"]
        product.comment_num = item["p_comment_count"]
        product.pay_num = item["p_pay_count"]
        product.month_sale_num = item["p_month_sale_count"]
        product.sale_num = item["p_sale_count"]
        product.collect_num = item["p_collect_count"]
        product.nid = item["p_nid"]
        product.shop_id = shop.id
        product.url = item["p_url"]
        product.search_key = item["p_search_key"]
        product.cid = item["p_cid"]
        product.raw_html = item["p_raw_html"]

        product_dao = ProductDao(cursor)
        product_dao_select = product_dao.select_only(product.nid, product.search_key)
        if product_dao_select[0] <= 0:
            product_dao.insert(product)
        db_connect.commit()
        cursor.close()
        db_connect.close()
        return item
