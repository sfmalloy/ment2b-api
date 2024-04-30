#!/bin/bash

# Path to the temporary cookie file
cookie_file=$(mktemp)

# Call localhost:8080/login and save cookies to a file
curl -s -X GET \
  -H "uid: aaaa" \
  --cookie-jar "$cookie_file" \
  http://localhost:8080/login > /dev/null

# Parse the "ment2b_session" cookie value from the cookie file
session_cookie=$(awk '/ment2b_session/{print $NF}' "$cookie_file")

# Call localhost:8080/user with the "ment2b_session" cookie
curl -X GET \
  -H "Cookie: ment2b_session=$session_cookie" \
  http://localhost:8080/user

# Call localhost:8080/match with the same "ment2b_session" cookie
curl -X GET \
  -H "Cookie: ment2b_session=$session_cookie" \
  http://localhost:8080/match

# Remove the temporary cookie file
rm "$cookie_file"
