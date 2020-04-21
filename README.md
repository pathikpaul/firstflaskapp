# My Firs Flask App 

## Tested on Virtual box using Vagrant
  bento/centos-7.2  (came with Python 2.7.5 installed)
  See more details in Vagrantfile

## Installed Flask using below commands
  sudo yum install python-virtualenv
  mkdir myproject
  cd myproject
  python2 -m virtualenv venv
  cd /home/hadoop/myproject
  . venv/bin/activate
  pip install Flask==1.1.2
## Ran using the below
  export  FLASK_ENV=development
  export  FLASK_APP=myfirstapp
  since the machine does not have a browser i had to use below flask command instead of "flask run"
  flask run --host=192.168.77.10
## Tested at below URL
  http://192.168.77.10:5000/
  http://192.168.77.10:5000/info
