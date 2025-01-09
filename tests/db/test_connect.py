from sqlalchemy import text


async def test_get_session(db):
    result = await db.execute(text("SELECT 1"))

    for row in result:
        assert row[0] == 1
