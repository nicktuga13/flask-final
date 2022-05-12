"""
Testing the application's capability to upload csv files (specifically transaction tpyes)
"""
import os

from flask_login import FlaskLoginClient

from app import db
from app.auth.forms import csv_upload
from app.db.models import User


def test_upload_csv(application):
    """ Creating an admin user and uploading a csv file as them """
    application.test_client_class = FlaskLoginClient
    user = User('abc12@njit.edu', '123abc')
    db.session.add(user)
    db.session.commit()
    assert user.email == 'abc12@njit.edu'

    root = os.path.dirname(os.path.abspath(__file__))
    transactions_csv = os.path.join(root, '../uploads/transactions2.csv')

    with application.test_client(user=user) as client:
        response = client.get('/transactions/upload')
        assert response.status_code == 200
        form = csv_upload()
        form.file = transactions_csv
        assert form.validate


def test_upload_csv_failure(application):
    """ Attempting to upload a csv file without being logged in """
    application.test_client_class = FlaskLoginClient
    assert db.session.query(User).count() == 0
    with application.test_client(user=None) as client:
        response = client.get('/transactions/upload')
        assert response.status_code == 302
