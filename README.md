# Pi Project
This is a university project.

**TODO**

## Get Started
**TODO**

# Documentation
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

### How to run Angular and Eel together in _**debug mode**_?
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