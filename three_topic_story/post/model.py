from three_topic_story import db
from datetime import datetime


class Post(db.Model):
    __tablename__ = 'Post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    tags = db.Column(db.String(20))
    body = db.Column(db.Text())
    author_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    create_date = db.Column(db.DateTime, default=datetime.utcnow)
    edit_date = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    private = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Post %s>' % self.title
