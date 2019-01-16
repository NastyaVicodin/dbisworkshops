/*==============================================================*/
/* DBMS name:      ORACLE Version 11g                           */
/* Created on:     09.01.2019 20:09:40                          */
/*==============================================================*/

drop table check_in_user cascade constraints;

drop table vacancy cascade constraints;

/*==============================================================*/
/* Table: check_in_user                                         */
/*==============================================================*/
create table check_in_user 
(
   id_code            NUMBER(10)           not null,
   last_name          VARCHAR2(30)         not null,
   first_name         VARCHAR2(30)         not null,
   login              VARCHAR2(30)         not null,
   password           VARCHAR2(30)         not null,
   email              VARCHAR2(30)         not null,
   salary             VARCHAR2(30),
   specialization     VARCHAR2(30),
   location           VARCHAR2(30),
   sphere             VARCHAR2(30),
   constraint PK_CHECK_IN_USER primary key (id_code),
   constraint un_user_login unique (login),
   constraint un_user_email unique (email),
   constraint user_id_code_constr check(regexp_like(id_code, '^[0-9]{10}$')),
   constraint user_last_name_constr check(regexp_like(last_name, '^([A-Z][a-z]+)$')),
   constraint user_first_name_constr check(regexp_like(first_name, '^([A-Z][a-z]+)$')),
   constraint user_email_constr check(regexp_like(email, '^[0-9a-zA-Z\.]{1,18}@[a-z]{1,8}\.[a-z]{2,3}$')),
   constraint user_login_constr check(regexp_like(login, '^[0-9a-zA-Z]{5,30}$')),
   constraint user_password_constr check(regexp_like(password, '.{8,}'))
);

/*==============================================================*/
/* Table: vacancy                                               */
/*==============================================================*/
create table vacancy 
(
   id_code            NUMBER(10)           not null,
   vacancy_name       VARCHAR2(30)         not null,
   company            VARCHAR2(30)         not null,
   email              VARCHAR2(30)         not null,
   salary             VARCHAR2(30),
   location           VARCHAR2(30)         not null,
   sphere             VARCHAR2(30)         not null,
   constraint PK_VACANCY primary key (id_code)
);
