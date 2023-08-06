# MyChat

Simple chat application build using django

## Quick Start

1. Add `chat` app to your `INSTALLED APPS` like this:

```
INSTALLED_APPS = [
  ...
  'chat'
]
```

2. Add it to you urls.py file like this:

```
urlpatterns = [
  path('', include('chat.urls'))
]
```

3. Run `python manage.py makemigrations` and `python manage.py migrate`.

4. Run development server and visit http://127.0.0.1:8000/chat
