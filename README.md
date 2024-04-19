# SpotReveal - WORK IN PROGRESS
How to run the program

1. You need to install Django onto your computer, we recommend downloading it on your terminal: python -m pip install Django.
2. After installing Django, copy the files down into your program and type them into your terminal python manage.py makemigrations. This loads our database.
3. After the last step we want to set our migrations with python manage.py migrate.
4. After that is finished, run the program using python manage.py runserver
5. After the last step you click on the link that is outputted in the terminal: 'http://127.0.0.1:8000/' and look at your browser and should see a new tab open showing the SpotReveal menu

# SpotReveal
The front page asks the user to log in and a brief description of the web app's functions. 
After logging in the web app will reveal your personal top artists and top tracks that you have been listening to over the last 6 months.
The web app will also allow you to click and listen to a curated playlist based on your favorite tracks. This function opens a separate tab to the Spotify web player allowing you to listen 
to your new playlist. It can be accessed whenever the user wants to see the curated playlist on the web player.

# Things to add
* Need to add a database to let users access the website :P
* Fix up the website - It is very barebones at the moment
