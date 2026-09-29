import uuid
from database import SessionLocal
from models.complaint import ComplaintModel

def seed_db():
    db = SessionLocal()
    try:
        count = db.query(ComplaintModel).count()
        if count == 0:
            print("Database is empty. Seeding data...")
            sample1 = ComplaintModel(
                id=f"CMP-{str(uuid.uuid4())[:8].upper()}",
                title="Pothole on Main Street",
                description="Large pothole near the central mall causing traffic.",
                category="Roads & Infrastructure",
                location="Main Street",
                status="open",
                priority="high",
                ai_summary="Large pothole reported.",
                triaged_by="seed",
            )
            sample2 = ComplaintModel(
                id=f"CMP-{str(uuid.uuid4())[:8].upper()}",
                title="Garbage truck missed pickup",
                description="The trash wasn't picked up on Tuesday in Sector 4.",
                category="Waste Management",
                location="Sector 4",
                status="resolved",
                priority="normal",
                ai_summary="Missed garbage pickup.",
                triaged_by="seed",
            )
            db.add(sample1)
            db.add(sample2)
            db.commit()
            print("Seeded 2 complaints.")
        else:
            print(f"Database already has {count} complaints. Skipping seed to ensure idempotency.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
