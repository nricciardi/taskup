# Pi Project
This is a university project.

**TODO**

## Get Started
**TODO**

# Documentation for Users
**TODO**


# Documentation for Developers
This is a base and simple documentation to illustrate this project.
To watch a full

## How to generate Sphinx documentation?
To run Sphinx doc:
1. Go in /doc directory
2. Run `sphinx-apidoc -o source/ ..` or `sphinx-apidoc -o source/ ../lib` to refresh only lib packages
3. Run `make html`
4. Go in `doc/build/html`

## Keyword
- **Base Directory:** _this_ project directory path
- **Project Directory:** the managed project path
- **Work Directory:** the work directory inside _project directory_

## App
### Eel and WebSocket
This project uses the [Eel library](https://github.com/python-eel/Eel) to send data between client (frontend) and server
(Python). Eel is a little Python library for making simple Electron-like offline HTML/JS GUI apps, with full access to Python capabilities and libraries.

Eel hosts a local webserver, then lets you annotate functions in Python so that they can be called from Javascript, and vice versa.

The App class in `app.py` implements `__init__` and `start` methods to load and start Eel. It takes the configuration files
from `settings.json` using the Settings class.
In `__init__` it uses the Exposer class to expose all methods for frontend.

#### Exposer
Exposer is the class which provides to expose methods using the "expose" methods of Eel. In particular, 
Eel provides two methods to expose a function (other than `@expose` decorator):
- `expose()` which exposes method (and function) as it is
- `_expose()` which expose method (and function) with an _alias_, it is so important because the entities managers have
the same methods name to create, read, update and so on entities, so each manager has the own prefix (e.i. UsersManager has "user_")
see [here](#how-to-set-alias-in-eel).

#### Webserver
The Eel's webserver implements a [**Web Socket**](https://en.wikipedia.org/wiki/WebSocket) to send data.
It is hosted on 8000 port (see `app.py`), so in develop mode the frontend have to host on different port, for example, 4200 port.
See [here](#how-to-run-angular-and-eel-together-in-develop-mode).

Since the webserver is implemented with web socket there can only be **one** data transfer at a time.



## Database and Entities
### DBManager
**DBManager** is the class used to provide connect with the database.
Moreover, it allows to create the base structure of the database: tables and relations between them.

### BEM
**BEM** is the base class for the _entities models_, it implements some common and useful methods.

### EntitiesManager
**EntitiesManager** is the base class for the _entities managers_, that are classes that manage entities (find, create, delete, ...).

## TO-DO
### Frontend
- [ ] Why some js file aren't tracked?
- [x] Internalization
- [ ] Set link in Documentation and Contribute in menu
- [ ] 404 and 500 pages

### Python
- [ ] (!) Implement try-except in exposed methods
- [x] Prevent Eel closing on error -> caused by shutdown_delay (Eel .start)
- [x] Create common method to add a table and insert base values
- [ ] Migrate from __insert_base to seeder
- [ ] Improve QueryBuilder (join, subquery, group by, order by)
- [ ] Crypt password of users
- [ ] Improve common methods of entity (py) as in typescript
  -  [x] all_as_model
  -  [ ] append relation on bem and not in another foreach

### DB
- [x] Unique on user's username? Add name and surname?
- [x] DB schema
- [ ] deadline from date to datetime?

### Generals
- [ ] Remove .vs and .idea directory from Git


## Help the Open Source Community

### How to run Angular and Eel together in develop mode?
1. Run Angular frontend with `ng serve` using 4200 port (the default port)
2. Set Eel using whatever directory, but using `{ 'port': 4200 }` as start file!
3. Set another port (i.e. 8000) in Eel `.start(...)`
4. Run Eel python script

### How to set alias in Eel?
```python
import eel


class MyClass:
   def my_method(self):
      pass
      
my_class = MyClass()
eel._expose("other_name", my_class.my_method)
```

Watch out "**_**" in `_expose(...)`, it is different from `expose(...)`