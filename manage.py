from app import create_app, sio
from app.models import db

app = create_app()

@app.route("/create_db")
#@app.cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    return "DB created"

if __name__ == "__main__":
    sio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
