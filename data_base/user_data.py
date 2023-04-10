from sqlalchemy import create_engine, Table, MetaData, select, update

from settings.config import DATABASE_URL


class DBUserData:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.metadata = MetaData()
        self.employee_table = Table('app_employee',
                                    self.metadata,
                                    autoload_with=self.engine
                                    )
        self.app_jobtitle = Table('app_jobtitle',
                                  self.metadata,
                                  autoload_with=self.engine
                                  )
        self.conn = self.engine.connect()

    def add_user_telegram_id_to_db(self, user_id: str,
                                   telegram_user_id: str):
        """
        Добавляет id пользователя телеграма в БД
        """
        print(user_id, telegram_user_id)
        query = update(
            self.employee_table
            ).where(
            self.employee_table.c.id == user_id
            ).values(telegram_user_id=telegram_user_id,)
        print(query)
        print(query.compile().params)
        result = self.conn.execute(query)
        print(result.rowcount)
        self.conn.close()

    async def get_user_data(self, uuid: str,
                            telegram_user_id: str) -> dict:
        dict = {'surname': '', 'name': '', 'surname2': '',
                'birthday': '', 'job_title': ''}
        employee = select(
            self.employee_table
            ).where(
            self.employee_table.c.uuid == uuid
            )

        result = self.conn.execute(employee).first()

        job_title = select(
            self.app_jobtitle.c.name
            ).where(
            self.app_jobtitle.c.id == result[5]
            )
        result2 = self.conn.execute(job_title).first()

        dict['surname'] = result[2]
        dict['name'] = result[1]
        dict['surname2'] = result[6]
        dict['birthday'] = result[3]
        dict['job_title'] = result2[0]

        # print(result[10])
        if result[10] is None:
            self.add_user_telegram_id_to_db(
                user_id=result[0],
                telegram_user_id=telegram_user_id
                )
        self.conn.close()
        return dict
