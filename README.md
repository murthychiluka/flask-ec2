 Install Dependencies on EC2


sudo yum update -y

sudo yum install -y python3 python3-pip git mariadb105-server

pip3 install flask  pymysql
************************************
Create the Database Table
Connect to RDS from EC2 to confirm connectivity and create a table:
mysql -h <RDS-ENDPOINT> -u <your-username> -p
Once connected:
CREATE DATABASE myapp;
USE myapp;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    done BOOLEAN DEFAULT FALSE
);

EXIT;
***********************************************

Create a folder and file on EC2:

mkdir ~/flaskapp && cd ~/flaskapp
vi app.py  ----paste app.py content  and run ---   python3 app.py
********************
if you close your SSH session, Flask stops. To keep it running permanently, use a process manager. 

sudo pip3 install gunicorn
nohup gunicorn -w 2 -b 0.0.0.0:5000 app:app &
******************************  
# flask-ec2
you can test the CRUD endpoints from your browser's address bar or terminal:
# Create a task
curl -X POST http://3.236.198.195:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "My first AWS task"}'

# Read all tasks
curl http://3.236.198.195:5000/tasks

# Update task (replace 1 with actual id)
curl -X PUT http://3.236.198.195:5000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"done": true}'


  What's running:

Flask app on EC2 (3.236.198.195:5000)
Gunicorn (2 workers) running in background
MySQL RDS connected and working
Full CRUD API (Create, Read, Update, Delete)

# Delete task
curl -X DELETE http://3.236.198.195:5000/tasks/1
*********************************************88

Gunicorn is running with nohup, you don't need to run python3 app.py anymore.
Here's the simple difference:
Command           Use case                          Stays alive after SSH closes?        Survives reboot?     
python3 app.py    Quick testing only              ❌                                       No❌    
Nonohup gunicorn ... &Proper background run        ✅ Yes                                  ❌ No
systemd service     Production grade                ✅ Yes                                ✅ Yes
