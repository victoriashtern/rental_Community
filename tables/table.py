class Table:
    def __init__(self, connection):
        self.connection = connection

    def truncate(self, table_name):
        sql = f"TRUNCATE TABLE {table_name}"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return sql
        except Exception as e:
            self.connection.rollback()
            raise ValueError(f"Error truncating table: {e} Table.truncate {sql}")

    def delete(self, table_name):
        sql = f"delete  from {table_name}"
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return sql
        except Exception as e:
            self.connection.rollback()
            raise ValueError(f"Error delete table: {e} Table.delete {sql}")

    def create(self, sql):
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql)
            self.connection.commit()
            cursor.close()
            return sql
        except Exception as e:
            self.connection.rollback()
            raise ValueError(f"Table.create. Error in create table: {e}  {sql}")