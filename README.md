# fastApi
creating a fast API REST API application

py -m venv venv
cd venv
OR 
venv\Scripts\activate.bat

uvicorn main:app --reload
pip install fastapi[all]

git add .
git commit m "commit message"
git push origin main

https://www.psycopg.org/

<!-- 
Updating all installed packages on ubuntu machine 
sudo apt update && sudo apt upgrade -y  
-->

<!-- 
installing Python 3.10, pip and venv on ubuntu

sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install Python3.10
python3.10 --version 3.10.6
suod install python3.pip
sudo pip3 install virtualenv
sudo apt install postgresql postgresql-contrib -y
 -->
<!-- 
configure postgress user password for postgres user on ubuntu

sudo -u postgres psql
\password postgres
 -->
