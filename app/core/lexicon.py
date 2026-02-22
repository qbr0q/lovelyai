from types import SimpleNamespace as sn


LEXICON = sn(
    start="добро пожаловать",
    state=sn(
        waiting_import="Отлично! Теперь просто перешли мне свою анкету другого бота "
                       "и я попробую вытащить оттуда все данные."
    ),
    button=sn(
        create_profile="Создать анкету",
        import_profile="Импортировать из других ботов"
    ),
    error=sn(
        message_not_forwared="Похоже это не пересланное сообщение. Попробуй еще раз или заполни вручную.",
        message_forwared_not_from_bot="Анкета должна быть переслана от телеграм-бота"
    )
)
