import unittest
from app import create_app, db
from app.models import Subject, Topic, User
from app.services.progress import subject_progress, topics_progress

class TestProgressHelper(unittest.TestCase):
    def setUp(self):
        class TestConfig:
            TESTING = True
            SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
            SQLALCHEMY_TRACK_MODIFICATIONS = False
            SECRET_KEY = 'test'
        self.app = create_app(TestConfig)
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        # Seed teacher
        teacher = User(name='Teacher', email='t@example.com', role='teacher', department='CSE')
        teacher.set_password('pass')
        db.session.add(teacher)
        db.session.commit()
        self.teacher = teacher

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_subject_progress_empty(self):
        subj = Subject(name='Algorithms', code='CSX', teacher_id=self.teacher.id)
        db.session.add(subj)
        db.session.commit()
        self.assertEqual(subject_progress(subj), 0.0)

    def test_subject_progress_partial(self):
        subj = Subject(name='DS', code='CS101', teacher_id=self.teacher.id)
        db.session.add(subj)
        db.session.commit()
        # Add 4 topics, 2 completed
        specs = [
            ('Intro', False),
            ('Arrays', True),
            ('Linked Lists', True),
            ('Stacks', False),
        ]
        for i,(name, done) in enumerate(specs, start=1):
            t = Topic(subject_id=subj.id, name=name, order=i, is_completed=done)
            db.session.add(t)
        db.session.commit()
        self.assertEqual(subject_progress(subj), 50.0)

    def test_topics_progress(self):
        subj = Subject(name='Graphs', code='CS201', teacher_id=self.teacher.id)
        db.session.add(subj)
        db.session.commit()
        for i in range(1,6):
            t = Topic(subject_id=subj.id, name=f'Topic {i}', order=i, is_completed=(i % 2 == 0))
            db.session.add(t)
        db.session.commit()
        all_topics = subj.topics.order_by(Topic.order.asc()).all()
        self.assertEqual(topics_progress(all_topics), 40.0)  # 2/5 completed

