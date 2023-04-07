from sqlalchemy import create_engine, Table, MetaData

from settings.config import DATABASE_URL


class DBUserData:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData()
        self.employee_table = Table('app_employee',
                                    self.metadata,
                                    # autoload=True,
                                    # autoload_with=self.engine
                                    )

        # создаем соединение с БД
        self.conn = self.engine.connect()

    def get_user_data(self, uuid: str):
        query = self.employee_table.select()
        result = self.conn.execute("""
            SELECT * FROM app_employee WHERE id=8;
            """)
        for row in result:
            print(row)

        # закрываем соединение
        self.conn.close()
