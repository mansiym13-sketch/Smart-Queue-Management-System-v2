from pydantic import BaseModel, Field, EmailStr

class UserAuth(BaseModel):
    username: str
    email: str
    password: str
    role: str = "customer"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class QueueCreate(BaseModel):
    name: str
    description: str


class QueueOut(BaseModel):
    id: int
    name: str
    description: str
    status: str

    class Config:
        from_attributes = True


# ===== ADD THESE =====

class JoinQueueRequest(BaseModel):
    user_id: int
    priority_level: int = 1


class TokenOut(BaseModel):
    id: int
    token_number: str
    queue_id: int
    user_id: int
    priority_level: int
    status: str

    class Config:
        from_attributes = True

class TokenStatusUpdate(BaseModel):
    status: str

class DashboardStats(BaseModel):
    total_users: int
    total_queues: int
    total_tokens: int
    completed_tokens: int
    active_tokens: int