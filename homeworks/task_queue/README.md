Очередь заданий
=========

Реализовать сервер очередей заданий с заданным протоколом взаимодействия на базе TCP сокетов

Описание
-------

Сервер это программа поднимающая socket на порту указанном как параметр запуска (по умолчаню 5555) и работающая до
нажатия Ctrl+C.

Сервер должен поддерживать операцию добавление задания в очередь, взять очередное задание и подтвердить его выполнение.
Если задание взято на обработку и не отмечено как выполненное в течение 5 минут (еще один параметр запуска), оно должно
вернуться в очередь.


Требования к сдаче задания
-------
Код должен быть разбит по методам класса (или классов) и хорошо читаться. За плохой стиль, за неуместное копирование
кусков кода, за огромные функции и пр. будет снижаться балл. Разбиение кода на осмысленые логические куски: объекты
атрибуты, методы - тоже является частью задания.

Также необходимо понять как устроены тесты и дописать хотя бы пару своих - это является частью задания.


Поддерживаемые команды
-------

Команды выполняются по одной на соединение и после ответа на команду соединение закрывается. Параллельного обслуживания
нескольких соединений не требуется, можно обслуживать соединения по одному.

Задания должны выдаваться в порядке их добавления в очередь. Выданные задания должны помечаться и не выдаваться пока не
истечет таймаут. После истечения таймаута они должны выдаваться в обработку в том же порядке, в котором были добавлены в
очередь.

После подтверждения выполнения задания его можно удалять.

Присуствует также команда сохранения - которая должна сохранить текущее состояние очереди на диск, в указанную папку.
Если сервер после выполнения этой команды остановить, он должен продолжить с очередью в том же состоянии что и сейчас (с
результатами всех успешно выполненных команд).

### Команды

* __Добавление задания__ `ADD <queue> <length> <data>`
    - Параметры
        - _queue_ - имя очереди: строка без пробелов
        - _length_ - длина содержимого задания: целое число не больше 10^6
        - _data_ - содержимое: массив байт длины _length_
    - Ответ
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов (не равная NONE)
    - Примечание
        - Если очереди с таким именем нет - то она создается
* __Получение задания__ `GET <queue>`
    - Параметры
        - _queue_ - имя очереди: строка без пробелов
    - Ответ
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов
        - _length_ - длина содержимого задания: целое число не больше 10^6
        - _data_ - содержимое: массив байт длины _length_
    - Примечание
        - Если очереди с таким именем нет или в очереди нет заданий для обработки ( например, они все выполняются), то
          возвращается строка `NONE`
* __Подтверждение выполнения__ `ACK <queue> <id>`
    - Параметры
        - _queue_ - имя очереди: строка без пробелов
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов
    - Ответ
        - `YES` - если такое задание присутствовало в очереди и было подтверждено его выполнение
        - `NO` - если такое задание отсутсвовало в очереди
* __Проверка__ `IN <queue> <id>`
    - Параметры
        - _queue_ - имя очереди: строка без пробелов
        - _id_ - уникальный идентификатор задания: строка без пробелов не длиннее 128 символов
    - Ответ
        - `YES` - если такое задание присутствует в очереди (не важно выполняется или нет)
        - `NO` - если такого задания в очереди нет
* __Сохранение__ `SAVE`
    - Ответ
        - `OK`
