#!/usr/bin/env sh

# abort on errors
set -e

# git pull
git pull

cd frontend

# run frontend
npm run serve

cd ..
cd server

# run server
flask run --host=192.168.0.102

cd -
