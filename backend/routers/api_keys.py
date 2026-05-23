from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import User, ApiKey, ApiKeyLog
from schemas import (
    ApiKeyCreate,
    ApiKeyResponse,
    ApiKeyCreateResponse,
    ApiKeyLogResponse
)
from deps import get_current_user, generate_api_key

router = APIRouter(prefix="/api/api-keys", tags=["API Key 管理"])


@router.get("", response_model=List[ApiKeyResponse])
def get_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取当前用户的所有 API Key"""
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户无法访问此功能"
        )
    
    api_keys = db.query(ApiKey).filter(
        ApiKey.user_id == current_user.id
    ).order_by(ApiKey.create_time.desc()).all()
    
    return [ApiKeyResponse.model_validate(ak) for ak in api_keys]


@router.post("", response_model=ApiKeyCreateResponse)
def create_api_key(
    key_data: ApiKeyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建新的 API Key"""
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户无法访问此功能"
        )
    
    full_key, prefix, key_hash = generate_api_key()
    
    api_key = ApiKey(
        user_id=current_user.id,
        key_name=key_data.key_name,
        key_hash=key_hash,
        key_prefix=prefix,
        scopes=key_data.scopes or [],
        expires_at=key_data.expires_at,
        is_active=1
    )
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    
    response = ApiKeyCreateResponse(
        id=api_key.id,
        key_name=api_key.key_name,
        key_prefix=api_key.key_prefix,
        scopes=api_key.scopes,
        expires_at=api_key.expires_at,
        is_active=api_key.is_active,
        last_used_at=api_key.last_used_at,
        create_time=api_key.create_time,
        update_time=api_key.update_time,
        api_key=full_key
    )
    
    return response


@router.delete("/{key_id}")
def delete_api_key(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除 API Key"""
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户无法访问此功能"
        )
    
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key 不存在")
    
    db.delete(api_key)
    db.commit()
    
    return {"message": "API Key 删除成功"}


@router.get("/{key_id}/logs", response_model=List[ApiKeyLogResponse])
def get_api_key_logs(
    key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取 API Key 使用日志"""
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户无法访问此功能"
        )
    
    # 确认 API Key 属于当前用户
    api_key = db.query(ApiKey).filter(
        ApiKey.id == key_id,
        ApiKey.user_id == current_user.id
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key 不存在")
    
    logs = db.query(ApiKeyLog).filter(
        ApiKeyLog.api_key_id == key_id
    ).order_by(ApiKeyLog.created_at.desc()).limit(100).all()
    
    return [ApiKeyLogResponse.model_validate(log) for log in logs]
