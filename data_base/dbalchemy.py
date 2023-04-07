from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from aiogram.types import CallbackQuery

from settings import config
from data_base.dbcore import Base


class DBManager:
    def __init__(self):
        self.engine = create_engine(
            config.DATABASE_URL,
            echo=False  # будет показывать SQL запросы
        )
        _session = sessionmaker(self.engine)
        self.session = _session()
        # Base.metadata.drop_all(self.engine)
        # Base.metadata.create_all(self.engine)

    def get_user(self, uuid: str):
        """
        Возвращает пользователя по его uuid
        """
        result = self.session.query(User).filter_by(
            user_telegram_id=user_telegram_id
            ).one_or_none()
        return result

    def get_user_subscribe(self, user_telegram_id: int):
        """
        Возвращает подписки пользователя
        """
        user = self.get_user(user_telegram_id)
        return [theme for theme in user.theme]

    def get_all_themes(self):
        """
        Возвращает все темы
        """
        result = self.session.query(Themes).limit(5).all()
        if not result:
            self.init_all_themes()  # вызываем инициализаю тем
            result = self.session.query(Themes).limit(5).all()
        return result

    def init_all_themes(self):
        """
        получаем все темы с хабра и записываем в БД
        """
        print('parsing themes...')
        all_themes = get_habr_themes()
        for theme in all_themes:
            obj = Themes(title=theme.get('title'),
                         url=theme.get('url'))
            self.session.add(obj)
        self.session.commit()

    def get_theme(self, theme_id: int):
        """
        Возвращает тему по id
        """
        result = self.session.query(Themes).filter_by(
            id=theme_id).one_or_none()
        return result

    async def add_theme_to_my_subscribe(self,
                                        callback: CallbackQuery,
                                        callback_data: NumbersCallbackFactory):
        """
        Добавляет id темы в подписку
        """
        user = self.get_user(callback.from_user.id)
        theme = self.get_theme(callback_data.id)
        if not user.theme:
            user.theme.append(theme)
            self.session.add(user)
            self.session.commit()
            await callback.message.answer(
                f'Вы подписались на {callback_data.title}'
                )
        else:
            for theme in user.theme:
                if theme.id == callback_data.id:
                    await callback.message.answer(
                        f'Вы уже подписаны на {callback_data.title}'
                        )
                    return None

            theme = self.session.query(Themes).filter_by(
                id=callback_data.id
            ).one()
            user.theme.append(theme)
            self.session.add(user)
            self.session.commit()
            await callback.message.answer(
                f'Вы подписались на {callback_data.title}'
                )

    def delete_theme_to_my_subscribe(self, id_theme: int,
                                     user_telegram_id: int):
        """
        Удаляет id темы из подписки
        """
        user = self.get_user(user_telegram_id)
        for index, theme in enumerate(user.theme):
            if theme.id == id_theme:
                del user.theme[index]
                self.session.add(user)
                self.session.commit()
                return None

    def close(self):
        self.session.close()
