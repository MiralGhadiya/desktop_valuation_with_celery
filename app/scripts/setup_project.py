# app/scripts/setup_project.py

import csv
from getpass import getpass

from dotenv import dotenv_values, load_dotenv
from sqlalchemy.orm import Session

from app.auth import pwd_context
from app.database.db import SessionLocal
from app.models import User
from app.models.country import Country
from app.models.subscription_settings import SubscriptionSettings
from app.models.system_config import SystemConfig
from app.utils.logger_config import app_logger as logger
from app.utils.phone import get_country_from_mobile


load_dotenv()


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

        db.add(SystemConfig(
            config_key=key,
            config_value=value
        ))

        logger.info(f"Inserted config: {key}")


def import_countries(db: Session, csv_path: str):
    try:
        existing_dial_codes = {
            dial_code
            for (dial_code,) in db.query(Country.dial_code).all()
            if dial_code
        }
        pending_dial_codes = set()

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                dial_code = row.get("dial_code", "").strip()
                existing = (
                    db.query(Country)
                    .filter(Country.country_code == row["country_code"])
                    .first()
                )

                if existing:
                    print(f"Skipping existing country: {row['country_code']}")
                    continue

                if dial_code and (
                    dial_code in existing_dial_codes
                    or dial_code in pending_dial_codes
                ):
                    print(
                        f"Skipping duplicate dial code {dial_code} "
                        f"for country {row['country_code']}"
                    )
                    continue

                country = Country(
                    name=row["name"].strip(),
                    country_code=row["country_code"].strip(),
                    dial_code=dial_code,
                    currency_code=row.get("currency_code", "").strip() or None,
                )

                db.add(country)
                if dial_code:
                    pending_dial_codes.add(dial_code)

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
        subscription_duration_days=365
    )

    db.add(settings)

    print("Subscription settings created (365 days)")


def create_superuser(db: Session):
    print("\n=== Create Superuser ===")

    email = input("Email: ").strip().lower()
    username = input("Username: ").strip()
    mobile_number = input("Mobile number (with country code): ").strip()

    password = getpass("Password: ")
    confirm_password = getpass("Confirm Password: ")

    if password != confirm_password:
        print("Passwords do not match")
        return

    if db.query(User).filter(User.email == email).first():
        print("Email already exists")
        return

    if db.query(User).filter(User.mobile_number == mobile_number).first():
        print("Mobile number already exists")
        return

    dial_code, country_code = get_country_from_mobile(mobile_number)

    country = db.query(Country).filter(
        Country.dial_code == dial_code
    ).first()

    if not country:
        print(f"Country not found for dial code {dial_code}")
        return

    user = User(
        email=email,
        username=username,
        mobile_number=mobile_number,
        country_id=country.id,
        hashed_password=pwd_context.hash(password),
        is_active=True,
        is_superuser=True,
        is_email_verified=True,
    )

    db.add(user)

    print("Superuser created")


def run_setup():
    db: Session = SessionLocal()

    try:
        print("Running project setup...")

        import_env_variables(db)
        import_countries(db, "data - data.csv.csv")
        setup_subscription_settings(db)

        db.commit()

        create_superuser(db)

        db.commit()

        print("\nSetup completed successfully!")

    except Exception as e:
        db.rollback()
        print("Setup failed:", str(e))

    finally:
        db.close()


if __name__ == "__main__":
    run_setup()
