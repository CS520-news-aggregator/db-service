#!/bin/bash

curl -X 'POST' \
'http://127.0.0.1:8000/user/register' \
-H 'accept: application/json' \
-H 'Content-Type: application/json' \
-d '{
          "email_address": "john.doe@gmail.com",
          "password": "passwordThis123",
          "first_name": "John",
          "last_name": "Doe"
}'

export TOKEN=$(curl -X 'POST' \
    'http://127.0.0.1:8000/user/login' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
          "email_address": "john.doe@gmail.com",
          "password": "passwordThis123"
}' | jq -r .token)

curl -X 'GET' -H "Authorization: Bearer $TOKEN" \
'http://localhost:8000/user/view'