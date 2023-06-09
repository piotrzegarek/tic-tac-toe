from app import create_app, socketio
from app.models import db

app = create_app()

@app.cli.command("runserver")
def run():
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)

# @app.cli.command("initdb")
@app.route("/create_db")
def init_db():
    print("Initializing database")
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)