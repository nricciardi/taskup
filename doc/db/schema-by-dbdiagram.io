Table role {    // all not null
  id integer [primary key]
  name varchar  // unique
  permission_create integer
  permission_read_all integer
  permission_move_backward integer
  permission_move_forward integer
  permission_edit integer
  permission_change_role integer
  permission_change_assignment integer
}


Table user {
  id integer [primary key]
  username varchar  // unique
  email varchar   // unique
  password varchar

  role_id integer
}

Ref: user.role_id > role.id
