from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Queue(Base):
    __tablename__ = "queues"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    description = Column(
        String(255),
        nullable=True
    )

    status = Column(
        String(20),
        default="active"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )