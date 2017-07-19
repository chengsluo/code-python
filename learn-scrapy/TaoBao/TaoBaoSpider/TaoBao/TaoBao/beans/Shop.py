from TaoBao.beans.Bean import Bean


class Shop(Bean):
    def __init__(self):
        """
        店铺类型。1:淘宝。2：天猫、店铺编号、
        店铺类目编号、店铺开店时间、店铺修改时间、店铺Id、店铺名称、
        卖家id、卖家昵称
        """
        super().__init__()
        self.type = 1
        self.rid = ""
        self.created = ""
        self.modified = ""
        self.shop_id = ""
        self.shop_name = ""
        self.seller_id = ""
        self.seller_nick = ""
