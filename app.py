from flask import Flask, jsonify, request
from models import db, migrate, Episode, Guest, Appearance

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate.init_app(app, db)


@app.route("/episodes")
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([e.to_dict() for e in episodes])

@app.route("/episodes/<int:id>")
def get_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        return jsonify({"error": "Episode not found"}), 404
    return jsonify({
        "id": episode.id,
        "date": episode.date,
        "number": episode.number,
        "appearances": [a.to_dict() for a in episode.appearances]
    })

@app.route("/guests")
def get_guests():
    guests = Guest.query.all()
    return jsonify([g.to_dict() for g in guests])

@app.route("/appearances", methods=["POST"])
def create_appearance():
    data = request.get_json()

    try:
        rating = int(data["rating"])
        guest_id = int(data["guest_id"])
        episode_id = int(data["episode_id"])
    except (KeyError, ValueError):
        return jsonify({"errors": ["Invalid data"]}), 400

    appearance = Appearance(rating=rating, guest_id=guest_id, episode_id=episode_id)

    if not appearance.validate():
        return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400

    db.session.add(appearance)
    db.session.commit()

    return jsonify(appearance.to_dict()), 201

if __name__ == "__main__":
    app.run(debug=True)
