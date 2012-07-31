drop table if exists comments;
create table comments (
  id integer primary key autoincrement,
  text string not null
);
