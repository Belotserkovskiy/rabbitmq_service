# rabbitmq_service
Cервис, позволяющий добавлять пользователя в БД и
выдающий результат обработки запроса.

Для получения запросов сервис должен слушать очередь RabbitMQ. Для
RabbitMQ параметры host, port, vhost, exchange, queue, user, password
должны задаваться в конфиге cfg/rabbitmq.cfg.

Сервис должен общаться с уже подготовленной базой данных postgresql.
Host, port, db_name, user, password для БД должны задаваться в конфиге cfg/postgresql.cfg.

Структура базы данных:
 - id serial NOT NULL
 - name character(100) NOT NULL
 - email character(100) NOT NULL
 - location character(100) NOT NULL

Запрос на добавление пользователя будет приходить в виде словаря с
ключами:
- ‘action’: ‘add_user’
- ‘name’: ‘some_name’
- ‘email’: ‘some_email’
- ‘location’: ‘some_city’
- ‘reply_to’: {‘queue’: ‘some_queue’, ‘exchange’: ‘some_exchange’}

После получения, проверки корректности и выполнения входящего запроса,
система должна по роутинг из reply_to поля запроса выслать информацию
- При успешном выполнении: Id: id человека в таблице; error_code: 0,
error_msg: ‘’
- При ошбике: id: null, error_code: 1, error_msg: “error description”

Пользователем гарантируется, что во входящем запросе всегда есть поле reply_to с
правильной структурой. Присутствие и правильность других полей не
гарантируется.
