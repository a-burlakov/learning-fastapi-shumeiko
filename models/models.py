from datetime import datetime

import sqlalchemy
from sqlalchemy import (
    MetaData,
    String,
    Integer,
    TIMESTAMP,
    ForeignKey,
    Table,
    Column,
    JSON,
)

metadata = MetaData()

roles = Table(
    "roles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow, nullable=False),
    Column("role_id", Integer, ForeignKey("roles.id")),
)

# engine = sqlalchemy.create_engine(DATABASER_URL)
# metadata.create_all(engine)
