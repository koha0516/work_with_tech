CREATE TABLE departments
(
    department_id   varchar(32) not null unique,
    name            varchar(32) not null,
    primary key (department_id)
);
INSERT INTO departments VALUES ('100', '営業本部'),
                            ('110', '営業部'),
                            ('111', '営業一課'),
                            ('112', '営業二課'),
                            ('113', '業務課'),
                            ('120', 'マーケティング部'),
                            ('121', 'マーケティング課'),
                            ('200', '製造本部'),
                            ('210', '製造部'),
                            ('211', '工場'),
                            ('212', '技術研究課'),
                            ('213', '調達課'),
                            ('220', '管理部'),
                            ('221', '品質管理課'),
                            ('222', '総務管理課');

CREATE TABLE roles
(
    role_id     varchar(32) not null unique,
    name        varchar(32) not null,
    primary key (role_id)
);
INSERT INTO roles VALUES ('01', '一般'),
                            ('02', '課長'),
                            ('03', '次長'),
                            ('04', '部長'),
                            ('05', '本部長'),
                            ('06', '取締役');


CREATE TABLE shift
(
    employee_id     int not null,
    working_date    date,
    working_time    time,
    primary key (employee_id, working_date)
);


CREATE TABLE holiday
(
    employee_id     int not null,
    holiday         date,
    type            varchar(32) not null,
    primary key (employee_id, holiday)
);


CREATE TABLE employees
(
    employee_id     varchar(64) not null,
    name            varchar(64) not null,
    mail            varchar(64) not null,
    department_id   varchar(64) not null,
    role            varchar(64) not null,
    salt            varchar(64) not null,
    password        varchar(64) not null,
    flg             int not null ,
    create_at       timestamp,
    primary key (employee_id),
    unique (employee_id)
);

