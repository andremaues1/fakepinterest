from FakePinterest.models import Usuario,Foto
from FakePinterest import app,database

with app.app_context():
    database.create_all()