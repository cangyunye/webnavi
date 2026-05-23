from fastapi import APIRouter, Depends, HTTPException, Header, Query, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime

from database import get_db
from models import Node, User, ApiKey
from schemas import NodeCreate, NodeResponse, APIResponse
from deps import get_current_user_from_api_key_or_jwt, log_api_key_usage

router = APIRouter(prefix="/api/v1/nodes", tags=["节点管理"])


@router.get("", response_model=APIResponse)
async def list_nodes(
    request: Request,
    name: Optional[str] = Query(None, description="按名称过滤"),
    group: Optional[str] = Query(None, description="按分组过滤"),
    label: Optional[str] = Query(None, description="按标签过滤"),
    status: Optional[str] = Query(None, description="按状态过滤 (active/inactive)"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(100, ge=1, le=1000, description="每页数量"),
    auth_result: tuple = Depends(get_current_user_from_api_key_or_jwt),
    db: Session = Depends(get_db)
):
    user, api_key = auth_result
    
    # 权限检查
    if user.role == "guest":
        raise HTTPException(
            status_code=401,
            detail="请先登录或使用有效的 API Key"
        )
    
    query = db.query(Node)

    if name:
        query = query.filter(Node.name.ilike(f"%{name}%"))
    if group:
        query = query.filter(Node.groups.contains([group]))
    if label:
        query = query.filter(Node.labels.contains(label))
    if status:
        query = query.filter(Node.status == status)

    total = query.count()
    start = (page - 1) * page_size
    items = query.offset(start).limit(page_size).all()

    response = APIResponse(
        code=0,
        message="success",
        data={
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [NodeResponse.model_validate(item).model_dump() for item in items]
        }
    )
    
    # 记录日志
    if api_key:
        await log_api_key_usage(request, api_key, user, 200, db)
    
    return response


@router.get("/{node_id}", response_model=APIResponse)
async def get_node(
    request: Request,
    node_id: str,
    auth_result: tuple = Depends(get_current_user_from_api_key_or_jwt),
    db: Session = Depends(get_db)
):
    user, api_key = auth_result
    
    if user.role == "guest":
        raise HTTPException(
            status_code=401,
            detail="请先登录或使用有效的 API Key"
        )

    node = db.query(Node).filter(Node.id == node_id).first()
    if not node:
        if api_key:
            await log_api_key_usage(request, api_key, user, 404, db)
        raise HTTPException(status_code=404, detail="节点不存在")

    response = APIResponse(
        code=0,
        message="success",
        data=NodeResponse.model_validate(node).model_dump()
    )
    
    if api_key:
        await log_api_key_usage(request, api_key, user, 200, db)
    
    return response


@router.post("", response_model=APIResponse)
async def create_node(
    request: Request,
    node: NodeCreate,
    auth_result: tuple = Depends(get_current_user_from_api_key_or_jwt),
    db: Session = Depends(get_db)
):
    user, api_key = auth_result
    
    if user.role == "guest":
        raise HTTPException(
            status_code=401,
            detail="请先登录或使用有效的 API Key"
        )

    if db.query(Node).filter(Node.id == node.id).first():
        if api_key:
            await log_api_key_usage(request, api_key, user, 400, db)
        raise HTTPException(status_code=400, detail="节点已存在")

    db_node = Node(
        id=node.id,
        name=node.name,
        hostname=node.hostname,
        address=node.address,
        port=node.port,
        user=node.user,
        status=node.status,
        groups=node.groups,
        labels=node.labels,
        ssh_key=node.ssh_key,
        ssh_password=node.ssh_password,
        proxy_jump=node.proxy_jump,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_node)
    db.commit()
    db.refresh(db_node)

    response = APIResponse(
        code=0,
        message="success",
        data=NodeResponse.model_validate(db_node).model_dump()
    )
    
    if api_key:
        await log_api_key_usage(request, api_key, user, 200, db)
    
    return response


@router.put("/{node_id}", response_model=APIResponse)
async def update_node(
    request: Request,
    node_id: str,
    node: NodeCreate,
    auth_result: tuple = Depends(get_current_user_from_api_key_or_jwt),
    db: Session = Depends(get_db)
):
    user, api_key = auth_result
    
    if user.role == "guest":
        raise HTTPException(
            status_code=401,
            detail="请先登录或使用有效的 API Key"
        )

    db_node = db.query(Node).filter(Node.id == node_id).first()
    if not db_node:
        if api_key:
            await log_api_key_usage(request, api_key, user, 404, db)
        raise HTTPException(status_code=404, detail="节点不存在")

    db_node.name = node.name
    db_node.hostname = node.hostname
    db_node.address = node.address
    db_node.port = node.port
    db_node.user = node.user
    db_node.status = node.status
    db_node.groups = node.groups
    db_node.labels = node.labels
    db_node.ssh_key = node.ssh_key
    db_node.ssh_password = node.ssh_password
    db_node.proxy_jump = node.proxy_jump
    db_node.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_node)

    response = APIResponse(
        code=0,
        message="success",
        data=NodeResponse.model_validate(db_node).model_dump()
    )
    
    if api_key:
        await log_api_key_usage(request, api_key, user, 200, db)
    
    return response


@router.delete("/{node_id}", response_model=APIResponse)
async def delete_node(
    request: Request,
    node_id: str,
    auth_result: tuple = Depends(get_current_user_from_api_key_or_jwt),
    db: Session = Depends(get_db)
):
    user, api_key = auth_result
    
    if user.role == "guest":
        raise HTTPException(
            status_code=401,
            detail="请先登录或使用有效的 API Key"
        )

    node = db.query(Node).filter(Node.id == node_id).first()
    if not node:
        if api_key:
            await log_api_key_usage(request, api_key, user, 404, db)
        raise HTTPException(status_code=404, detail="节点不存在")

    db.delete(node)
    db.commit()

    response = APIResponse(
        code=0,
        message="success",
        data=None
    )
    
    if api_key:
        await log_api_key_usage(request, api_key, user, 200, db)
    
    return response
