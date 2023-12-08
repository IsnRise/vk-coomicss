# Публикация комиксов
Этот проект создан для того, чтобы Вы могли выкладывать случайный комикс xkcd в свою группу VK с подписью к этим комиксам от самого же автора.

## Как установить
Вам понадобится несколько ключей для этого проекта, например:
1. Личный ключ

    Чтобы получить Ваш личный ключ, ознакомьтесь с [этим сайтом](https://dev.vk.com/ru/api/access-token/implicit-flow-user?ref=old_portal)

    Вот пример такого ключа: `533bacf01e1165b57531ad114461ae8736d6506a3`

    Когда Вы его получите, положите его в `.env`, в формате:
    ```
    VK_ACCESS_TOKEN=(ВАШ КЛЮЧ)
    ```

3. Group_id (Идентификатор Вашей группы)

    Узнать group_id Вашей группы можно [здесь](https://regvk.com/id/)

    Вот пример такого идентификатора: `724676122`

    Когда вы его получите, положите его в `.env`, в формате:
    ```
    VK_GROUP_ID = (ВАШ ИДЕНТИФИКАТОР)
    ```


Python3 должен быть уже установлен. Затем используйте `pip` (или `pip3`, есть есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

И вот вы уже можете запустить этот проект!


## Пример запуска скрипта
Чтобы запустить скрипт и опубликовать случайный комикс в Вашу группу, вот пример запуска:
```
python vk_comics.py
```

## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
