import uvicorn
import os
from fastapi import FastAPI, Header, Depends, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, BeforeValidator, PlainSerializer, EmailStr
from typing import Optional, Annotated, List  # <<< 1. ADICIONADO 'List'
from contextlib import asynccontextmanager
import motor.motor_asyncio
from bson import ObjectId
from datetime import datetime, timedelta, timezone

# --- Bibliotecas de Segurança ---
from passlib.context import CryptContext
from jose import JWTError, jwt


# --- 1. Definição dos Modelos de Dados (Validação) ---

# Helper de ObjectId para Pydantic v2
def validate_object_id(v):
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    ObjectId,
    BeforeValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str)
]


# Modelos de Despesa
class Despesa(BaseModel):
    valor: float
    descricao: str
    categoria: str


class DespesaInDB(Despesa):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    usuario_id: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


# Modelo de Conta
class Conta(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    usuario_id: str
    saldo: float
    moeda: str = "BRL"

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


# Modelos para Usuário e Token
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserInDB(BaseModel):
    id: PyObjectId = Field(default_factory=ObjectId, alias="_id")
    email: EmailStr
    hashed_password: str

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True


class Token(BaseModel):
    access_token: str
    token_type: str


# --- 2. Configuração de Segurança e Conexão ---

# Carrega a Chave da API (para comunicação segura entre serviços)
SECRET_API_KEY = os.environ.get("MINHA_API_SECRET_KEY")
if not SECRET_API_KEY:
    raise Exception("Variável de ambiente 'MINHA_API_SECRET_KEY' não definida.")

# Carrega os detalhes do MongoDB
MONGO_DETAILS = os.environ.get("MONGO_DETAILS")
if not MONGO_DETAILS:
    raise Exception("Variável de ambiente 'MONGO_DETAILS' não definida.")

# Configuração de Segurança JWT e Hashing
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise Exception("Variável de ambiente 'JWT_SECRET_KEY' não definida.")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- 3. Funções Helper de Segurança ---

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- 4. Função de Dependência (Segurança JWT) ---

async def get_current_user(
        request: Request,
        token: str = Header(None, alias="Authorization")
):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorização ausente",
        )
    try:
        scheme, token_value = token.split()
        if scheme.lower() != "bearer":
            raise ValueError
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato do token inválido (esperado: 'Bearer [token]')",
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token_value, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db = request.app.state.db
    user = await db.usuarios.find_one({"_id": ObjectId(user_id)})
    if user is None:
        raise credentials_exception
    return user_id


# --- 5. Ciclo de Vida da Aplicação (Conexão com DB) ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Conectando ao MongoDB...")
    app.state.mongodb_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
    app.state.db = app.state.mongodb_client.meu_financeiro
    await app.state.db.usuarios.create_index("email", unique=True)
    print("Conectado com sucesso!")
    yield
    print("Fechando conexão com o MongoDB...")
    app.state.mongodb_client.close()
    print("Conexão fechada.")


# --- 6. Criação da Aplicação FastAPI ---
app = FastAPI(
    title="Minha API Financeira",
    description="API para o chatbot financeiro se conectar ao sistema.",
    version="1.0.0",
    lifespan=lifespan
)

# --- 7. Configuração do CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 8. Função de Segurança Antiga (API Key) ---
async def check_api_key(x_api_key: str = Header(None)):
    if x_api_key != SECRET_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave de API (X-API-Key) inválida ou ausente"
        )
    return True


# --- 9. Definição dos Endpoints (Rotas) ---

@app.get("/")
async def root():
    return {"message": "API Financeira está online e conectada ao MongoDB!"}


# Endpoint de Registro
@app.post("/api/v1/register", response_model=UserInDB)
async def register_user(
        user_data: UserCreate,
        request: Request,
        is_auth: bool = Depends(check_api_key)  # Protegido pela API Key
):
    db = request.app.state.db
    existing_user = await db.usuarios.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Um usuário com este email já existe",
        )
    hashed_password = hash_password(user_data.password)
    new_user_data = {
        "email": user_data.email,
        "hashed_password": hashed_password
    }
    insert_result = await db.usuarios.insert_one(new_user_data)
    created_user = await db.usuarios.find_one({"_id": insert_result.inserted_id})
    return UserInDB.model_validate(created_user)


# Endpoint de Login
@app.post("/api/v1/login", response_model=Token)
async def login_for_access_token(
        user_credentials: UserCreate,
        request: Request,
        is_auth: bool = Depends(check_api_key)  # Protegido pela API Key
):
    db = request.app.state.db
    user = await db.usuarios.find_one({"email": user_credentials.email})
    if not user or not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    user_id = str(user["_id"])
    access_token = create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Endpoint de Saldo (Protegido por JWT)
@app.get("/api/v1/saldo", response_model=Conta)
async def get_saldo_endpoint(
        request: Request,
        current_user_id: str = Depends(get_current_user)
):
    db = request.app.state.db
    conta = await db.contas.find_one({"usuario_id": current_user_id})
    if conta:
        return Conta.model_validate(conta)

    # Se não houver conta, cria uma nova
    nova_conta_doc = {
        "usuario_id": current_user_id,
        "saldo": 0.0,
        "moeda": "BRL"
    }
    await db.contas.insert_one(nova_conta_doc)
    nova_conta = await db.contas.find_one({"usuario_id": current_user_id})
    return Conta.model_validate(nova_conta)


# --- 2. <<< CORREÇÃO AQUI: ADICIONADO O ENDPOINT 'GET' PARA DESPESAS ---
@app.get("/api/v1/despesas", response_model=List[DespesaInDB])
async def get_despesas_endpoint(
        request: Request,
        current_user_id: str = Depends(get_current_user)
):
    """
    Busca TODAS as despesas do usuário logado.
    """
    db = request.app.state.db
    # find() retorna um cursor, convertemos para lista
    despesas_cursor = db.despesas.find({"usuario_id": current_user_id})
    # Definimos um limite, ex: 1000, para não sobrecarregar
    despesas_list = await despesas_cursor.to_list(length=1000)

    # O Pydantic validará a lista antes de retornar
    return despesas_list


# Endpoint de Despesas (POST)
@app.post("/api/v1/despesas", response_model=DespesaInDB)
async def adicionar_despesa_endpoint(
        despesa: Despesa,
        request: Request,
        current_user_id: str = Depends(get_current_user)
):
    """
    Cria uma nova despesa para o usuário logado.
    """
    db = request.app.state.db
    despesa_dict = despesa.model_dump()
    despesa_dict["usuario_id"] = current_user_id

    insert_result = await db.despesas.insert_one(despesa_dict)
    created_despesa = await db.despesas.find_one(
        {"_id": insert_result.inserted_id}
    )
    if created_despesa:
        return DespesaInDB.model_validate(created_despesa)

    raise HTTPException(status_code=500, detail="Erro ao salvar a despesa.")


# --- 10. Ponto de Entrada para Rodar ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)