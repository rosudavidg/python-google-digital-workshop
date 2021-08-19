#!/usr/bin/env bash

mkdir secrets &> /dev/null

read -p "Enter database name: " database_db
read -p "Enter user: " database_user
read -s -p "Enter password: " database_password
read -p "Enter email address: " email_address
read -s -p "Enter email password: " email_password
read -p "Enter jwt key: " auth_jwt_key

echo $database_db > secrets/database_db
echo $database_user > secrets/database_user
echo $database_password > secrets/database_password
echo $email_address > secrets/email_address
echo $email_password > secrets/email_password
echo $auth_jwt_key > secrets/auth_jwt_key
