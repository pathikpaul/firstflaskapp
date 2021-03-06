# My First Flask App 

## Tested on Virtual box using Vagrant
  bento/centos-7.2  (came with Python 2.7.5 installed)
  See more details in Vagrantfile

## Installed Flask using below commands
```bash
  sudo yum install python-virtualenv
  cd ~
  python2 -m virtualenv venv
  cd ~
  . ~/venv/bin/activate
  pip install Flask==1.1.2
  mkdir firstflaskapp
  cd firstflaskapp
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
## What does this application do
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
gunicorn application:application 
gunicorn -D application:application  # use -D for Deamon Mode
gunicorn --chdir /home/hadoop/firstflaskapp -b:5000 application:application   ## if you need to run from a remote location on a different port
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

## For Deploying in AWS using a Launch Configuration In Development Mode
```bash
#!/bin/bash
yum install git -y
git clone https://github.com/pathikpaul/firstflaskapp.git
easy_install pip
pip install -r firstflaskapp/requirements.txt
python firstflaskapp/application.py 80
```
## For Deploying in AWS using a Launch Configuration with Gunicorn and Nginx
```bash
#!/bin/bash
yum install git -y
git clone https://github.com/pathikpaul/firstflaskapp.git
easy_install pip
pip install -r firstflaskapp/requirements.txt
#GUNICORN
pip install gunicorn
gunicorn -D --chdir firstflaskapp -b:5000  application:application
#NGINX
amazon-linux-extras install nginx1.12 -y
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf_saved_pathik
sh -c "sed 's/default_server//' /etc/nginx/nginx.conf_saved_pathik > /etc/nginx/nginx.conf"
cp firstflaskapp/firstflaskapp_nginx.conf /etc/nginx/conf.d/.
systemctl start nginx
systemctl enable nginx
systemctl status nginx
```
## Tested this with S3 (instead of files on local disk)
**Pre Requisites**
aws cli needs to be installed on your machine
aws cli needs to be configured on your machine
The sample code is in application.py_works_with_S3
```bash
## Inital Setup 
cd firstflaskapp
# The bucket needs to be created 
aws s3 mb s3://pathik2020
# The initial DB File needs to be uploaded to S3 Bucket
aws s3 cp notes_db.json s3://pathik2020/
aws s3 ls s3://pathik2020/notes_db.json  ## Expect Output notes_db.json
##
mv application.py               application.py_save
mv application.py_works_with_S3 application.py
## Finally Restore files
mv application.py        application.py_works_with_S3
mv application.py_save   application.py 

```
## Tested this with AWS Lambda
lambda_read_notes.py
 - Create Lambda Funciton 
 - ReadNotes  (Python 2.7)
 - Create a new role from AWS policy templates
 - lambdareadnotes
 - Attach AmazonS3FullAccess (using IAM)
 - Lambda - Basic Settings - Edit - 15 Seconds

lambda_write_notes.py
 - WriteNotes (Python 2.7)
 - Create a new role from AWS policy templates
 - lambdawritenotes
 - Attach AmazonS3FullAccess (using IAM)
 - Lambda - Basic Settings - Edit - 15 Seconds
 - Test using the below event
```bash
{ "list_of_notes": [ { "topic": "Topic1", "comment": "Test1 Uploaded" },
                     { "topic": "Topic2", "comment": "Test2 Uploaded" } ]
}
```
 - validate that you can Read the Event after writing to it

Now that we have the Lambda Functions we need be able to connect it with the API Gateway

API Gateway
- New Rest API ApiName = NewNote
- CreateMethod = GET
- Use Lambda Proxy integration = NotChecked
- LambdaFuntion = ReadNotes
- Test the function using "Test" button 
- Validate the results
- Deploy to New Stage "dev"
- Enable Throttling 1 request per sec 
- Hit the URL using a Browser and validate that function is working
- URL will be something like https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/dev
- CreateMethod = POST
- Use Lambda Proxy integration = NotChecked
- LambdaFuntion = WriteNotes
- Test the function using "Test" button 
```bash
{ "list_of_notes": [ { "topic": "Topic3", "comment": "Test3 Uploaded via API" },
                     { "topic": "Topic4", "comment": "Test4 Uploaded via API" } ]
}
```
- Validate the results
- Deploy to New Stage "dev"
- Enable Throttling 1 request per sec 
- Hit the URL and validate that the data was uploaded into S3 via Test Method

We can store the URL in the API Parmeter key so that we do not have to store it in GITHUM
Parameter Store
- AWS Systems Manager > Parameter Store > Create parameter
- Name=APIInvokeUrl 
- Standard, SecureString, Save the URL in the Value Field
- Run the below command on the terminal to validate that you can get to the Parmeter Store from your local machine
```bash
aws ssm get-parameter --name APIInvokeUrl  --with-decryption
```

To test the code
```bash
##
mv application.py                                        application.py_save
mv application.py_works_with_unauthenticated_lamba_api   application.py
## Finally Restore files
mv application.py        application.py_works_with_unauthenticated_lamba_api  
mv application.py_save   application.py 
```

Securing the API using Usage Plans and API Keys
- API Gateway -> NewNote(ApiName) -> GET  -> Method Request -> API Key Required = true
- API Gateway -> NewNote(ApiName) -> POST -> Method Request -> API Key Required = true
- Actions -> Deploy API -> dev -> Save
- API Gateway -> Usage Plans -> xxxxxxxxxxxUsagePlan -> Next -> Add API Stage -> NewNote(ApiName) -> dev (stage) -> ClickTheCheckMark -> Next -> Create API Key and Add to Usage Plan
- Store the APIKey in the Parameter Store
- AWS Systems Manager > Parameter Store > Create parameter -> APIKey
- Validate that you can extract the APIKey from your machine
- Validate that you get Forbidden when you try to readh your API URL without the key
- Validate using Curl that you can reach the API when you pass the key to CURL
```bash
$ aws ssm get-parameter --name APIKey --with-decryption
$
$ curl https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/dev
{"message":"Forbidden"}
$ 
$ curl https://xxxxxxxxxx.execute-api.us-west-2.amazonaws.com/dev -H "x-api-key:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
{"body": [{"topic": "Topic3", "comment": "Test3 Uploaded via API"}, {"topic": "Topic2", "comment": "Added via Browser"}], "statusCode": 200}
$
```

Simple Python Code to call the API 

```bash
import requests, json
import logging
logging.basicConfig(level=logging.DEBUG)
url="https://XXXXXXXXXX.execute-api.us-west-2.amazonaws.com/dev"
headers = {'x-api-key': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'}
r=requests.request("GET",url,verify=False,headers=headers)
print('\nRESPONSE++++++++++++++++++++++++++++++++++++')
print('Response code: %d\n' % r.status_code)
print("Type: ",type(r.text))
print(r.text)
```

To test the code
```bash
##
mv application.py                                        application.py_save
mv application.py_works_with_lamba_api_with_apikeys      application.py
## Finally Restore files
mv application.py        application.py_works_with_lamba_api_with_apikeys
mv application.py_save   application.py 
```


