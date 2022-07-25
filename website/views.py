from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
import random
import secrets

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    
    if request.method == 'POST':
        title = request.form.get('note')
        siteusername = request.form.get('siteusername')
        
        def Passwordgenerater():
            lower = 'abcdefghijklmnopqrstuvwxyz'
            upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            nums = str(secrets.randbits(35))
            symbols = '!@#$%^&*'
            string = lower + upper + nums + symbols
            stage_1 = ''.join(random.sample(string,15))
            stage_2 = ''.join(random.sample(stage_1,15))
            return stage_2

        generatedPassword = Passwordgenerater()

        if len(title) < 1:
            flash('Enter a Website/App name!', category='error')
        elif len(siteusername) < 1 :
            flash('enter a user name!', category='error')
        else:
            new_note = Note(data=title, key=generatedPassword,username=siteusername ,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Password added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
