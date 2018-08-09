# MySQL
这里记录一下MySQL的初级操作，高级操作在本目录下的其他文件中记录。

## 安装与连接

### MacOS
```
brew install mysql
mysql.server start
```

### Linux
##### SentOS 7
```
yum install mariadb-server mariadb
systemctl start mariadb
```
##### others
```
yum install mysql
service mysqld start
```
### 安装后的操作
```
mysqladmin --version #验证是否安装成功
mysqladmin -uroot password "new_password";
mysql -uroot -p
```
可操作`mysql`库进行用户管理

## 数据库操作
##### create 
```
mysqladmin -uroot -p create database_name #命令行创建
create database database_name #mysql客户端创建
```
##### drop
```
mysqladmin -uroot -p drop database_name #命令行创建
drop database database_name #mysql客户端创建
```
##### use
```
use databaseName
```

## 数据类型
##### 数值类型
`TINYINT` `SMALLINT` `MEDIUMINT` `INT` `INTEGER` `BIGINT` `FLOAT` `DOUBLE` `DECIMAL`
##### 日期和时间类型
`DATE` `TIME` `YEAR` `DATETIME` `TIMESTAMP`
##### 字符串类型
`CHAR` `VARCHAR` `TINYBLOB` `TINYTEXT` `BLOB` `TEXT` `MEDIUMBLOB` `MEDIUMTEXT` `LONGBLOB` `LONGTEXT` `JSON`

## 数据表操作
##### create
```
CREATE TABLE table_name(
   id INT UNSIGNED AUTO_INCREMENT,
   name VARCHAR(255) NOT NULL,
   date DATE,
   PRIMARY KEY ( id )
)ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
##### drop
```
DROP TABLE table_name ;
```
##### alter

## 数据操作
##### insert
```
INSERT INTO table_name ( field1, field2,...fieldN )
VALUES ( value1, value2,...valueN );
```
##### select
```
SELECT column_name,column_name
FROM table_name
[WHERE Clause]
[LIMIT N][ OFFSET M]
```
##### where
```
SELECT field1, field2,...fieldN FROM table_name1, table_name2...
[WHERE condition1 [AND [OR]] condition2...
```
##### update
```
UPDATE table_name SET field1=new-value1, field2=new-value2
[WHERE Clause]
```
##### delete
```
DELETE FROM table_name [WHERE Clause]
```
##### like
```
SELECT field1, field2,...fieldN 
FROM table_name
WHERE field1 LIKE condition1 [AND [OR]] filed2 = 'somevalue'
```
##### union
```
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions]
UNION [ALL | DISTINCT]
SELECT expression1, expression2, ... expression_n
FROM tables
[WHERE conditions];
```