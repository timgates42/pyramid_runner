import alembic
import sqlalchemy as sa
import paste.deploy
import pyramid.paster

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = alembic.context.config
pyramid_config_file = config.get_main_option('pyramid_config_file')

# Interpret the config file for Python logging.
# This line sets up loggers basically.
# fileConfig(config.config_file_name)
pyramid.paster.setup_logging(pyramid_config_file)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
app = paste.deploy.loadapp('config:%s' % pyramid_config_file, relative_to='.')
settings = pyramid.paster.get_appsettings(pyramid_config_file)
target_metadata = __import__(app.registry.__name__).models.meta.Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.
    Calls to context.execute() here emit the given string to the
    script output.
    """
    alembic.context.configure(url=settings.get('sqlalchemy.url'))

    with alembic.context.begin_transaction():
        alembic.context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.
    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    engine = sa.engine_from_config(settings, 'sqlalchemy.')
    # engine = engine_from_config(
    #            config.get_section(config.config_ini_section),
    #            prefix='sqlalchemy.',
    #            poolclass=pool.NullPool)

    connection = engine.connect()
    alembic.context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with alembic.context.begin_transaction():
            alembic.context.run_migrations()
    finally:
        connection.close()

if alembic.context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
