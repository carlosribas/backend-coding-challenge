from flask import render_template, flash, redirect, url_for, request
from app import app, db
from forms import TranslatorForm
from models import Translator
from unbabel_api import post_translation, get_translation
from sqlalchemy.sql.expression import func
from rq import Queue
from worker import conn

translation_queue = Queue(connection=conn)


def create_translation(post_text):
    post_text = post_translation(post_text)
    new_text = Translator(
        text=post_text.text,
        uid=post_text.uid,
        status='requested'
    )
    db.session.add(new_text)
    db.session.commit()


def update_translation(id, uid):
    text = Translator.query.get(id)
    get_text = get_translation(uid)

    if get_text.status == 'completed':
        text.text_translated = get_text.translation
        text.status = 'translated'
        db.session.commit()

    elif get_text.status == 'translating':
        text.status = 'pending'
        db.session.commit()


@app.route("/", methods=['GET', 'POST'])
def home():
    form = TranslatorForm()
    texts = Translator.query.order_by(func.length(Translator.text))

    if request.method == 'POST' and form.validate_on_submit():
        translation_queue.enqueue_call(func=create_translation, args=(form.text.data,))
        flash('Your text will be translated. Please wait.', 'success')
        return redirect(url_for('home'))

    else:
        not_translated = Translator.query.filter_by(text_translated=None).all()
        if not_translated:
            for item in not_translated:
                translation_queue.enqueue_call(func=update_translation, args=(item.id, item.uid))

    return render_template('home.html', form=form, texts=texts)
