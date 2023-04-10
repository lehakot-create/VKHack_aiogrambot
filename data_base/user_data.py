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
        self.app_jobtitle = Table('app_jobtitle',
                                  self.metadata,
                                    # autoload=True,
                                    autoload_with=self.engine
                                  )

        # создаем соединение с БД
        self.conn = self.engine.connect()

    def get_user_data(self, uuid: str) -> dict:
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

        self.conn.close()
        dict['surname'] = result[2]
        dict['name'] = result[1]
        dict['surname2'] = result[6]
        dict['birthday'] = result[3]
        dict['job_title'] = result2[0]

        return dict
