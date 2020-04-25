# My First Flask App 

## Tested on Virtual box using Vagrant
  bento/centos-7.2  (came with Python 2.7.5 installed)
  See more details in Vagrantfile

## Installed Flask using below commands
```bash
  sudo yum install python-virtualenv
  mkdir myproject
  cd myproject
  python2 -m virtualenv venv
  cd /home/hadoop/myproject
  . venv/bin/activate
  pip install Flask==1.1.2
```
## Ran using the below
```bash
  export  FLASK_ENV=development
  export  FLASK_APP=application  ##
  flask run --host=192.168.77.10 ## since the machine does not have a browser I had to use below flask command instead of "flask run"
```
## Tested at below URL
```bash
  http://192.168.77.10:5000/
  http://192.168.77.10:5000/info
```
## What does this app do
```bash
   - /info
     - Displays Host information like IP Address
     - Current Time
     - A Counter
   - Displays, Adds and deletes Notes
   - Notes are kept in a local static files
   - This version is NOT suitable for scaling
```
## For Deploying the App 
- https://flask.palletsprojects.com/en/1.1.x/deploying/
- https://gunicorn.org/#deployment
```bash
pip install gunicorn
gunicorn application:app # gunicorn -D application:app  # use -D for Deamon Mode
gunicorn stop
sudo yum -y install epel-release
sudo yum -y install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
sudo cp -fp   /etc/nginx/nginx.conf /etc/nginx/nginx.conf_backup
sudo vi   /etc/nginx/nginx.conf ## update as per https://gunicorn.org/#deployment
sudo systemctl restart nginx
sudo systemctl status nginx
```
## For Deploying in AWS I needed to make a few changes
* Created a "requirements.txt" file 
    * https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/python-development-environment.html
```bash
pip freeze >requirements.txt
```
* Created a Zip file to be used by Elastic Beanstalk 
```bash
zip myapp.zip application.py templates/* static/* README.md  requirements.txt notes_db.json
git archive -v -o myapp.zip --format=zip HEAD
```
