# Курсовая работа по курсу №5
## Задача - спроектировать базу данных на основе данных о работодателях полученных через API с сайта HH.ru
## Установка:
1. Склонировать репозиторий:
```
https://github.com/nikita-szr/coursework_3
```
2. Установка зависимостей: 
```
poetry install
```
3. Использование
```
Ввести ключевые слова для поиска и получить базу данных с вакансиям по заданным работодателям
```


4. Модули
```
main - Запускает проект
api_hh - скрипт для подключения по api к сайту HH.ru
utils - функции для создания бд и таблиц
DBManager - класс для взаимодействия с БД
```