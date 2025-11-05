from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from bson import ObjectId
import bcrypt
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List
import motor.motor_asyncio

load_dotenv()

app = FastAPI(title="Finance Manager API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client.financeapp


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    name: str
    email: str


class TransactionCreate(BaseModel):
    description: str
    amount: float
    type: str
    category_id: Optional[str] = None


class CategoryResponse(BaseModel):
    id: str
    name: str
    type: str
    color: str


SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 43200


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


async def get_current_user(token: str = Depends(lambda: "")):
    if not token:
        raise HTTPException(status_code=401, detail="Token não fornecido")
    payload = await verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    return payload


@app.post("/api/register", response_model=dict)
async def register(user_data: UserCreate):
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), bcrypt.gensalt())

    user = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password.decode('utf-8'),
        "currency": "BRL",
        "created_at": datetime.utcnow()
    }

    result = await db.users.insert_one(user)

    default_categories = [
        {"name": "Salário", "type": "income", "color": "#22c55e", "user_id": str(result.inserted_id)},
        {"name": "Freelance", "type": "income", "color": "#16a34a", "user_id": str(result.inserted_id)},
        {"name": "Investimentos", "type": "income", "color": "#15803d", "user_id": str(result.inserted_id)},
        {"name": "Alimentação", "type": "expense", "color": "#ef4444", "user_id": str(result.inserted_id)},
        {"name": "Transporte", "type": "expense", "color": "#f59e0b", "user_id": str(result.inserted_id)},
        {"name": "Moradia", "type": "expense", "color": "#8b5cf6", "user_id": str(result.inserted_id)},
        {"name": "Lazer", "type": "expense", "color": "#ec4899", "user_id": str(result.inserted_id)},
        {"name": "Saúde", "type": "expense", "color": "#06b6d4", "user_id": str(result.inserted_id)},
        {"name": "Educação", "type": "expense", "color": "#84cc16", "user_id": str(result.inserted_id)}
    ]

    await db.categories.insert_many(default_categories)

    token = await create_access_token({"user_id": str(result.inserted_id)})

    return {
        "token": token,
        "user": {
            "id": str(result.inserted_id),
            "name": user_data.name,
            "email": user_data.email
        }
    }


@app.post("/api/login", response_model=dict)
async def login(user_data: UserCreate):
    user = await db.users.find_one({"email": user_data.email})
    if not user:
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    if not bcrypt.checkpw(user_data.password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = await create_access_token({"user_id": str(user["_id"])})

    return {
        "token": token,
        "user": {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }
    }


@app.get("/api/transactions")
async def get_transactions(
        page: int = 1,
        limit: int = 50,
        type: Optional[str] = None,
        current_user: dict = Depends(get_current_user)
):
    skip = (page - 1) * limit

    filter_query = {"user_id": current_user["user_id"]}
    if type:
        filter_query["type"] = type

    transactions = await db.transactions.find(filter_query).sort("date", -1).skip(skip).limit(limit).to_list(limit)
    total = await db.transactions.count_documents(filter_query)

    for transaction in transactions:
        transaction["id"] = str(transaction["_id"])
        if "category_id" in transaction and transaction["category_id"]:
            category = await db.categories.find_one({"_id": ObjectId(transaction["category_id"])})
            transaction["category"] = {
                "id": str(category["_id"]),
                "name": category["name"],
                "color": category["color"]
            } if category else None

    return {
        "transactions": transactions,
        "total_pages": (total + limit - 1) // limit,
        "current_page": page,
        "total": total
    }


@app.post("/api/transactions", response_model=dict)
async def create_transaction(
        transaction_data: TransactionCreate,
        current_user: dict = Depends(get_current_user)
):
    transaction = {
        "description": transaction_data.description,
        "amount": transaction_data.amount,
        "type": transaction_data.type,
        "category_id": ObjectId(transaction_data.category_id) if transaction_data.category_id else None,
        "date": datetime.utcnow(),
        "user_id": current_user["user_id"],
        "created_at": datetime.utcnow()
    }

    result = await db.transactions.insert_one(transaction)
    transaction["id"] = str(result.inserted_id)

    if transaction["category_id"]:
        category = await db.categories.find_one({"_id": transaction["category_id"]})
        transaction["category"] = {
            "id": str(category["_id"]),
            "name": category["name"],
            "color": category["color"]
        } if category else None

    return transaction


@app.get("/api/categories")
async def get_categories(current_user: dict = Depends(get_current_user)):
    categories = await db.categories.find({"user_id": current_user["user_id"]}).to_list(1000)

    for category in categories:
        category["id"] = str(category["_id"])

    return categories


@app.get("/api/dashboard")
async def get_dashboard(current_user: dict = Depends(get_current_user)):
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    pipeline_month = [
        {
            "$match": {
                "user_id": current_user["user_id"],
                "date": {
                    "$gte": datetime(current_year, current_month, 1),
                    "$lt": datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(
                        current_year + 1, 1, 1)
                }
            }
        },
        {
            "$group": {
                "_id": "$type",
                "total": {"$sum": "$amount"}
            }
        }
    ]

    month_summary = await db.transactions.aggregate(pipeline_month).to_list(length=None)

    pipeline_categories = [
        {
            "$match": {
                "user_id": current_user["user_id"],
                "type": "expense",
                "date": {
                    "$gte": datetime(current_year, current_month, 1),
                    "$lt": datetime(current_year, current_month + 1, 1) if current_month < 12 else datetime(
                        current_year + 1, 1, 1)
                }
            }
        },
        {
            "$group": {
                "_id": "$category_id",
                "total": {"$sum": "$amount"}
            }
        }
    ]

    category_spending = await db.transactions.aggregate(pipeline_categories).to_list(length=None)

    for item in category_spending:
        if item["_id"]:
            category = await db.categories.find_one({"_id": item["_id"]})
            item["category"] = {
                "id": str(category["_id"]),
                "name": category["name"],
                "color": category["color"]
            } if category else None

    pipeline_balance = [
        {
            "$match": {"user_id": current_user["user_id"]}
        },
        {
            "$group": {
                "_id": None,
                "income": {"$sum": {"$cond": [{"$eq": ["$type", "income"]}, "$amount", 0]}},
                "expense": {"$sum": {"$cond": [{"$eq": ["$type", "expense"]}, "$amount", 0]}}
            }
        }
    ]

    balance_result = await db.transactions.aggregate(pipeline_balance).to_list(length=None)
    balance = balance_result[0]["income"] - balance_result[0]["expense"] if balance_result else 0

    return {
        "balance": balance,
        "month_summary": month_summary,
        "category_spending": category_spending,
        "current_month": current_month,
        "current_year": current_year
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)