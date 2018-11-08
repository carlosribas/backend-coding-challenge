import time
from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import TranslatorForm
from models import Translator
from unbabel_api import post_translation, get_translation
from sqlalchemy.sql.expression import func
from rq import Queue
from worker import conn

translation_queue = Queue(connection=conn)


def create_translation(id, text):
    text_to_be_translated = Translator.query.get(id)
    post_text = post_translation(text)
    text_to_be_translated.uid = post_text.uid
    db.session.commit()


def update_translation(id):
    text = Translator.query.get(id)
    time.sleep(10)
    get_text = get_translation(text.uid)

    if get_text.status == 'completed':
        text.text_translated = get_text.translation
        text.status = 'translated'
        db.session.commit()

    elif get_text.status == 'translating':
        text.status = 'pending'
        db.session.commit()
        update_translation(id)

    elif get_text.status == 'new':
        update_translation(id)


@app.route("/", methods=['GET', 'POST'])
def home():
    form = TranslatorForm()
    texts = Translator.query.order_by(func.length(Translator.text_translated))

    if request.method == 'POST' and form.validate_on_submit():
        new_text = Translator(
            text=form.text.data,
            status='requested'
        )
        db.session.add(new_text)
        db.session.commit()
        new_request = translation_queue.enqueue_call(create_translation, args=(new_text.id, new_text.text,))
        translation_queue.enqueue(update_translation, args=(new_text.id,), depends_on=new_request)
        flash('Your text will be translated. Please wait.', 'success')
        return redirect(url_for('home'))

    return render_template('home.html', form=form, texts=texts)
