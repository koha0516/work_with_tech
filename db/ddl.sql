CREATE TABLE departments
(
    department_id   int not null unique,
    name varchar(32) not null,
    primary key (department_id)
);
CREATE TABLE employees
(
    employee_id     int not null,
    department_id   int not null,
    name            varchar(64) not null,
    birth           varchar(32) not null,
    gender          varchar(64) not null,
    mail            varchar(64) not null,
    tel             varchar(64) not null,
    post_code       varchar(64) not null,
    address         varchar(64) not null,
    salt            varchar(20) not null,
    password        varchar(64) not null,
    join_at         date,
    create_at       timestamp,
    primary key (employee_id),
    unique (employee_id)
);

