import datetime
from uuid import uuid1

from TaoBao.daos.Dao import *
from tools import log


class ProductDao(Dao):
    def __init__(self, cursor):
        super().__init__()
        self.cursor = cursor

    def insert(self, bean):
        insert_sql = INSERT.format(table="product",
                                   columns="id,create_time,name, standard_price,shop_price,comment_num, pay_num, sale_num, month_sale_num, collect_num, nid,cid,shop_id, url,search_key, raw_html",
                                   values="'%s','%s','%s', '%s','%s','%s', '%s', '%s', '%s', '%s', '%s','%s','%s', '%s', '%s', '%s'" %
                                          (uuid1(), datetime.datetime.now(), bean.name, bean.standard_price, bean.price, bean.comment_num, bean.pay_num, bean.sale_num, bean.month_sale_num, bean.collect_num, bean.nid, bean.cid, bean.shop_id, bean.url,
                                           bean.search_key,
                                           bean.raw_html))
        log.d("mysql insert:\n%s" % insert_sql)
        self.cursor.execute(insert_sql)

    def select_only(self, nid, key):
        dt = datetime.datetime.now().strftime("%Y-%m-%d")
        select_sql = SELECT.format(s="id",
                                   table="product") + "WHERE dt = 0 and search_key = '" + str(key) + "' and nid = '" + str(nid) + "' and create_time > '" + str(dt) + " 00:00:00.000000' and create_time < '" + str(dt) + " 23:59:59.999999'"
        log.d("mysql select:\n%s" % select_sql)
        num = self.cursor.execute(select_sql)
        return num, self.cursor.fetchall()
