# IT-проект "Образовательная платформа ООП"

<h2>Архитектура проекта:
<h4><font color="red"> /// Miro ///
https://miro.com/welcomeonboard/SkR4WjFKdGRJT0pwT1dyMG9vOEgwSWRVOFJpV0ZXWkJJYXpWZm1pMllYaVpybHgzWlJTQVVTQkYzNUVuR1dkN3wzNDU4NzY0NTg1NjQwMjA1MDE1fDI=?share_link_id=998162167732
</font>

<h2>Цели и задачи:
<h4><font color="lightblue"> /// Trello ///
https://trello.com/b/Oj3UHJCU/gigoop
</font>

<h2>Структура базы данных:
<h4><font color="pink">/// Figma ///
https://www.figma.com/file/GPE3nndbkOOPY9NNyKKXWF/gigaOOP-schema?type=whiteboard&node-id=0%3A1&t=kQiOJ1q8unnMvuZU-1
</font>

## Запуск проекта
### Запуска сервера backend
Запуск проекта осуществляется после того, как вы клонировали репозиторий себе на локальную машину. 
Для запуска backend используется сервер uvicorn
Установите виртуальную среду python - venv в корень проекта

```
python -m venv venv
```

Затем войдите в venv с помощью команды (windows):

```
venv/Scripts/activate
```

Перейдите в папку бэкенда

```
cd backend
```

Выполните установку зависимостей
```
pip install -r requirements.txt
```
Запустите сервер uvicorn

```
uvicorn main:app --reload
```


### Запуск сервера frontend
Из корня проекта перейдите в папку фронтенда
```
cd frontend
```

Установите зависимости для фронетенда
```
npm install
```

Запустите сервер фронтенда
```
npm run dev
```






