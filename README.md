# TradeCore_test
This is an example of a social network as a part of the interview for TradeCore.

## Install PostgreSQL 9.5
```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list'
wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | sudo apt-key add -
sudo apt-get update
sudo aptitude install postgresql postgresql-contrib
```
## Create Socialising user and change password
```
sudo su - postgres
createdb --owner postgres tradecore
psql
ALTER USER postgres PASSWORD ‘postgres’;
```
## Install Python 3.5
```
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.5
```
## Install virtualenv
```
sudo aptitude install python-virtualenv
mkdir project
cd project
virtualenv venv -p python3.5
source venv/bin/activate
```
## Install git, initiate repo and pull project
```
sudo apt-get install git
git init
git remote add origin https://github.com/milos-mandic/tradecore_test
git pull origin master
```
## Install dependencies
```
sudo apt-get install libxml2-dev libxslt1-dev python3.5-dev
sudo apt-get install python-psycopg2
sudo apt-get install libpq-dev
pip install -r requirements.txt
```
## Migrate database alterations
```
python manage.py migrate
```
## Run server on local host
```
python manage.py runserver
```
## Run the bot with:
```
python bot.py
```