drop table if exists books;
create table books (
  id integer primary key autoincrement,
  title text not null unique,
  author text not null,
  category text not null,
);

create table users (
	id integer primary key autoincrement,
	username text not null unique,
	email text not null,
	password text not null
);