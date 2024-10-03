from app import create_app, db
from app.models import User, Ticket

app = create_app()

@app.cli.command('initdb')
def init_db():
    db.create_all()
    print('Initialized the database.')

if __name__ == '__main__':
    app.run(debug=True)