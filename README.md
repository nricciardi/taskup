# Pi Project
This is a university project.

**TODO**

## Get Started
**TODO**

## Documentaion
### How to generate Sphinx documentation?
To run Sphinx doc:
1. Go in /doc directory
2. Run `sphinx-apidoc -o source/ ..` or `sphinx-apidoc -o source/ ../lib` to refresh only lib packages
3. Run `make html`
4. Go in `doc/build/html`

### Keyword
- **Base Directory:** _this_ project directory path
- **Project Directory:** the managed project path
- **Work Directory:** the work directory inside _project directory_

## TO-DO
- [ ] Why some js file aren't tracked?
- [ ] Remove .vs and .idea


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