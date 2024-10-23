# Generated by Django 4.2.11 on 2024-04-17 04:30

from django.contrib.sessions.models import Session
from django.db import connection, migrations, transaction
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from psycopg2.sql import SQL, Identifier

# This migration copies over data from existing sessions table "django_session"
# to the custom session table "zerver_realmsession" which is introduced in previous migration.

# Since "django_session" is a large table, we want to insert data as performantly as possible,
# the approach is simple: drop all indexes, copy over data and finally create back those indexes
# because creating an index on pre-existing data is quicker than updating it incrementally as each row is loaded.

# Note: Although we are modifying the schema, this file shouldn't be considered as a schema migration because
# eventually the schema doesn't change as the dropped indexes are created back.


def migrate_data_from_django_session_to_realmsession(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    # No need to do all of this if django_session table is empty.
    if not Session.objects.exists():
        return

    # [(index_name, index_definition),]
    indexes_tubles: list[tuple[str, str]] = []

    with transaction.atomic():
        cursor = connection.cursor()
        # Fetch indexes names and their definitions, excluding pk.
        # These definitions were used to create the indexes when the table was first created,
        # and will be used to create them back after copying over the data.
        cursor.execute(
            SQL(
                "SELECT indexname,indexdef FROM pg_indexes WHERE tablename = 'zerver_realmsession' AND indexname != 'zerver_realmsession_pkey' "
            )
        )
        indexes_tubles = cursor.fetchall()

        # Drop indexes.
        for index in indexes_tubles:
            cursor.execute(SQL("DROP INDEX {index_name}").format(index_name=Identifier(index[0])))

        # Copy over data.
        cursor.execute(SQL("INSERT INTO zerver_realmsession (SELECT * FROM django_session)"))

    # Create back indexes.
    cursor = connection.cursor()
    for index in indexes_tubles:
        cursor.execute(SQL(index[1]))

    # Finally, should we clear django_session table?
    # cursor.execute(SQL("TRUNCATE django_session"))


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("zerver", "0617_sessions_create_custom_model"),
    ]

    operations = [
        migrations.RunPython(migrate_data_from_django_session_to_realmsession),
    ]
