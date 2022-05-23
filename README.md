# Кэширующий DNS сервер
_____
# Описание:
Клиент отправляет запрос серверу с помощью утилиты nslookup. Сервер получает запрос и проверяет кэш на наличие нужно ответа.    
Если ответ есть в кэше, сервер отправляет его. Если ответа в кэше не оказалось, сервер отправляет запрос на старший DNS сервер,
после чего парсит полученный пакет, заносит данные в кэш и отправляет ответ клиенту.    
Сервер регулярно просматривает кэш и удаляет из него просроченные записи.
_____
# Запуск
Сервер запускается командой
```
python dns.py
```
В консоль вводятся запросы, например
```
nslookup urfu.ru 127.0.0.1    
nslookup -type=A urfu.ru 127.0.0.1    
nslookup -type=NS urfu.ru 127.0.0.1   
```
# Примеры запросов
## №1
```
nslookup urfu.ru 127.0.0.1
```
![Image alt](https://github.com/anya-otman/DNS/blob/main/images/example1.png)
## №2
```
nslookup -type=A urfu.ru 127.0.0.1
```
![Image alt](https://github.com/anya-otman/DNS/blob/main/images/example2.png)
## №3
```
nslookup -type=NS urfu.ru 127.0.0.1 (ответ от сервера)
```
![Image alt](https://github.com/anya-otman/DNS/blob/main/images/example3.png)
![Image alt](https://github.com/anya-otman/DNS/blob/main/images/example3_1.png)
```
nslookup -type=NS urfu.ru 127.0.0.1 (ответ из кэша)
```
![Image alt](https://github.com/anya-otman/DNS/blob/main/images/example3.png)
![Image alt](https://github.com/anya-otman/DNS/blob/main/images/example3_2.png)
