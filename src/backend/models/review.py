'''
This file stores the Review Model.
'''
from db import db


class ReviewModel(db.Model):
    '''
    This class defines the Review Model
    and contains Review's attributes.
    '''

    __tablename__ = 'Reviews'
    review_id = db.Column(db.String(100), primary_key=True)
    user_id = db.Column(db.String(100), db.ForeignKey('Users.user_id'))
    comment_id = db.Column(db.String(100),
                           db.ForeignKey('Comments.comment_id'))
    rating = db.Column(db.Float(precision=2))
    review_date = db.Column(db.DateTime)
    title = db.Column(db.Text)
    review_text = db.Column(db.Text)

    def _init_(self, review_id,
               user_id, comment_id,
               rating, review_date,
               title, review_text) -> None:
        self.review_id = review_id
        self.user_id = user_id
        self.comment_id = comment_id
        self.rating = rating
        self.review_date = review_date
        self.title = title
        self.review_text = review_text

    def __repr__(self) -> str:
        '''
        This class returns a string as a representation of the Review.
        '''
        return '<Review %r>' % self.review_id
