# freeapi-autotests

Pet проект тестирования API - https://api.freeapi.app

Чтобы состояние базы данных сервера freeapi сохранялось, необходимо поднять его локально.

Для этого запускаем docker и в терминале выполняем команды:

    - git clone https://github.com/hiteshchoudhary/apihub.git
    - cd apihub
    - cp .env.sample .env (выполняется один раз при первом запуске)
    - docker-compose up --build
