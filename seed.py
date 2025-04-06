import csv
from app import app
from models import db, Episode, Guest, Appearance

def get_or_create_episode(date_str):
    episode = Episode.query.filter_by(date=date_str).first()
    if not episode:
        episode = Episode(date=date_str)
        db.session.add(episode)
        db.session.flush()  # To get episode.id
    return episode

def get_or_create_guest(name, occupation):
    guest = Guest.query.filter_by(name=name).first()
    if not guest:
        guest = Guest(name=name.strip(), occupation=occupation.strip())
        db.session.add(guest)
        db.session.flush()  # To get guest.id
    return guest

with app.app_context():
    db.drop_all()
    db.create_all()

    with open("seed.csv", newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            raw_guests = row["Raw_Guest_List"]
            if raw_guests.strip() == "NA":
                continue  # Skip rows with no guest info

            date = row["Show"]
            occupation = row["GoogleKnowlege_Occupation"]

            # Handle multiple guests
            guest_names = [name.strip() for name in raw_guests.split(",")]

            episode = get_or_create_episode(date)

            for guest_name in guest_names:
                guest = get_or_create_guest(guest_name, occupation)
                # Avoid duplicate appearances
                existing = Appearance.query.filter_by(guest_id=guest.id, episode_id=episode.id).first()
                if not existing:
                    appearance = Appearance(guest_id=guest.id, episode_id=episode.id, rating=5)  # Arbitrary default rating
                    db.session.add(appearance)

        db.session.commit()
        print("✅ Database seeded successfully!")
