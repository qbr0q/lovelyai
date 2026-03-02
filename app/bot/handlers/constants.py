from app.bot.states import Registration
from app.core.utils import SimpleObject as so


GENDER_ICON_MAP = {
    "M": "💙",
    "F": "💗"
}

GENDER_MAP = {
    "M": "Мужской",
    "F": "Женский"
}

INPUT_GENDER_MAP = {
    "М": "M",
    "Ж": "F"
}

GENDER_BUTTONS = ["М", "Ж", "Не указано"]


FIELDS_CONFIG = {
    "gender": so(
        text="Укажи свой пол",
        state=so(
            edit_state=Registration.edit_gender,
            create_state=Registration.create_gender,
        ),
        validate=lambda x: "Пожалуйста, выбери вариант на кнопках ниже" if x not in GENDER_BUTTONS else ""
    ),
    "name": so(
        text="Как тебя зовут?",
        state=so(
            edit_state=Registration.edit_name,
            create_state=Registration.create_name,
        ),
    ),
    "age": so(
        text="Сколько тебе лет?",
        state=so(
            edit_state=Registration.edit_age,
            create_state=Registration.create_age,
        ),
    ),
    "city": so(
        text="Где ты живешь?",
        state=so(
            edit_state=Registration.edit_city,
            create_state=Registration.create_city,
        ),
    ),
    "bio": so(
        text="Расскажи о себе",
        state=so(
            edit_state=Registration.edit_bio,
            create_state=Registration.create_bio,
        ),
    )
}

CREATION_ORDER = ["name", "gender", "age", "city", "bio"]

CREATION_STATE = [Registration.create_name, Registration.create_gender, Registration.create_age,
                  Registration.create_city, Registration.create_bio]
