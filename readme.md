# READ ME

### Mongodb
Install mongodb using the msi file after getting the correct version for your os.
Use this website to find the correct install tutorial:
https://docs.mongodb.com/manual/installation/#mongodb-community-edition-installation-tutorials

Install it as a network service. 

Create the following folder for storing mongodb data
C:\data\db
Also, add the path to your mongodb installation to your system environment PATH.
I added the following directory for my installation: C:\Program Files\MongoDB\Server\4.2\bin but your installation might be different. 

I basically followed the following tutorial: https://www.geeksforgeeks.org/guide-install-mongodb-python-windows/

I did steps 5 through 8 as well but as long as you in some way have a mongodb server running on your os at the default ip this is sufficient. 

### Python
Install python somehow. I installed anaconda and used anaconda promopt with my project but you may use another method for installing python and packages.
I am using python 3.7 and am unsure if python 2.7 would be compatible with my code.

### Packages
Furthermore, make sure you have the following packages installed for python:
tkinter
pymongo
mysql.connector
pandas
numpy
logging
urllib
sqlalchemy
pymysql
pandastable

I already had some of these installed by default but had to pip install the others. Peasonally had to use the --user option to pip install.

I used anaconda prompt to pip install for every package which was simple enough but feel free to use any method.

Also used a widget called pandastable for outputting dataframe results. Had to do pip3 install pandastable personally to use it.

### Mysql
Make sure you have mysql 8.0 running as well 

### Passwords
You must control f through both my python files and change passwords where it says "#put your own root password here"

### Gui resource
I used the following tutorial for my gui but heavily modified it:
https://www.simplifiedpython.net/python-gui-login/

### Services and Run
Make sure mongodb and sql services are running.
Then run my program form command line with python loadDatabases.py to set everything up.
Note that if for some reason you mess something up or already have databases of those names, you would need to drop them.
Then run python login.py to run my main program and you should be all set



