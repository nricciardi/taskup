import os
from lib.db.query import SelectQueryBuilder
from lib.db.entity.user import UsersManager
from lib.app.project import ProjectManager
from lib.db.entity.task import TasksManager
from lib.db.component import WhereCondition
from lib.app.service.auth import AuthService
from random import randint
import sqlite3

if __name__ == '__main__':

    db_path = "/home/ncla/Desktop/project/project-pi/code/fakeproject/work/database.db"

    # os.remove(db_path)
    pm = ProjectManager()

    users_manager = UsersManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work", verbose=True)
    tasks_manager = TasksManager("database.db", "/home/ncla/Desktop/project/project-pi/code/fakeproject/work", verbose=True)

    # auth = AuthService(users_manager, "/home/ncla/Desktop/project/project-pi/code/fakeproject/work/fakevault.json", True)
    # auth.login("n1@r.com", "asdf123", False)

    # query = SelectQueryBuilder.from_table("user").enable_binding().select().where("username", "=", "franco1")
    # print(query.to_sql())
    # print(query.data_bound)

    #
    users = users_manager.all_as_dict(with_relations=True)
    print(users)

    # users = users_manager.all_as_model(with_relations=True)
    # print(users)

    #
    tasks = tasks_manager.find(1, with_relations=True, safe=False)
    print(tasks)

    # users_manager.where_as_model(WhereCondition("username", "=", "franco2"))

    # offset = 0
    # count = 3
    #
    # for n in range(count * offset, count * offset + count):
    #     user = users_manager.create_from_dict({"username": f"franco{n}",
    #                                 "email": f"n{n}@r.com",
    #                                 "password": "asdf123",
    #                                 "role_id": 1})
    #
    #     print(user)
    #
    #     task = tasks_manager.create_from_dict({
    #         "name": f"prova task{n}",
    #         "description": f"descrizione di prova{n}",
    #         "author_id": user.id,
    #         "task_status_id": randint(1, 8)
    #     })


    # def dict_factory(cursor, row):
    #
    #     print(type(row))
    #
    #     fields = [column[0] for column in cursor.description]
    #     return {key: value for key, value in zip(fields, row)}
    #
    # con = sqlite3.connect(db_path)
    # con.row_factory = dict_factory
    # cur = con.cursor()
    #
    # res = cur.execute("Select * From user where id = 1")
    #
    # res = res.fetchall()
    #
    #
    # print(res)




