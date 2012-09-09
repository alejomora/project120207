/*Init tables*/
drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  key string not null,
  value string
);

/*Insert default values*/
insert into entries(key, value) VALUES ('web_username','admin');
insert into entries(key, value) VALUES ('web_password','admin');
insert into entries(key, value) VALUES ('web_layout_title','Проект 120207');
insert into entries(key, value) VALUES ('web_layout_h1','Проект 120207');
