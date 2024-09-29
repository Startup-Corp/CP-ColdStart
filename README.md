## Ссылки

Screencast: [ссылка](https://disk.yandex.ru/d/tOuoz6p9HlZ3lw)
Сайт: [ссылка](http://87.242.86.81:3000/)

## Содержание

1. Запуск приложения на своей системе
	1. Запуск Baackend-а
	2. Запуск Frontend-а
2. Полезные файлы
## Запуск приложения на своей системе
### Запуск Backend

1. Открываем проект и переходим в папку `back`. 
2. Устанавливаем зависимости 
```
pip install -r req.txt
```
3. Далее запускаем backend часть
```
python main.py
```

### Запуск Frontend

1. Открываем корневую папку проекта
2. Для сборки проекта, в консоли прописываем
```
npm install
```
3. В файлах `js/[videoId].js` и `js/ChooseVideoPage.js`, изменяем все `url` адреса либо на `http://127.0.0.1:5005`, если серверная часть запущена локально, и `http://[server.ip]:5005`, если серверная часть запущена на выделенном сервере.
4. Запускаем проект 
```
npm start
```
5. Если автоматически не открылась страница в браузере, то переходим по ссылке  [http://localhost:3000](http://localhost:3000).

## Полезные файлы

ML исследования - [ColdStart/notebooks · Startup-Corp/ColdStart (github.com)](https://github.com/Startup-Corp/ColdStart/tree/main/notebooks)