from src.database.engine import SessionLocal


async def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
