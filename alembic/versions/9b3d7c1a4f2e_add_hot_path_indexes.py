"""add hot path indexes

Revision ID: 9b3d7c1a4f2e
Revises: 858bf3c04b71
Create Date: 2026-03-25 20:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "9b3d7c1a4f2e"
down_revision: Union[str, Sequence[str], None] = "858bf3c04b71"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

INDEX_DEFINITIONS = [
    ("ix_valuation_reports_user_id", "valuation_reports", ["user_id"]),
    ("ix_valuation_reports_category", "valuation_reports", ["category"]),
    ("ix_valuation_reports_country_code", "valuation_reports", ["country_code"]),
    ("ix_valuation_reports_created_at", "valuation_reports", ["created_at"]),
    ("ix_valuation_reports_subscription_id", "valuation_reports", ["subscription_id"]),
    (
        "ix_valuation_reports_user_created_at",
        "valuation_reports",
        ["user_id", "created_at"],
    ),
    (
        "ix_valuation_reports_country_created_at",
        "valuation_reports",
        ["country_code", "created_at"],
    ),
    ("ix_valuation_jobs_user_id", "valuation_jobs", ["user_id"]),
    ("ix_valuation_jobs_subscription_id", "valuation_jobs", ["subscription_id"]),
    ("ix_valuation_jobs_country_code", "valuation_jobs", ["country_code"]),
    ("ix_valuation_jobs_status", "valuation_jobs", ["status"]),
    ("ix_valuation_jobs_valuation_id", "valuation_jobs", ["valuation_id"]),
    ("ix_valuation_jobs_created_at", "valuation_jobs", ["created_at"]),
    (
        "ix_valuation_jobs_user_created_at",
        "valuation_jobs",
        ["user_id", "created_at"],
    ),
    (
        "ix_valuation_jobs_status_created_at",
        "valuation_jobs",
        ["status", "created_at"],
    ),
    (
        "ix_subscription_plans_country_active",
        "subscription_plans",
        ["country_code", "is_active"],
    ),
    (
        "ix_user_subscriptions_user_active_window",
        "user_subscriptions",
        ["user_id", "is_active", "is_expired", "start_date", "end_date"],
    ),
    (
        "ix_user_subscriptions_pricing_country_code",
        "user_subscriptions",
        ["pricing_country_code"],
    ),
    (
        "ix_user_subscriptions_payment_status",
        "user_subscriptions",
        ["payment_status"],
    ),
    (
        "ix_user_subscriptions_start_date",
        "user_subscriptions",
        ["start_date"],
    ),
    (
        "ix_user_subscriptions_end_date",
        "user_subscriptions",
        ["end_date"],
    ),
    (
        "ix_user_subscriptions_active_expiry_window",
        "user_subscriptions",
        ["is_active", "is_expired", "end_date"],
    ),
    (
        "ix_user_subscriptions_ip_country_code",
        "user_subscriptions",
        ["ip_country_code"],
    ),
    (
        "ix_user_subscriptions_payment_country_code",
        "user_subscriptions",
        ["payment_country_code"],
    ),
    ("ix_feedback_user_id", "feedback", ["user_id"]),
    ("ix_feedback_valuation_id", "feedback", ["valuation_id"]),
    ("ix_feedback_subscription_id", "feedback", ["subscription_id"]),
    ("ix_feedback_status", "feedback", ["status"]),
    ("ix_feedback_created_at", "feedback", ["created_at"]),
    ("ix_feedback_user_created_at", "feedback", ["user_id", "created_at"]),
    ("ix_feedback_status_created_at", "feedback", ["status", "created_at"]),
]


def upgrade() -> None:
    for index_name, table_name, columns in INDEX_DEFINITIONS:
        with op.get_context().autocommit_block():
            op.create_index(
                index_name,
                table_name,
                columns,
                unique=False,
                postgresql_concurrently=True,
            )


def downgrade() -> None:
    for index_name, table_name, _ in reversed(INDEX_DEFINITIONS):
        with op.get_context().autocommit_block():
            op.drop_index(
                index_name,
                table_name=table_name,
                postgresql_concurrently=True,
            )
