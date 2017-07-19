INSERT = "INSERT INTO {table}({columns}) VALUES ({values}) "
UPDATE = "UPDATE {table} SET "
DELETE = "UPDATE {table} SET dt = 1 WHERE id = {id}"
SELECT = "SELECT {s} from {table} "


class Dao:
    def __init__(self):
        pass

    def insert(self, bean):
        pass

    def delete(self, id):
        pass

    def update(self, bean):
        pass

    def select(self, id):
        pass

    def selects(self):
        pass
