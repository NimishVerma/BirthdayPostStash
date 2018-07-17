# BirthdayPostStash
~~tba~~


Road Plan
=========

1. Manage User -~~reg/login/~~forget
2. Add P-picture
3. Person module:
        .apis: get person, create person, delete person, update person's details
        .serialize persons
        .set fav_pic for person object
        
3. Add image obj foreign key-ed to user
4. add FC and FR to gallery
5. Host on ec2 instance(Refer:https://gist.github.com/Atem18/4696071)


Installation
==============

1. cd ~
2. mkdir env
3. cd env
4. virtualenv bpstash
5. cd/path/to/project
6. source activate.sh
7. pip install -r requirements.txt
8. python manage.py runserver


(Please work on this virtual env and if you insall dependencies, freeze and update them in requirements.txt)


Current Flow
==============
https://ibb.co/h8b698



