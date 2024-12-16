from __future__ import with_statement
import sys
from os import path
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig

# Import the Flask app's config
from flask import current_app
from app import create_app, db

# Here we create a Flask app instance for the migrations
app = create_app()  # Assuming you have a function to create your app

# This will use the same config that Flask uses
app.config.from_object('config')  # Adjust this to load your actual config

# Automatically pull the SQLAlchemy URL from Flask config
config = context.config
config.set_main_option('sqlalchemy.url', app.config['SQLALCHEMY_DATABASE_URI'])

# Now proceed with the usual Alembic setup
fileConfig(config.config_file_name)
target_metadata = db.metadata

def run_migrations_online():
    # Create an engine that knows how to connect to your database
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    print("Running in offline mode")
else:
    run_migrations_online()
