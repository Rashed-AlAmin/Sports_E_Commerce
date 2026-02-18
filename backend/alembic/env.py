import os
import asyncio
from logging.config import fileConfig
from sqlalchemy import  pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from dotenv import load_dotenv
from backend.models import CartItem, Order, OrderItem, Product, User, Cart
# 1. Import your Base
from backend.db.base import Base

# 2. Load the .env file
load_dotenv(".env")

# this is the Alembic Config object
config = context.config

# 3. Get the DATABASE_URL from environment and inject it into Alembic config
database_url = os.getenv("DATABASE_URL")

# Neon/Heroku fix: SQLAlchemy requires 'postgresql://' not 'postgres://'
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

if database_url:
    config.set_main_option("sqlalchemy.url", database_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode using an Async Engine."""
    
    # Get the config
    configuration = config.get_section(config.config_ini_section)
    
    # Create an Async Engine
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async def do_run_migrations():
        async with connectable.connect() as connection:
            # We use 'run_sync' because Alembic's migration context is synchronous
            await connection.run_sync(do_run_migrations_sync)

    def do_run_migrations_sync(connection):
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
    asyncio.run(do_run_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()



# alembic -c backend/alembic.ini revision --autogenerate -m "initial_migration"
# alembic -c backend/alembic.ini stamp head
# alembic -c backend/alembic.ini revision --autogenerate -m "remove_test_column"
# alembic -c backend/alembic.ini upgrade head