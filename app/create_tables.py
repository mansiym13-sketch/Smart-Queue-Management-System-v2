from app.database import Base, engine

from app.models.user import User
from app.models.queue import Queue
from app.models.token import Token

Base.metadata.create_all(bind=engine)

print("All tables created successfully!")