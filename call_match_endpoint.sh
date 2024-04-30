#!/bin/bash

# MODIFY UID below to change user to match on

# Call localhost:8080/login and parse sessionToken
session_token=$(curl -s -X GET \
  -H "uid: aaaa" \
  http://localhost:8080/login | jq -r '.sessionToken')

# Call localhost:8080/match with sessionToken
curl -X POST \
  -H "Authorization: Bearer $session_token" \
  http://localhost:8080/match