from TaoBao.beans.Bean import *


class Product(Bean):
    def __init__(self):
        """
        名称、标准价格、店内价格、评论次数、付款人数、销量、月销量、收藏数量、
        商品的淘宝、天猫ID、店铺Id,商品类目ID
        """
        super().__init__()
        self.name = ""
        self.standard_price = ""
        self.price = ""
        self.comment_num = 0
        self.pay_num = 0
        self.sale_num = 0
        self.month_sale_num = 0
        self.collect_num = 0
        self.nid = ""
        self.shop_id = ""
        self.cid = ""
