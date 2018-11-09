from app import db


class Translator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    text_translated = db.Column(db.String(255))
    uid = db.Column(db.String(50))
    status = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return '<Text %r>' % self.text
