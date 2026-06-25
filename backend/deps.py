from datetime import datetime, timedelta
from typing import Optional, Tuple
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import bcrypt
import secrets
import hashlib
from sqlalchemy.orm import Session

from config import settings
from database import get_db
from models import User, ApiKey, ApiKeyLog
from schemas import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


def generate_api_key() -> Tuple[str, str, str]:
    """生成 API Key，返回 (完整 key, 前缀, 哈希值)"""
    random_part = secrets.token_hex(20)
    prefix = f"sk_{random_part[:8]}"
    full_key = f"{prefix}_{random_part[8:]}"
    key_hash = bcrypt.hashpw(full_key.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    return full_key, prefix, key_hash


def verify_api_key(api_key: str, key_hash: str) -> bool:
    """验证 API Key"""
    return bcrypt.checkpw(api_key.encode('utf-8'), key_hash.encode('utf-8'))


def get_api_key_from_request(request: Request) -> Optional[str]:
    """从请求中获取 API Key"""
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]
    return None


async def get_current_user_from_api_key_or_jwt(
    request: Request,
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Tuple[Optional[User], Optional[ApiKey]]:
    """
    支持两种认证方式：
    1. API Key (Bearer)
    2. JWT Token (Bearer)
    返回 (user, api_key)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 首先尝试从请求获取 API Key
    api_key_str = get_api_key_from_request(request)
    if api_key_str:
        # 查找对应的 API Key
        api_key = db.query(ApiKey).filter(
            ApiKey.is_active == 1
        ).all()
        
        for ak in api_key:
            if verify_api_key(api_key_str, ak.key_hash):
                # 检查是否过期
                if ak.expires_at and ak.expires_at < datetime.utcnow():
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="API Key 已过期"
                    )
                
                # 更新最后使用时间
                ak.last_used_at = datetime.utcnow()
                db.commit()
                
                user = db.query(User).filter(User.id == ak.user_id).first()
                if not user or not user.is_active:
                    raise credentials_exception
                return user, ak
        
        # 如果没有匹配的 API Key，尝试 JWT
        pass

    # 尝试 JWT 认证
    if token:
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: int = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        if not user.is_active:
            raise HTTPException(status_code=400, detail="用户已被禁用")
        return user, None
    
    # 没有认证信息，返回访客用户
    return get_guest_user(db), None


async def log_api_key_usage(
    request: Request,
    api_key: ApiKey,
    user: User,
    response_status: int,
    db: Session
):
    """记录 API Key 使用日志"""
    request_body = None
    try:
        if hasattr(request.state, "body"):
            request_body = request.state.body
    except:
        pass
    
    log = ApiKeyLog(
        api_key_id=api_key.id,
        user_id=user.id,
        endpoint=str(request.url.path),
        method=request.method,
        ip_address=request.client.host if request.client else None,
        user_agent=request.headers.get("User-Agent"),
        request_body=request_body,
        response_status=response_status
    )
    db.add(log)
    db.commit()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_guest_user(db: Session) -> User:
    guest = User(
        id=0,
        username="guest",
        role="guest",
        is_active=1
    )
    return guest


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        return get_guest_user(db)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.user_id).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已被禁用")
    return user


def check_permission(user: User, category_id: Optional[int] = None) -> bool:
    if user.role == "admin":
        return True
    if user.role in ("learning_mentor", "ops_expert"):
        return True
    public_categories = ["学习", "AI", "软件资源", "测试", "工具"]
    if user.role in ("guest", "registered"):
        if category_id:
            from models import Category
            from database import SessionLocal
            db = SessionLocal()
            try:
                category = db.query(Category).filter(Category.id == category_id).first()
                db.close()
                if category and category.name in public_categories:
                    return True
            finally:
                db.close()
        return False
    return False
