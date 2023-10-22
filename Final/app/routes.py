import os
from flask import flash, redirect, render_template, request, session, url_for, jsonify
from app import app, db, mail
from werkzeug.security import check_password_hash, generate_password_hash
from app.form import LoginForm, RegisterForm, QuoteForm, WordForm, UpdateForm, ResetForm, ResetPasswordForm
from app.models import User, Book, Word
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message 


# index route 
@app.route("/")
def index():

    return render_template("home.html")

# login route
@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('You have been successfully logged in!', 'success') 
            next_page = request.args.get('next')
            return redirect(next_page or(url_for('index')))
        else:
            flash('Login failed, Please check your username and password!', 'danger')

    return render_template("login.html", form=form)

# logout route
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():

    logout_user()
    return redirect('/')

# sign up route
@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        flash(f'Welcome {form.username.data}!', 'success')
        password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')  

    return render_template("register.html", form=form)


@app.route("/words", methods=["GET", "POST"])
@login_required
def words():

    words = Word.query.filter_by(user_id=str(current_user.id)).all()
    return render_template('words.html', words=words)


@app.route("/quotes", methods=["GET", "POST"])
@login_required
def quotes():


    books = Book.query.filter_by(user_id=str(current_user.id)).all()

    return render_template('quotes.html', books=books)

# route for adding a new quote
@app.route("/new/quote", methods=["GET", "POST"])
@login_required
def new_quote():
    
    form = QuoteForm()

    if request.method == "POST" and form.validate_on_submit():

        book = Book(title=form.title.data, author=form.author.data, content=form.content.data, reader=current_user)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('newquote.html', form=form)

# route for adding a new word
@app.route("/new/word", methods=["GET", "POST"])
@login_required
def new_word():

    form = WordForm()

    if request.method == "POST" and form.validate_on_submit():
        word = Word(
            word=form.word.data.strip(), 
            synonym=form.synonym.data.strip(), 
            part_of_speech=form.part_of_speech.data.strip(), 
            example=form.example.data.strip(),
            definition=form.definition.data.strip(), 
            reader=current_user
            )
        
        db.session.add(word)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('newword.html', form=form)

# account route to update credentials
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateForm() 

    if request.method == "POST" and form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template('account.html', form=form)


@app.route("/words/review", methods=["GET", "POST"])
@login_required
def word_review():

    page = request.args.get('page', 1, type=int)
    
    words = Word.query.order_by(Word.id.desc()).filter_by(user_id=str(current_user.id)).paginate(page=page, per_page=2)

    return render_template('learnt_words.html', words=words)


@app.route("/quotes/review", methods=["GET", "POST"])
@login_required
def quotes_review():    

    page = request.args.get('page', 1, type=int)
    
    books = Book.query.order_by(Book.id.desc()).filter_by(user_id=str(current_user.id)).paginate(page=page, per_page=2)

    return render_template('learnt_book.html', books=books)


@app.route("/book/<int:book_id>/update", methods=["GET", "POST"])
@login_required
def update_book(book_id):

    book = Book.query.get_or_404(book_id)

    form = QuoteForm()
    
    if request.method == "POST" and form.validate_on_submit():   
        book.title = form.title.data.strip()
        book.author = form.author.data.strip()
        book.content = form.content.data.strip()
        db.session.commit()
        flash('Your Quote has been updated!', 'success')
        return redirect(url_for('quotes_review'))
    elif request.method == "GET":
        form.title.data = book.title
        form.author.data = book.author
        form.content.data = book.content

    return render_template('newquote.html', titel='Update Book', form=form )


@app.route("/delete/<int:book_id>/quote", methods=["GET"])
@login_required
def delete_quote(book_id):

    book = Book.query.get_or_404(book_id)

    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('quotes_review'))


@app.route('/update/<int:word_id>/word', methods=["GET", "POST"])
@login_required
def update_word(word_id):

    word = Word.query.get_or_404(word_id)

    form = WordForm()

    if request.method == "POST" and form.validate_on_submit():
        word.word = form.word.data.strip()
        word.definition = form.definition.data.strip()
        word.part_of_speech = form.part_of_speech.data.strip()
        word.synonym = form.synonym.data.strip()
        word.example = form.example.data.strip()
        db.session.commit()
        return redirect(url_for('word_review'))
    elif request.method == "GET":
        form.word.data = word.word
        form.definition.data = word.definition
        form.part_of_speech.data = word.part_of_speech
        form.synonym.data = word.synonym
        form.example.data = word.example
    return render_template('newword.html', titel='Update Word', form=form)


@app.route("/delete/<int:word_id>/word", methods=["GET"])
@login_required
def delete_word(word_id):

    word = Word.query.get_or_404(word_id)
    
    db.session.delete(word)
    db.session.commit()

    return redirect(url_for('word_review'))


def send_email(user):

    token = user.get_reset_token()
    msg = Message('Reset Your Password', 
                  sender='noreply.quodophile@gmail.com',
                  recipients=[user.email])

    msg.body = f''' Click on the link to reset your password:
{url_for('reset_password', token=token, _external=True)}
'''
    mail.send(msg)


@app.route("/reset", methods=["GET", "POST"])
def reset():

    form = ResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash('Please enter the correct email address')
            return redirect(url_for('reset'))
        
        send_email(user)
        flash('Please check your email to reset your password.')
        return redirect(url_for('login'))

    return render_template('reset.html', form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    
    user = User.verify_reset_token(token)

    form = ResetPasswordForm()

    if user is None:
        flash('The Token is expired')
        return redirect(url_for('reset'))
    
    if request.method == "POST" and form.validate_on_submit():
        password = generate_password_hash(form.password.data)
        user.password = password
        db.session.commit()
        flash('You password has been updated!')
        return redirect(url_for('login'))

    return render_template('reset_password.html', form=form)

@app.route("/random", methods=["GET", "POST"])
@login_required
def random_quote():

    # get the data POSTED to backend 
    data = request.get_json()

    if data:
        book = Book(title='', content=data['quote'], author=data['author'], reader=current_user)
        db.session.add(book)
        db.session.commit()
        print('success')

    return render_template('random_quote.html')

