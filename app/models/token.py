from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Token(Base):
    __tablename__ = "tokens"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    token_number = Column(
        String(10),
        nullable=False
    )

    queue_id = Column(
        Integer,
        ForeignKey("queues.id")
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    priority_level = Column(
        Integer,
        default=1
    )

    status = Column(
        String(20),
        default="WAITING"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    queue = relationship("Queue")
    user = relationship("User")