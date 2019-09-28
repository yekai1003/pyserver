#!/bin/bash 

mysql_home=~/mysql

mkdir -p $mysql_home/conf $mysql_home/logs $mysql_home/data

cd $mysql_home

docker run \
-p 3306:3306 \
--name dockermysql \
-v $PWD/conf:/etc/mysql/conf.d \
-v $PWD/logs:/logs \
-v $PWD/data:/var/lib/mysql \
-e MYSQL_ROOT_PASSWORD=root -d mysql
