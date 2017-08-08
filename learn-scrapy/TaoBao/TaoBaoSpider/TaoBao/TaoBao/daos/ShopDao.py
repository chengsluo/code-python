import datetime

from TaoBao.daos.Dao import *


class ShopDao(Dao):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor

    def insert(self, bean):
        insert_sql = INSERT.format(table="shop",
                                   columns="id,create_time,rid, created, modified, type,shop_id, shop_name,seller_id, seller_nick, url, raw_html, search_key",
                                   values="'%s','%s','%s', '%s','%s', %s, '%s', '%s', '%s','%s', '%s', '%s', '%s'" % (
                                       bean.id, datetime.datetime.now(), bean.rid, bean.created, bean.modified, bean.type, bean.shop_id,
                                       bean.shop_name, bean.seller_id, bean.seller_nick, bean.url, bean.raw_html, bean.search_key))
        print("mysql insert:\n" + insert_sql)
        self.cursor.execute(insert_sql)

    def select_by_shop_id(self, shop_id, key):
        select_sql = SELECT.format(table="shop", s="id") + "WHERE dt = 0 and shop_id = '" + str(shop_id) + "' and search_key='" + str(key) + "'"
        print("mysql select:\n" + select_sql)
        num = self.cursor.execute(select_sql)
        return num, self.cursor.fetchall()
