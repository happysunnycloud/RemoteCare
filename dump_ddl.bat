@echo off

docker exec remotecare-postgres pg_isready -U remotecare -d remotecare >nul 2>&1
if errorlevel 1 (
    echo PostgreSQL is not available.
    pause
    exit /b 1
)

docker exec -t remotecare-postgres pg_dump ^
    -U remotecare ^
    -d remotecare ^
    --schema-only ^
    --no-owner > ddl\ddl.sql

if errorlevel 1 (
    echo Backup failed.
) else (
    echo Backup completed successfully.
)

pause