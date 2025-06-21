from app.database import engine
from app.models import property, user
from sqlalchemy import text

try:
    with engine.connect() as conn:
        conn.execute(text('SELECT 1'))
    print('Database connection successful')
except Exception as e:
    print(f'Database connection failed: {e}')