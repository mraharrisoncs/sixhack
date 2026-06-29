from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False, index=True)
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    submissions = db.relationship('Submission', backref='user', lazy=True,
                                  cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id           = db.Column(db.String(20),  primary_key=True)
    title        = db.Column(db.String(200), nullable=False, index=True)
    description  = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    starter_code = db.Column(db.Text, nullable=False)
    difficulty   = db.Column(db.String(20), nullable=False)
    spec_level   = db.Column(db.String(20))
    topic        = db.Column(db.String(100))
    free         = db.Column(db.Boolean, default=False, index=True)
    max_lines    = db.Column(db.Integer)
    max_bytes    = db.Column(db.Integer)

    solutions = db.Column(db.JSON, nullable=False)
    hints     = db.Column(db.JSON, nullable=False)
    tests     = db.Column(db.JSON, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    submissions = db.relationship('Submission', backref='challenge', lazy=True,
                                  cascade='all, delete-orphan')


class Submission(db.Model):
    __tablename__ = 'submissions'

    id           = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(db.String(20), db.ForeignKey('challenges.id'),
                             nullable=False, index=True)
    paradigm     = db.Column(db.String(20), nullable=False)
    code         = db.Column(db.Text, nullable=False)
    score        = db.Column(db.Integer, default=0)

    test_results = db.Column(db.JSON)
    passed_tests = db.Column(db.Integer, default=0)
    total_tests  = db.Column(db.Integer, default=0)

    student_name  = db.Column(db.String(200))
    teacher_email = db.Column(db.String(120))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Signup(db.Model):
    __tablename__ = 'signups'

    id         = db.Column(db.Integer, primary_key=True)
    type       = db.Column(db.String(20), nullable=False)   # 'newsletter' | 'early_adopter'
    email      = db.Column(db.String(120), nullable=False, index=True)
    school     = db.Column(db.String(200))
    role       = db.Column(db.String(50))
    code       = db.Column(db.String(30))                   # early adopter code, if generated
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class Email(db.Model):
    __tablename__ = 'emails'

    id                  = db.Column(db.Integer, primary_key=True)
    submission_id       = db.Column(db.Integer, db.ForeignKey('submissions.id'), nullable=False)
    to_email            = db.Column(db.String(120), nullable=False, index=True)
    student_name        = db.Column(db.String(200), nullable=False)
    status              = db.Column(db.String(20), default='pending')
    sendgrid_message_id = db.Column(db.String(255))
    error_message       = db.Column(db.Text)
    created_at          = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at             = db.Column(db.DateTime)
