from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db

from app.models.user import User
from app.models.queue import Queue
from app.models.token import Token

from app.schemas import (
    UserOut,
    UserAuth,
    TokenSchema,
    QueueCreate,
    QueueUpdate,
    QueueOut,
    JoinQueueRequest,
    CustomerJoinRequest,
    TokenOut,
    TokenStatusUpdate,
    DashboardStats
)

from app.services.token_service import generate_token_number

from app.utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

app = FastAPI(
    title="Smart Queue Management System",
    description="Queue Management System with JWT Authentication, Priority Queue Processing, Token Tracking and Analytics Dashboard",
    version="1.0.0"
)


@app.on_event("startup")
def prepare_database():
    Base.metadata.create_all(bind=engine)

    if engine.dialect.name != "postgresql":
        return

    migration_statements = [
        "ALTER TABLE queues ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'ACTIVE'",
        "ALTER TABLE queues ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE tokens ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
        "UPDATE queues SET status = 'ACTIVE' WHERE status IS NULL",
        "UPDATE queues SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL",
        "UPDATE tokens SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL",
        "UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL"
    ]

    with engine.begin() as connection:
        for statement in migration_statements:
            connection.execute(text(statement))


# =========================
# USER APIs
# =========================

@app.post(
    "/signup",
    summary="Create new user",
    tags=["Authentication"],
    response_model=UserOut
)
async def create_user(
    data: UserAuth,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    hashed_password = get_hashed_password(
        data.password
    )

    new_user = User(
        name=data.username,
        email=data.email,
        password_hash=hashed_password,
        role=data.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserOut(
        id=new_user.id,
        username=new_user.name,
        email=new_user.email,
        role=new_user.role
    )


@app.post(
    "/login",
    summary="Create access and refresh tokens for user",
    tags=["Authentication"],
    response_model=TokenSchema
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    if not verify_password(
        form_data.password,
        user.password_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
        "token_type": "bearer",
        "username": user.name,
        "email": user.email,
        "role": user.role
    }


@app.get(
    "/users",
    tags=["Users"],
    response_model=list[UserOut]
)
async def get_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
        UserOut(
            id=user.id,
            username=user.name,
            email=user.email,
            role=user.role
        )
        for user in users
    ]


# =========================
# QUEUE APIs
# =========================

@app.post(
    "/queues",
    tags=["Queues"],
    summary="Create a new queue",
    response_model=QueueOut
)
async def create_queue(
    queue: QueueCreate,
    db: Session = Depends(get_db)
):
    new_queue = Queue(
        name=queue.name,
        description=queue.description,
        status=queue.status.upper()
    )

    db.add(new_queue)
    db.commit()
    db.refresh(new_queue)

    return new_queue


@app.get(
    "/queues",
    tags=["Queues"],
    summary="Get all queues",
    response_model=list[QueueOut]
)
async def get_queues(
    db: Session = Depends(get_db)
):
    return db.query(Queue).all()


@app.get(
    "/queues/{queue_id}",
    tags=["Queues"],
    summary="Get a specific queue by ID",
    response_model=QueueOut
)
async def get_queue(
    queue_id: int,
    db: Session = Depends(get_db)
):
    queue = db.query(Queue).filter(
        Queue.id == queue_id
    ).first()

    if not queue:
        raise HTTPException(
            status_code=404,
            detail="Queue not found"
        )

    return queue


@app.put(
    "/queues/{queue_id}",
    tags=["Queues"],
    summary="Update a queue",
    response_model=QueueOut
)
async def update_queue(
    queue_id: int,
    data: QueueUpdate,
    db: Session = Depends(get_db)
):
    queue = db.query(Queue).filter(
        Queue.id == queue_id
    ).first()

    if not queue:
        raise HTTPException(
            status_code=404,
            detail="Queue not found"
        )

    if data.name is not None:
        queue.name = data.name

    if data.description is not None:
        queue.description = data.description

    if data.status is not None:
        queue.status = data.status.upper()

    db.commit()
    db.refresh(queue)

    return queue


@app.delete(
    "/queues/{queue_id}",
    tags=["Queues"],
    summary="Delete a queue"
)
async def delete_queue(
    queue_id: int,
    db: Session = Depends(get_db)
):
    queue = db.query(Queue).filter(
        Queue.id == queue_id
    ).first()

    if not queue:
        raise HTTPException(
            status_code=404,
            detail="Queue not found"
        )

    db.query(Token).filter(
        Token.queue_id == queue_id
    ).delete()

    db.delete(queue)
    db.commit()

    return {
        "message": "Queue deleted successfully"
    }


# =========================
# TOKEN APIs
# =========================

@app.post(
    "/queues/{queue_id}/join",
    tags=["Queues"],
    summary="Join a queue and generate a token",
    response_model=TokenOut
)
async def join_queue(
    queue_id: int,
    request: JoinQueueRequest,
    db: Session = Depends(get_db)
):
    queue = db.query(Queue).filter(
        Queue.id == queue_id
    ).first()

    if not queue:
        raise HTTPException(
            status_code=404,
            detail="Queue not found"
        )

    user = db.query(User).filter(
        User.id == request.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    last_token = (
        db.query(Token)
        .filter(Token.queue_id == queue_id)
        .order_by(Token.id.desc())
        .first()
    )

    last_token_number = (
        last_token.token_number
        if last_token
        else None
    )

    token_number = generate_token_number(
        last_token_number
    )

    token = Token(
        token_number=token_number,
        queue_id=queue_id,
        user_id=request.user_id,
        priority_level=request.priority_level,
        status="WAITING"
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return token


@app.post(
    "/queues/{queue_id}/join-customer",
    tags=["Queues"],
    summary="Create or find a customer and join a queue",
    response_model=TokenOut
)
async def join_queue_customer(
    queue_id: int,
    request: CustomerJoinRequest,
    db: Session = Depends(get_db)
):
    queue = db.query(Queue).filter(
        Queue.id == queue_id
    ).first()

    if not queue:
        raise HTTPException(
            status_code=404,
            detail="Queue not found"
        )

    user = db.query(User).filter(
        User.email == request.email
    ).first()

    if not user:
        user = User(
            name=request.customer_name,
            email=request.email,
            password_hash=get_hashed_password("customer-entry"),
            role="customer"
        )

        db.add(user)
        db.commit()
        db.refresh(user)

    last_token = (
        db.query(Token)
        .filter(Token.queue_id == queue_id)
        .order_by(Token.id.desc())
        .first()
    )

    last_token_number = (
        last_token.token_number
        if last_token
        else None
    )

    token_number = generate_token_number(
        last_token_number
    )

    token = Token(
        token_number=token_number,
        queue_id=queue_id,
        user_id=user.id,
        priority_level=request.priority_level,
        status="WAITING"
    )

    db.add(token)
    db.commit()
    db.refresh(token)

    return token


@app.get(
    "/tokens",
    tags=["Tokens"],
    summary="Get all tokens",
    response_model=list[TokenOut]
)
def get_tokens(
    db: Session = Depends(get_db)
):
    return (
        db.query(Token)
        .order_by(Token.id.desc())
        .all()
    )


@app.get(
    "/tokens/{token_id}",
    tags=["Tokens"],
    summary="Get a specific token by ID",
    response_model=TokenOut
)
def get_token(
    token_id: int,
    db: Session = Depends(get_db)
):
    token = db.query(Token).filter(
        Token.id == token_id
    ).first()

    if not token:
        raise HTTPException(
            status_code=404,
            detail="Token not found"
        )

    return token


@app.get(
    "/queues/{queue_id}/tokens",
    tags=["Tokens"],
    summary="Get all tokens in a specific queue",
    response_model=list[TokenOut]
)
def get_queue_tokens(
    queue_id: int,
    db: Session = Depends(get_db)
):
    queue = db.query(Queue).filter(
        Queue.id == queue_id
    ).first()

    if not queue:
        raise HTTPException(
            status_code=404,
            detail="Queue not found"
        )

    return (
        db.query(Token)
        .filter(Token.queue_id == queue_id)
        .order_by(Token.id)
        .all()
    )


@app.post(
    "/queues/{queue_id}/call-next",
    tags=["Tokens"],
    summary="Call the next token in the queue",
    response_model=TokenOut
)
def call_next_token(
    queue_id: int,
    db: Session = Depends(get_db)
):
    next_token = (
        db.query(Token)
        .filter(
            Token.queue_id == queue_id,
            Token.status == "WAITING"
        )
        .order_by(
            Token.priority_level.desc(),
            Token.created_at.asc()
        )
        .first()
    )

    if not next_token:
        raise HTTPException(
            status_code=404,
            detail="No waiting tokens found"
        )

    next_token.status = "CALLED"

    db.commit()
    db.refresh(next_token)

    return next_token


@app.put(
    "/tokens/{token_id}/status",
    tags=["Tokens"],
    response_model=TokenOut
)
def update_token_status(
    token_id: int,
    data: TokenStatusUpdate,
    db: Session = Depends(get_db)
):
    token = db.query(Token).filter(
        Token.id == token_id
    ).first()

    if not token:
        raise HTTPException(
            status_code=404,
            detail="Token not found"
        )

    token.status = data.status

    db.commit()
    db.refresh(token)

    return token


# =========================
# ANALYTICS APIs
# =========================

@app.get(
    "/analytics/dashboard",
    tags=["Analytics"],
    summary="Get analytics dashboard data",
    response_model=DashboardStats
)
def analytics_dashboard(
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()

    total_queues = db.query(Queue).count()

    total_tokens = db.query(Token).count()

    completed_tokens = (
        db.query(Token)
        .filter(Token.status == "COMPLETED")
        .count()
    )

    active_tokens = (
        db.query(Token)
        .filter(Token.status != "COMPLETED")
        .count()
    )

    return {
        "total_users": total_users,
        "total_queues": total_queues,
        "total_tokens": total_tokens,
        "completed_tokens": completed_tokens,
        "active_tokens": active_tokens
    }
