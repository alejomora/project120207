# -*- coding: utf-8 -*-

from __future__ import with_statement
from contextlib import closing
from flask import Flask, g, render_template, session, abort, request, flash, redirect, url_for
import os
import sqlite3


#Configuration
DATABASE = os.path.dirname(os.path.realpath(__file__))+'/web.db'
DEBUG = True
SECRET_KEY = 'my strong key'
SCHEMA = 'schema.sql'

#Configure application
app = Flask(__name__)
app.config.from_object(__name__)

#Database function
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def update_entry_db(key, value):
    cur = g.db.execute('select count(*) from entries where key=?',(key,))
    if cur.fetchone()[0] > 0:
        g.db.execute('update entries set value=? where key=?',(value,key,))
    else:
        g.db.execute('insert into entries(key,values) values(?,?)',(key,value,))

def get_entry(key):
    value = None
    cur = g.db.execute('select count(*) from entries where key=?',(key,))
    if cur.fetchone()[0] > 0:
        cur = g.db.execute('select value from entries where key=?',(key,))
        value = cur.fetchone()[0]

    return value


#This function execute one step
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource(app.config['SCHEMA']) as schema:
            db.cursor().executescript(schema.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.context_processor
def utility_processor():
    return dict(get_entry=get_entry)

@app.route('/')
def show_entries():

    cur = g.db.execute('select key, value from entries')
    entries = [dict(key=row[0], value=row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():

    if not session.get('logged_in'):
        abort(401)

    update_entry_db(request.form['key'],request.form['value'])

    g.db.commit()

    flash(u'Новая запись добавлена!')

    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = get_entry('web_username')
        password = get_entry('web_password')

        if request.form['username'] != username:
            error = u'Неверный пользователь!'
        elif request.form['password'] != password:
            error = u'Неверный пароль'
        else:
            session['logged_in'] = True
            flash(u'Вход произведен. Сеанс работы начат!')
            return redirect(url_for('show_entries'))

    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(u'Сеанс завершен!')
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run()
