import json
from typing import Optional
from psycopg2.extensions import cursor
from jax.geneweaver.db import sql
from jax.geneweaver.core.schema import User


def get_user(db: cursor, user_id: int) -> Optional[User]:
    sql.user.get_by_id(db, user_id)
    result = db.fetchone()

    if not result:
        return None

    return User(**result)


def get_user_preferences(db: cursor, user_id: int) -> Optional[dict]:
    user = get_user(db, user_id)
    if user:
        return json.loads(user.prefs)
    return None
