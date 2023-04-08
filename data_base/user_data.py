from sqlalchemy import create_engine, Table, MetaData, select

from settings.config import DATABASE_URL


class DBUserData:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData()
        self.employee_table = Table('app_employee',
                                    self.metadata,
                                    # autoload=True,
                                    autoload_with=self.engine
                                    )

        # создаем соединение с БД
        self.conn = self.engine.connect()

    def get_user_data(self, uuid: str):
        query = select(
            self.employee_table.c.uuid
            ).where(
            self.employee_table.c.id == 8
            )
        result = self.conn.execute(query).fetchone()
        self.conn.close()
        return result._data[0]
