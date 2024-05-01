#!/bin/bash

# Call localhost:8080/login and capture the verbose output
login_response=$(curl -s -X GET \
  -H "uid: cccc" \
  -D - \
  http://localhost:8080/login)

# Parse the "ment2b_session" cookie value from the verbose output
session_cookie=$(echo "$login_response" | awk -F'set-cookie: ' 'NF > 1 {split($2, cookie, ";"); print cookie[1]}')

#echo "session cookie"
#echo $session_cookie

# Call localhost:8080/user with the "ment2b_session" cookie
# curl -s -X GET \
#   -H "Cookie: $session_cookie" \
#   http://localhost:8080/user

# Call localhost:8080/match with the same "ment2b_session" cookie
curl -s -X GET \
  -H "Cookie: $session_cookie" \
  http://localhost:8080/match
