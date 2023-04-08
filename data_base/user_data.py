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
        # uuid = "c441eeca-734d-43f1-bde9-5a680d8487cc"
        query = select(
            self.employee_table
            ).where(
            self.employee_table.c.uuid == uuid
            )
        result = self.conn.execute(query).first()
        self.conn.close()
        # print(result.job_title.name)
        try:
            return result
        except AttributeError:
            return None
