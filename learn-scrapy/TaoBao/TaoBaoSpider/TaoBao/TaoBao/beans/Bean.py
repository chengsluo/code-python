class Bean:
    """
    创建时间、更新时间、删除时间、删除标志（1：已删除）、id、
    html地址、html内容
    """

    def __init__(self):
        self.create_time = ""
        self.update_time = ""
        self.delete_time = ""
        self.dt = 0
        self.id = ""
        self.url = ""
        self.raw_html = ""
        self.search_key = ""
