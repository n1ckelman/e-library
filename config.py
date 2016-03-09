import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


SQLALCHEMY_DATABASE_URI = 'postgres://nxzpfnweftzolf:-NxX4LTOwIvxwHole-Zn_Z_HnV@ec2-107-21-101-67.compute-1.amazonaws.com:5432/d4qjeuo93gousu'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
