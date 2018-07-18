# BirthdayPostStash
~~tba~~
https://demo-bpstash.herokuapp.com/

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
5. Setting up djcelery(Refer:http://michal.karzynski.pl/blog/2014/05/18/setting-up-an-asynchronous-task-queue-for-django-using-celery-redis/, https://github.com/celery/celery/tree/master/examples/django/proj)
6. Celery with supervisord(Refer:https://thomassileo.name/blog/2012/08/20/how-to-keep-celery-running-with-supervisor/)
7. Setting up ec2 instance(Refer:https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/get-set-up-for-amazon-ec2.html)
8. Host on ec2 instance(Refer:https://gist.github.com/Atem18/4696071)


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


Current Flow
==============
https://ibb.co/h8b698



