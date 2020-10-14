# Project2 - Milestone 1

Hi, There! This is my Chat application! This application can be used to talk to people. This application also has a bot to interact with!
Here are the steps so enjoy!

## 0. Clone this repo
```$ git clone https://github.com/Sresht/lect8-react```

## First we need to download so type these commands: 

## 1. Upgrade Node version to 7

```$ nvm install 7```

```$ npm install```

This command runs `npm`, which looks inside our `package.json` file, 
retrieves a list of packages, and installs them to the `node_modules` folder
inside your repository.

## 3. Add files to your .gitignore

```$ touch .gitignore; echo "node_modules/" >> .gitignore; ```
```$ echo "static/script.js" >> .gitignore```
```$ npm install```
##4. run these commands:
  ```pip install flask-socketio```
  ```pip install eventlet```
  ```npm install -g webpack```
   ```npm install --save-dev webpack```
    ```npm install socket.io-client --save```
Warning: If the commands do not work try  "sudo" in front of pip :) 

## To Set PSQL run these commands. 
  ```sudo yum update```
  ```sudo /usr/local/bin/pip install --upgrade pip```
  ```sudo /usr/local/bin/pip install psycopg2-binary```
  ```sudo /usr/local/bin/pip install Flask-SQLAlchemy==2.1```


## 4. Setting up PSQL 
  ```sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs```
  ```sudo service postgresql initdb```
   
   ```sudo service postgresql start```
   ```sudo -u postgres createuser --superuser $USER```
   ```sudo -u postgres createdb $USER```
## 5. to setup your username and password for database 
   ```create user [some_username_here] superuser password '[some_unique_new_password_here]';``` password does not have to be long 
## 6. Create pro2.env file  
     ```touch pro2.env```
type in to the pro2 file -> export DATABASE_URL=postgresql://[YOUR_USERNAME]:[YOUR_PASS]@localhost/postgres

## 7. finally to enable read and write from sql 
      in the terminal: ``` sudo vim /var/lib/pgsql9/data/pg_hba.conf ```
      in the vim file: ```:%s/ident/md5/g```
        type: ```:wq ``` to save and exit 
      restart your sql 
        ```sudo service postgresql restart```
       than run ``` npm run watch ``` 
## 8. YOUR ALL SET ENJOY 



Known Problems: 
  1) Updating of the user counter does not work how it supposed to. The updating should happen when any user has opened an application. I would fix this issue by making changes
      to connecting socket where user has immidetly lunched the application, and making changes also to disconnecing socket to record user that has left the chat.
  2) The messages from the data base does not have name attached to the messages. I would fix that by having parallel array to see who said what in the past. 
  3) The command !! funtranslate does not work. This is because i used google translate api to translate text. The google api was a json file so i had issues sending it to heroku. I would solve this by using a different tranlation api. 

Technical issues: 

  1) In the process of pushing data base to heroku i ran in to the problem for the command -> " PGUSER= USERNAME heroku pg:push postgres DATABASE_URL" 
       this was fixed thanks to people in the slack. The command caused an error to be dumped there for just taking out PGUSER= USERNAME fixed the issue.
  2) For the socket data[] i tried to use userCounter as an integer. This caused an error because it became string in the backend. Therefore i changed the data going to the              backend to .toString() and converted back to int in the python file. 
  3) I could not use global variable in the python file for the counter. Therefore i fixed it by passing through data[] which kept track of the counter. 
  4) I could not import css file in the react files. simply by adding ./staic/styles.css did not work. The copy file path option did not work as well. I searched on the internet 
      to try to get full path and i found by typing "readlink -f [filename]" will give you full file path so that you can import css file. 
  
