Table role {    // all not null
  id integer [pk]
  name varchar(100) unique
  permission_create integer
  permission_read_all integer
  permission_move_backward integer
  permission_move_forward integer
  permission_edit_own integer
  permission_edit_all integer
  permission_change_role integer
  permission_change_assignment integer
  permission_delete_own integer
  permission_delete_all integer
}

Table user {
  id integer [pk]
  username varchar(256) unique
  name varcharvarchar(256)
  surname varcharvarchar(256)
  email varchar(256) unique
  password varchar(256)
  avatar_hex_color varchar(6)
  last_visit_at datetime

  role_id integer
}

Ref: user.role_id > role.id

Table task {
  id integer [pk]
  name varchar(150)
  description varchar(1000)
  deadline datetime
  priority integer
  created_at datetime
  updated_at datetime

  author_id integer
  task_status_id integer
}

Ref: task.author_id > user.id
Ref: task.task_status_id > task_status.id

Table task_assignment {
  id integer [pk]
  last_watched_at datetime

  user_id integer
  task_id integer
}

Ref: task_assignment.user_id > user.id
Ref: task_assignment.task_id > task.id

Table task_label {
  id integer [pk]
  name varchar(500) unique
  description varchar(1000)
  hex_color varchar(6)
}

Table task_task_label_pivot {
  id integer [pk]

  task_id integer
  task_label_id integer
}

Ref: task_task_label_pivot.task_id > task.id
Ref: task_task_label_pivot.task_label_id > task_label.id


Table task_status {
  id integer [pk]
  name varchar(150) unique
  description varchar(1000)
  default_next_task_status_id integer
}

Ref: task_status.default_next_task_status_id > task_status.id

Table todo_item {
  id integer [pk]
  description varchar(1000)
  deadline datetime
  created_at datetime
  updated_at datetime
  done integer

  author_id integer
  task_id integer
}

Ref: todo_item.author_id > user.id
Ref: todo_item.task_id > task.id
