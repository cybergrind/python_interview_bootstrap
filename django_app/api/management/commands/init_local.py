import os

from django.core.management.base import BaseCommand

from tipsi_tools.unix import succ


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        succ(
            f'echo create database {os.environ.get("PGDATABASE", "django_app")} | '
            'psql -Upostgres -h postgres postgres'
        )
        succ('./manage.py makemigrations')
        succ('./manage.py migrate')
