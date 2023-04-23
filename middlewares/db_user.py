from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, db_user):
        super().__init__()
        self.db_user = db_user

    async def pre_process(self, obj, data, *args):
        data['db_user'] = self.db_user
