# teams-bot-test

### Deploy using Heroku Git
#### Connect to existed heroku app
```
heroku login
heroku git:remote -a ms-teams-chatbot
```
#### Deploy my application
```
git add .
git commit -m "add profile"
git push heroku master
```