from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from database import get_db
from models import EnumItem, User
from schemas import EnumItemBase, EnumItemCreate, EnumItemResponse
from deps import get_current_user

router = APIRouter(prefix="/api/enum-items", tags=["枚举管理"])


@router.get("", response_model=List[EnumItemResponse])
def get_enum_items(
    enum_type: Optional[str] = Query(None, description="按类型过滤"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取枚举项列表"""
    query = db.query(EnumItem)
    
    if enum_type:
        query = query.filter(EnumItem.enum_type == enum_type)
    
    items = query.filter(EnumItem.is_active == 1)\
                 .order_by(EnumItem.sort_order, EnumItem.id)\
                 .all()
    
    return [EnumItemResponse.model_validate(item) for item in items]


@router.get("/types", response_model=List[str])
def get_enum_types(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取所有枚举类型"""
    types = db.query(EnumItem.enum_type)\
              .distinct()\
              .order_by(EnumItem.enum_type)\
              .all()
    
    return [t[0] for t in types]


@router.get("/{enum_type}/options", response_model=List[dict])
def get_enum_options(
    enum_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定类型的枚举选项（用于下拉菜单）"""
    items = db.query(EnumItem)\
              .filter(EnumItem.enum_type == enum_type)\
              .filter(EnumItem.is_active == 1)\
              .order_by(EnumItem.sort_order, EnumItem.id)\
              .all()
    
    return [{"value": item.enum_value, "label": item.enum_label} for item in items]


@router.get("/{enum_type}/options-full", response_model=List[dict])
def get_enum_options_full(
    enum_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取指定类型的完整枚举选项（包含颜色、图标等）"""
    items = db.query(EnumItem)\
              .filter(EnumItem.enum_type == enum_type)\
              .filter(EnumItem.is_active == 1)\
              .order_by(EnumItem.sort_order, EnumItem.id)\
              .all()
    
    return [{
        "value": item.enum_value,
        "label": item.enum_label,
        "color": item.color,
        "icon": item.icon,
        "description": item.description
    } for item in items]


@router.post("", response_model=EnumItemResponse)
def create_enum_item(
    item: EnumItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建枚举项（仅管理员）"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 检查是否已存在
    existing = db.query(EnumItem).filter(
        EnumItem.enum_type == item.enum_type,
        EnumItem.enum_value == item.enum_value
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="该枚举值已存在")
    
    db_item = EnumItem(
        enum_type=item.enum_type,
        enum_value=item.enum_value,
        enum_label=item.enum_label,
        description=item.description,
        sort_order=item.sort_order or 0,
        is_active=item.is_active or 1,
        color=item.color,
        icon=item.icon
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    return EnumItemResponse.model_validate(db_item)


@router.put("/{item_id}", response_model=EnumItemResponse)
def update_enum_item(
    item_id: int,
    item: EnumItemBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新枚举项（仅管理员）"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="权限不足")
    
    db_item = db.query(EnumItem).filter(EnumItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="枚举项不存在")
    
    # 检查新值是否与其他值冲突
    if item.enum_value and item.enum_value != db_item.enum_value:
        existing = db.query(EnumItem).filter(
            EnumItem.enum_type == db_item.enum_type,
            EnumItem.enum_value == item.enum_value,
            EnumItem.id != item_id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="该枚举值已存在")
    
    if item.enum_value:
        db_item.enum_value = item.enum_value
    if item.enum_label:
        db_item.enum_label = item.enum_label
    if item.description is not None:
        db_item.description = item.description
    if item.sort_order is not None:
        db_item.sort_order = item.sort_order
    if item.is_active is not None:
        db_item.is_active = item.is_active
    if item.color is not None:
        db_item.color = item.color
    if item.icon is not None:
        db_item.icon = item.icon
    
    db.commit()
    db.refresh(db_item)
    
    return EnumItemResponse.model_validate(db_item)


@router.delete("/{item_id}")
def delete_enum_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除枚举项（仅管理员）"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="权限不足")
    
    db_item = db.query(EnumItem).filter(EnumItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="枚举项不存在")
    
    db.delete(db_item)
    db.commit()
    
    return {"message": "删除成功"}


@router.post("/{enum_type}/reorder")
def reorder_enum_items(
    enum_type: str,
    item_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """重新排序指定类型的枚举项（仅管理员）"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="权限不足")
    
    for index, item_id in enumerate(item_ids):
        db_item = db.query(EnumItem).filter(EnumItem.id == item_id).first()
        if db_item and db_item.enum_type == enum_type:
            db_item.sort_order = index
            db.commit()
    
    return {"message": "排序成功"}
