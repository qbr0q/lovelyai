from app.bot.states import Registration


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
    "gender": {
        "text": "Укажи свой пол", "state": Registration.edit_gender,
        "validate": lambda x: "Пожалуйста, выбери вариант на кнопках ниже"
        if x not in GENDER_BUTTONS else ""
    },
    "name": {"text": "Как тебя зовут?", "state": Registration.edit_name},
    "age": {"text": "Сколько тебе лет?", "state": Registration.edit_age},
    "city": {"text": "Где ты живешь?", "state": Registration.edit_city},
    "bio": {"text": "Расскажи о себе", "state": Registration.edit_bio}
}

STATE_TO_FIELD = {
    Registration.edit_gender: "gender",
    Registration.edit_name: "name",
    Registration.edit_age: "age",
    Registration.edit_city: "city",
    Registration.edit_bio: "bio"
}
