import csv

from dotenv import dotenv_values, load_dotenv
from sqlalchemy.orm import Session

from app.database.db import Base, SessionLocal, engine
from app.models.country import Country
from app.models.subscription_settings import SubscriptionSettings
from app.models.system_config import SystemConfig
from app.services.bootstrap_service import ensure_default_superusers
from app.utils.logger_config import app_logger as logger


load_dotenv()

# Ensure tables exist
Base.metadata.create_all(bind=engine)


def import_env_variables(db: Session):
    env_vars = dotenv_values(".env")

    for key, value in env_vars.items():
        if value is None:
            continue

        existing = db.query(SystemConfig).filter(
            SystemConfig.config_key == key
        ).first()

        if existing:
            logger.info(f"Skipping existing config: {key}")
            continue

        db.add(
            SystemConfig(
                config_key=key,
                config_value=value,
            )
        )

        logger.info(f"Inserted config: {key}")


def import_countries(db: Session, csv_path: str):
    try:
        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
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

        print("Countries imported")

    except Exception as e:
        raise Exception(f"Country import failed: {e}")


def setup_subscription_settings(db: Session):
    existing = db.query(SubscriptionSettings).first()

    if existing:
        print("Subscription settings already exist")
        return

    settings = SubscriptionSettings(
        id=1,
        subscription_duration_days=365,
    )

    db.add(settings)

    print("Subscription settings created (365 days)")


def run_setup():
    db: Session = SessionLocal()

    try:
        print("Running project setup...")

        import_env_variables(db)
        import_countries(db, "data - data.csv.csv")
        setup_subscription_settings(db)
        db.commit()

        result = ensure_default_superusers(db)
        print(
            "Default superusers ensured "
            f"(created={result['created']}, skipped={result['skipped']})"
        )

        print("\nSetup completed successfully!")

    except Exception as e:
        db.rollback()
        print("Setup failed:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    run_setup()
