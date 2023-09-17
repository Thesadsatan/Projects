from flask import flash, redirect, render_template, request, session, url_for, jsonify
from app.models import User, Book, Word
from flask_mail import Message 
from app import app, db, mail
import requests
import asyncio
from celery import Celery
from apscheduler.schedulers.background import BackgroundScheduler

celery = Celery(app.name, broker='redis://localhost:6379/0')


@celery.task
def send_async_email(email_data, us):
    print('hello')
    msg = Message(email_data['subject'],
                  sender='hamidiartaug@gmail.com',
                  recipients=[email_data['to']])
    msg.body = email_data['body']
    print('hello')
    us.emailed_word = int(us.emailed_word + 1)
    db.session.commit()
    with app.app_context():
        print('hello')
        mail.send(msg)





users = User.query.all()



def testing():
    # with app.app_context():


        # users = User.query.all()

    for user in users:
        us = user
        print
        email = user.email
        print(email)
        word = Word.query.filter_by(user_id=user.id, word_email=user.emailed_word).first()
        quote = Book.query.filter_by(user_id=user.id, book_email=user.emailed_quote).first()
        mess = {}

        if word is None and quote is None:

            mess = {
                'subject': 'Testing', 
                'to': email,
                'body': f''' No quotes for today!
                Please update your quotes '''
            }
            # send_async_email(mess)

        elif word is not None and quote is None:

            mess = {
                'subject': 'Testing', 
                'to': email,
                'body': f''' Today's Word: 
                {word.word}: {word.content}.
                Please update your quotes!'''
            }
            user.emailed_word = int(user.emailed_word + 1)
            db.session.commit()
            print('hello')
            # send_async_email(mess)

        elif word is None and quote is not None:
            
            mess = {
                'subject': 'Testing', 
                'to': email,
                'body': f''' Today's quote: 
                "{quote.content}." 
                _{quote.author}, {quote.title}
                Please update your words!'''
            }
            user.emailed_quote = int(user.emailed_quote + 1)
            db.session.commit()
            print('hello')
            # send_async_email(mess)
        
        else:
            mess = {
                'subject': 'Testing', 
                'to': email,
                'body': f''' Today's quote: 
                "{quote.content}." 
                _{quote.author}, {quote.title}
                
                Today's word:
                {word.word}: {word.content}'''
            }
            user.emailed_quote = int(user.emailed_quote + 1)
            user.emailed_word = int(user.emailed_word + 1)
            db.session.commit()
            print('hello')
        # send_async_email(mess)
    db.session.commit()
    send_async_email(mess,us)






sched = BackgroundScheduler(daemon=True)
sched.add_job(testing, 'interval', seconds=30)
sched.start()

# # # # sched = BackgroundScheduler(daemon=True)
# # # # sched.add_job(testing,'interval',seconds=120)
# # # # sched.start()

# # from flask import flash, redirect, render_template, request, session, url_for, jsonify
# # from app.models import User, Book, Word
# # from flask_mail import Message 
# # from app import app, db, mail
# # import requests
# # import asyncio
# # from celery import Celery
# # from apscheduler.schedulers.background import BackgroundScheduler

# # celery = Celery(app.name, broker='redis://localhost:6379/0')


# # @celery.task
# # def send_async_email(email_data):
# #     print('hello')
# #     msg = Message(email_data['subject'],
# #                   sender='hamidiartaug@gmail.com',
# #                   recipients=[email_data['to']])
# #     msg.body = email_data['body']
# #     print('hello')
# #     db.session.commit()
# #     with app.app_context():
# #         print('hello')
# #         mail.send(msg)


# # def testing():
# #     with app.app_context():
# #         users = User.query.all()

# #         for user in users:
# #             email = user.email
# #             word = Word.query.filter_by(user_id=user.id, word_email=user.emailed_word).first()
# #             quote = Book.query.filter_by(user_id=user.id, book_email=user.emailed_quote).first()
# #             mess = {}

# #             if word is None and quote is None:
# #                 mess = {
# #                     'subject': 'Testing', 
# #                     'to': email,
# #                     'body': f''' No quotes for today!
# #                     Please update your quotes '''
# #                 }
# #             elif word is not None and quote is None:
# #                 mess = {
# #                     'subject': 'Testing', 
# #                     'to': email,
# #                     'body': f''' Today's Word: 
# #                      {word.word}: {word.content}.
# #                      Please update your quotes!'''
# #                 }
# #                 user.emailed_word = int(user.emailed_word + 1)
# #             elif word is None and quote is not None:
# #                 mess = {
# #                     'subject': 'Testing', 
# #                     'to': email,
# #                     'body': f''' Today's quote: 
# #                      "{quote.content}." 
# #                      _{quote.author}, {quote.title}
# #                      Please update your words!'''
# #                 }
# #                 user.emailed_quote = int(user.emailed_quote + 1)
# #             else:
# #                 mess = {
# #                     'subject': 'Testing', 
# #                     'to': email,
# #                     'body': f''' Today's quote: 
# #                      "{quote.content}." 
# #                      _{quote.author}, {quote.title}
                     
# #                      Today's word:
# #                      {word.word}: {word.content}'''
# #                 }
# #                 user.emailed_quote = int(user.emailed_quote + 1)
# #                 user.emailed_word = int(user.emailed_word + 1)

# #             db.session.commit()
# #             send_async_email(mess)


# # sched = BackgroundScheduler(daemon=True)
# # sched.add_job(testing, 'interval', seconds=30)
# # sched.start()


# from flask import flash, redirect, render_template, request, session, url_for, jsonify
# from app.models import User, Book, Word
# from flask_mail import Message 
# from app import app, db, mail
# import requests
# import asyncio
# from celery import Celery
# from apscheduler.schedulers.background import BackgroundScheduler

# celery = Celery(app.name, broker='redis://localhost:6379/0')


# @celery.task
# def send_async_email(email_data):
#     print('hello')
#     msg = Message(email_data['subject'],
#                   sender='hamidiartaug@gmail.com',
#                   recipients=[email_data['to']])
#     msg.body = email_data['body']
#     print('hello')
#     db.session.commit()
#     with app.app_context():
#         print('hello')
#         mail.send(msg)





# users = User.query.all()



# def testing():
    
#     # users = User.query.all()


#     for user in users:

#         email = user.email
#         print(email)
#         word = Word.query.filter_by(user_id=user.id, word_email=user.emailed_word).first()
#         quote = Book.query.filter_by(user_id=user.id, book_email=user.emailed_quote).first()
#         mess = {}

#         if word is None and quote is None:

#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' No quotes for today!
#                 Please update your quotes '''
#             }
#              # send_async_email(mess)

#         elif word is not None and quote is None:

#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' Today's Word: 
#                  {word.word}: {word.content}.
#                  Please update your quotes!'''
#             }
#             user.emailed_word = int(user.emailed_word + 1)
#             # db.session.commit()
#             print('hello')
#             # send_async_email(mess)

#         elif word is None and quote is not None:
            
#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' Today's quote: 
#                  "{quote.content}." 
#                  _{quote.author}, {quote.title}
#                  Please update your words!'''
#             }
#             user.emailed_quote = int(user.emailed_quote + 1)
#             # db.session.commit()
#             print('hello')
#             # send_async_email(mess)
        
#         else:
#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' Today's quote: 
#                  "{quote.content}." 
#                  _{quote.author}, {quote.title}
                 
#                  Today's word:
#                  {word.word}: {word.content}'''
#             }
#             user.emailed_quote = int(user.emailed_quote + 1)
#             user.emailed_word = int(user.emailed_word + 1)
#             # db.session.commit()
#             print('hello')
#             # send_async_email(mess)
#         db.session.commit()
#         send_async_email(mess)






# sched = BackgroundScheduler(daemon=True)
# sched.add_job(testing, 'interval', seconds=30)
# sched.start()

# from flask import flash, redirect, render_template, request, session, url_for, jsonify
# from app.models import User, Book, Word
# from flask_mail import Message 
# from app import app, db, mail
# import requests
# import asyncio
# from celery import Celery
# from apscheduler.schedulers.background import BackgroundScheduler

# celery = Celery(app.name, broker='redis://localhost:6379/0')


# @celery.task
# def send_async_email(email_data):
#     print('hello')
#     msg = Message(email_data['subject'],
#                   sender='hamidiartaug@gmail.com',
#                   recipients=[email_data['to']])
#     msg.body = email_data['body']
#     print('hello')
#     db.session.commit()
#     with app.app_context():
#         print('hello')
#         mail.send(msg)


# def testing():


#     users = User.query.all()

#     for user in users:

#         # db.session.refresh(user)

#         email = user.email

#         print(email)
#         word = Word.query.filter_by(user_id=user.id, word_email=user.emailed_word).first()
#         quote = Book.query.filter_by(user_id=user.id, book_email=user.emailed_quote).first()
#         mess = {}

#         if word is None and quote is None:

#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' No quotes for today!
#                 Please update your quotes '''
#             }
#              # send_async_email(mess)

#         elif word is not None and quote is None:

#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' Today's Word: 
#                  {word.word}: {word.content}.
#                  Please update your quotes!'''
#             }
#             user.emailed_word = int(user.emailed_word + 1)
#             db.session.commit()
#             print('hello')
#             # send_async_email(mess)

#         elif word is None and quote is not None:
            
#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' Today's quote: 
#                  "{quote.content}." 
#                  _{quote.author}, {quote.title}
#                  Please update your words!'''
#             }
#             user.emailed_quote = int(user.emailed_quote + 1)
#             db.session.commit()
#             print('hello')
#             # send_async_email(mess)
        
#         else:
#             mess = {
#                 'subject': 'Testing', 
#                 'to': email,
#                 'body': f''' Today's quote: 
#                  "{quote.content}." 
#                  _{quote.author}, {quote.title}
                 
#                  Today's word:
#                  {word.word}: {word.content}'''
#             }
#             user.emailed_quote = int(user.emailed_quote + 1)
#             user.emailed_word = int(user.emailed_word + 1)
#             db.session.commit()
#             print('hello')
#             # send_async_email(mess)

#         send_async_email(mess)



# sched = BackgroundScheduler(daemon=True)
# sched.add_job(testing, 'interval', seconds=30)
# sched.start()

# from flask import flash, redirect, render_template, request, session, url_for, jsonify
# from app.models import User, Book, Word
# from flask_mail import Message 
# from app import app, db, mail
# import requests
# import asyncio
# from celery import Celery
# from apscheduler.schedulers.background import BackgroundScheduler

# celery = Celery(app.name, broker='redis://localhost:6379/0')

# @celery.task
# def send_async_email(email_data):
#     msg = Message(email_data['subject'],
#                   sender='hamidiartaug@gmail.com',
#                   recipients=[email_data['to']])
#     msg.body = email_data['body']
#     print('hello')
#     mail.send(msg)

# def send_email(subject, to, body):
#     email_data = {
#         'subject': subject,
#         'to': to,
#         'body': body
#     }
#     send_async_email.delay(email_data)

# def testing():
#     users = User.query.all()

#     for user in users:
#         email = user.email
#         print('HELLO')

#         word = Word.query.filter_by(user_id=user.id, word_email=user.emailed_word).first()
#         quote = Book.query.filter_by(user_id=user.id, book_email=user.emailed_quote).first()

#         if word is None and quote is None:
#             print('HELLO')
#             subject = 'Testing'
#             body = 'No quotes for today! Please update your quotes'
#             send_email(subject, email, body)

#         elif word is not None and quote is None:
#             print('HELLO')

#             subject = 'Testing'
#             body = f'Today\'s Word: {word.word}: {word.content}. Please update your quotes!'
#             user.emailed_word = user.emailed_word + 1
#             db.session.commit()
#             send_email(subject, email, body)

#         elif word is None and quote is not None:
#             print('HELLO')

#             subject = 'Testing'
#             body = f'Today\'s quote: "{quote.content}." _{quote.author}, {quote.title}. Please update your words!'
#             user.emailed_quote = user.emailed_quote + 1
#             db.session.commit()
#             send_email(subject, email, body)
        
#         else:
#             print('HELLO')

#             subject = 'Testing'
#             body = f'Today\'s quote: "{quote.content}." _{quote.author}, {quote.title}. Today\'s word: {word.word}: {word}'


# sched = BackgroundScheduler(daemon=True, misfire_grace_time=60)
# sched.add_job(testing, 'interval', seconds=30)
# sched.start()


# this 

# from flask import flash, redirect, render_template, request, session, url_for, jsonify
# from app.models import User, Book, Word
# from flask_mail import Message 
# from app import app, db, mail
# import requests
# import asyncio
# from celery import Celery
# from apscheduler.schedulers.background import BackgroundScheduler

# celery = Celery(app.name, broker='redis://localhost:6379/0')

# @celery.task
# def send_async_email(email_data):
#     msg = Message(email_data['subject'],
#                   sender='hamidiartaug@gmail.com',
#                   recipients=[email_data['to']])
#     msg.body = email_data['body']
#     print('hello')
#     mail.send(msg)

# def send_email(subject, to, body):
#     email_data = {
#         'subject': subject,
#         'to': to,
#         'body': body
#     }
#     send_async_email.delay(email_data)

# def testing():
#     with app.app_context():
#         users = User.query.all()

#         for user in users:
#             email = user.email
#             print('HELLO')

#             word = Word.query.filter_by(user_id=user.id, word_email=user.emailed_word).first()
#             quote = Book.query.filter_by(user_id=user.id, book_email=user.emailed_quote).first()

#             if word is None and quote is None:
#                 print('HELLO')
#                 subject = 'Testing'
#                 body = 'No quotes for today! Please update your quotes'
#                 send_email(subject, email, body)

#             elif word is not None and quote is None:
#                 print('HELLO')

#                 subject = 'Testing'
#                 body = f'Today\'s Word: {word.word}: {word.content}. Please update your quotes!'
#                 user.emailed_word = user.emailed_word + 1
#                 db.session.commit()
#                 send_email(subject, email, body)

#             elif word is None and quote is not None:
#                 print('HELLO')

#                 subject = 'Testing'
#                 body = f'Today\'s quote: "{quote.content}." _{quote.author}, {quote.title}. Please update your words!'
#                 user.emailed_quote = user.emailed_quote + 1
#                 db.session.commit()
#                 send_email(subject, email, body)
            
#             else:
#                 print('HELLO')

#                 subject = 'Testing'
#                 body = f'Today\'s quote: "{quote.content}." _{quote.author}, {quote.title}. Today\'s word: {word.word}: {word}'


# sched = BackgroundScheduler(daemon=True, misfire_grace_time=60)
# sched.add_job(testing, 'interval', seconds=30)
# sched.start()


# from flask import flash, redirect, render_template, request, session, url_for, jsonify
# from app.models import User, Book, Word
# from flask_mail import Message 
# from app import app, db, mail
# import requests
# import asyncio
# from celery import Celery
# from apscheduler.schedulers.blocking import BlockingScheduler

# # celery = Celery(app.name, broker='redis://localhost:6379/0')

# # @celery.task
# # def send_async_email(email_data):
# #     msg = Message(email_data['subject'],
# #                   sender='hamidiartaug@gmail.com',
# #                   recipients=[email_data['to']])
# #     msg.body = email_data['body']
# #     print('hello')
# #     mail.send(msg)


# def send_email(subject, to, body):
#     # email_data = {
#     #     'subject': subject,
#     #     'to': to,
#     #     'body': body
#     # }
#     # print(email_data['to'])
#     # send_async_email.delay(email_data)
#     msg = Message(subject,
#                   sender='hamidiartaug@gmail.com',
#                   recipients=to)
#     msg.body = body
#     print('sent')
#     mail.send(msg)
#     print('sent')
              

# def testing():
#     with app.app_context():
#         users = User.query.all()

#         for user in users:
#             email = user.email
#             print('HELLO')

#             word = Word.query.filter_by(user_id=user.id, word_email=user.emailed_word).first()
#             quote = Book.query.filter_by(user_id=user.id, book_email=user.emailed_quote).first()

#             if word is None and quote is None:
#                 print('HELLO')
#                 subject = 'Testing'
#                 body = 'No quotes for today! Please update your quotes'
#                 send_email(subject, email, body)

#             elif word is not None and quote is None:
#                 print('HELLO')

#                 subject = 'Testing'
#                 body = f'Today\'s Word: {word.word}: {word.content}. Please update your quotes!'
#                 user.emailed_word = user.emailed_word + 1
#                 db.session.commit()
#                 send_email(subject, email, body)

#             elif word is None and quote is not None:
#                 print('HELLO')

#                 subject = 'Testing'
#                 body = f'Today\'s quote: "{quote.content}." _{quote.author}, {quote.title}. Please update your words!'
#                 user.emailed_quote = user.emailed_quote + 1
#                 db.session.commit()
#                 send_email(subject, email, body)
            
#             else:
#                 print('HELLO')

#                 subject = 'Testing'
#                 body = f'Today\'s quote: "{quote.content}." _{quote.author}, {quote.title}. Today\'s word: {word.word}: {word}'
        
#         # Close the database connection to prevent resource leaks
#         db.session.close()

# # sched = BlockingScheduler()
# # sched.add_job(testing, 'interval', seconds=30)
# # sched.start()

# testing()