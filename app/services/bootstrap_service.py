from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.auth import hash_password
from app.models import User
from app.utils.logger_config import app_logger as logger


DEFAULT_SUPERUSERS = (
    {
        "email": "admin@gmail.com",
        "role":"ADMIN",
        "username": "admin",
        "mobile_number": "+10000000001",
        "password": "admin",
    },
    {
        "email": "superadmin@gmail.com",
        "username": "superadmin",
        "role":"SUPER_ADMIN",
        "mobile_number": "+10000000002",
        "password": "superadmin",
    },
)


def ensure_default_superusers(db: Session) -> dict[str, int]:
    created_count = 0
    skipped_count = 0

    try:
        for default_user in DEFAULT_SUPERUSERS:
            existing_by_email = (
                db.query(User)
                .filter(User.email == default_user["email"])
                .first()
            )
            if existing_by_email:
                skipped_count += 1
                logger.info(
                    "Skipping default superuser because email already exists: %s",
                    default_user["email"],
                )
                continue

            existing_by_mobile = (
                db.query(User)
                .filter(User.mobile_number == default_user["mobile_number"])
                .first()
            )
            if existing_by_mobile:
                skipped_count += 1
                logger.warning(
                    "Skipping default superuser %s because mobile number %s is already in use",
                    default_user["email"],
                    default_user["mobile_number"],
                )
                continue

            db.add(
                User(
                    email=default_user["email"],
                    username=default_user["username"],
                    mobile_number=default_user["mobile_number"],
                    hashed_password=hash_password(default_user["password"]),
                    role="ADMIN",
                    is_active=True,
                    is_superuser=True,
                    is_email_verified=True,
                    email_verified_at=datetime.now(timezone.utc),
                )
            )
            created_count += 1
            logger.info(
                "Queued default superuser for creation: %s",
                default_user["email"],
            )

        if created_count:
            db.commit()
            logger.info("Created %s default superuser(s)", created_count)
    except Exception:
        db.rollback()
        logger.exception("Failed to ensure default superusers")
        raise

    return {
        "created": created_count,
        "skipped": skipped_count,
    }
