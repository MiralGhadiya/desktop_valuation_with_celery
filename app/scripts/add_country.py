import csv
from sqlalchemy.orm import Session

from app.database.db import SessionLocal
from app.models.country import Country


def import_countries(csv_path: str):
    db: Session = SessionLocal()

    try:
        with open(csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Skip if country_code already exists
                existing = (
                    db.query(Country)
                    .filter(Country.country_code == row["country_code"])
                    .first()
                )

                if existing:
                    print(f"Skipping existing country: {row['country_code']}")
                    continue

                country = Country(
                    name=row["name"].strip(),
                    country_code=row["country_code"].strip(),
                    dial_code=row.get("dial_code", "").strip(),
                    currency_code=row.get("currency_code", "").strip() or None,
                )

                db.add(country)

            db.commit()
            print("✅ Countries imported successfully!")

    except Exception as e:
        db.rollback()
        print("❌ Error importing countries:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    import_countries("data - data.csv.csv")