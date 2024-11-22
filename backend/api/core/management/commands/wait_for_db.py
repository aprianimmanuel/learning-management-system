"""Django command to wait for the database to be available."""

from __future__ import annotations

import socket
import time
from typing import Any

import psycopg2
import redis
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to wait for the database to be available."""

    def handle(
        self,
        *args,
        **options,
    ) -> None:
        """To override the handle method to wait for the database to be available."""
        self.stdout.write("Waiting for database...")
        self.wait_for_service(
            "database",
            self.check_db,
            {},
            wait_time=1,
            max_retries=30,
        )
        self.stdout.write(self.style.SUCCESS("Database available!"))

        if settings.USE_REDIS_FOR_CACHE:
            self.stdout.write("Waiting for Redis...")
            self.wait_for_service(
                "redis",
                self.check_redis,
                {},
                wait_time=1,
                max_retries=30,
            )
            self.stdout.write(self.style.SUCCESS("Redis available!"))
        
        self.wait_for_service(
            "RabbitMQ",
            self.check_rabbitmq,
            {},
            wait_time=1,
            max_retries=30,
        )
        self.stdout.write(self.style.SUCCESS("RabbitMQ available!"))
    
    def wait_for_service(
        self,
        service_name: str,
        check_function: Any,
        check_kwargs: dict[str, Any],
        wait_time: int,
        max_retries: int,
    ) -> None:
        """To wait for a service to be available."""
        self.stdout.write(f"Waiting for {service_name}...")
        retries = 0
        while retries < max_retries:
            try:
                check_function(**check_kwargs)
                self.stdout.write(self.style.SUCCESS(f"{service_name} available!"))
                return
            except Exception as e:  # noqa: BLE001
                self.stdout.write(
                    self.stdout.write(
                        f"{service_name} is not available. Retrying in {wait_time} seconds..."
                    )
                )
                self.stdout.write(str(e))
                time.sleep(wait_time)
                retries += 1

        msg = f"Failed to connect to {service_name} after {max_retries} retries."
        raise Exception(msg)  # noqa: TRY002

    def check_db(self) -> None:
        """To check if the database is available."""
        self.stdout.write("Checking database connection...")
        try:
            db_conn = connections["default"]
            db_conn.cursor()
        except OperationalError as e:
            if "pgbouncer" in str(e):
                self.check_pgbouncer()
            else:
                raise

    def check_pgbouncer(self) -> None:
        """To check if pgbouncer is available."""
        self.stdout.write("Checking PGBouncer....")
        conn = psycopg2.connect(
            dbname=settings.DATABASE["default"]["NAME"],
            user=settings.DATABASE["default"]["USER"],
            password=settings.DATABASE["default"]["PASSWORD"],
            host=settings.DATABASE["default"]["HOST"],
            port=settings.DATABASE["default"]["PORT"],
        )
        conn.close()
    
    def check_redis(self) -> None:
        """To check if Redis is available."""
        client = redis.StrictRedis(
            host=settings.CACHE["default"]["HOST"],
            port=settings.CACHE["default"]["PORT"],
            db=0,
            password=settings.CACHE["default"]["PASSWORD"],
        )
        client.ping()

    def check_rabbitmq(self) -> None:
        """To check if RabbitMQ is available."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((settings.RABBITMQ["default"]["HOST"], settings.RABBITMQ["default"]["PORT"]))
        sock.close()
