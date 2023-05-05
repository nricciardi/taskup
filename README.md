# Pi Project
This is a university project for teaching object-oriented programming at UniMoRe university (a.y. 2022/2023).


**TODO**

## Get Started

### Dependencies
To run this project are required the followings dependencies:
- [Python 3.10+](https://www.python.org/downloads/)
- [Eel](https://pypi.org/project/Eel/) (Python module to create frontend)
- [Colorama](https://pypi.org/project/colorama/) (Python module for Logger)
- [Chromium](https://www.chromium.org/) based software (as Google Chrome or Firefox)

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

![structure of the project](./doc/img/dev-doc/structure-diagram.jpg)

### Eel and WebSocket
This project uses the [Eel library](https://github.com/python-eel/Eel) to send data between client (frontend) and server
(Python). Eel is a little Python library for making simple Electron-like offline HTML/JS GUI apps, with full access to Python capabilities and libraries.

Eel hosts a local webserver, then lets you annotate functions in Python so that they can be called from Javascript, and vice versa.

![websocket schema](./doc/img/dev-doc/websocket-schema1.png)

The App class in `app.py` implements `__init__` and `start` methods to load and start Eel. It takes the configuration files
from `settings.json` using the Settings class.
In `__init__` it uses the Exposer class to expose all methods for frontend.

#### Exposer
Exposer is the class which provides to expose methods using the "expose" methods of Eel. In particular, 
Eel provides two methods to expose a function (other than `@expose` decorator):
- `expose()` which exposes method (and function) as it is
- `_expose()` which is a _protected_ method of Eel library and expose method (and function) with an _alias_, it is so important because the entities managers have
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

### User, Task, TaskLabel and so on Managers
The entities (**User, Task, TaskLabel, ...**) are the classes used to manage the single entity of database.
Each of them has the base shared methods and some specific methods. For example, _TaskManager_ and _TaskLabelManager_ have `add_label` method to add a label on specific task.

### QueryBuilder
**QueryBuilder** is a custom _query builder_ based on Python `sqlite3` that implements the common utilities to build a query with Python code instead of SQL.
It supports binding with specific method as `enable_binding`.

## Frontend
The frontend of this application uses the _Angular framework_.
Angular is a TypeScript-based, free and open-source web application framework led by the Angular Team at Google and by a community of individuals and corporations.
The frontend is structured in:
- **page** contains final pages as _login page_ or _home page_
- **widget** contains simple widgets shared between pages as _user avatar_
- **service** contains the _services_ that are used to implements shared methods and communication with backend
- **model** contains a list of interface for objects that also represents entities data to show
- **directive** contains custom Angular directives

### Services
The services in Angular are used to manage connections with backend and provide some other functionality to app.
To communicate with Eel backend was implemented `EelService` which uses a global declared variable `eel` to provide the main class method `call` to call Python exposed methods.

### EntityApiService
The `EntityApiService` is a service which is used to share common methods between entity services.
It uses a _generic type_ which represents the specif _entity model_, so it can be used in some methods.
Each method returns a _Promise of Observable_, the observable is connected with websocket of backend.
To call the specific method of entity services, this class uses _readonly abstract variable_, each child service override them. 

For example the `find` method, which returns data of an entity searched by its id:

```typescript
export abstract class EntityApiService<T> {

  readonly abstract ALL: string;

  constructor(public eelService: EelService) { }

  public async find(id: number): Promise<Observable<T>> {

    return this.eelService.call(this.FIND, id);
  }
}
```

Using, for example, TaskService: 
```typescript
this.taskService.find(id).then((respose) => {
    respose.subscribe({
      next: (task: TaskModel) => {
        // ...
      }
    })
})
```

In addition, the _entities services_ as `TaskService` or `UserService` have other specific methods.
For example, `TaskService` has `addAssignment` method:

```typescript
public async addAssignment(taskId: number, userId: number): Promise<Observable<boolean>> {

    return this.eelService.call(this.ADD_ASSIGNMENT, taskId, userId);
}
```

### Task
The task visualization is made using a set of widgets:
- **TaskPreview** is the main component which is a card with all task information as title, description and so on
- **TaskPreviewList** is a component which display a list of task passed in a set of _TaskPreview_
- **TaskTodo** and **TaskTodoList** are the components used to show the list of todo-item for each task 

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

## Credits, libraries and plug in used
- Bootstrap framework
- Bootstrap icon
- Eel library
- Sqlite3 library
- Colorama library
- Mazer template