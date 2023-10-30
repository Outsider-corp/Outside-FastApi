import datetime

from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON, UUID, \
    Boolean

metadata = MetaData()

role = Table(
    'role',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True, nullable=False),
    Column('role_name', String, nullable=False),
    Column('permissions', JSON)
)

user = Table(
    'user',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('username', String, nullable=False),
    Column('email', String, nullable=False),
    Column('hashed_password', String, nullable=False),
    Column('registered_at', TIMESTAMP, default=datetime.datetime.utcnow),
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=False, nullable=False),
    Column('is_verified', Boolean, default=False, nullable=False),
)

man = Table(
    'man',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False)
)
