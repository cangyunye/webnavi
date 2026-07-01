from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ResourceTheme, Resource, EnumItem, User
from schemas import ResourceThemeUpdate, ResourceThemeResponse
from deps import get_current_user

router = APIRouter(prefix="/api/resource-themes", tags=["资源主题"])


@router.put("/{resource_id}", response_model=ResourceThemeResponse)
def update_resource_theme(
    resource_id: int,
    body: ResourceThemeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="权限不足")

    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="资源未找到")

    valid_themes = db.query(EnumItem.enum_value).filter(
        EnumItem.enum_type == "resource_theme",
        EnumItem.is_active == 1
    ).all()
    valid_keys = [t[0] for t in valid_themes]

    if body.theme_key not in valid_keys:
        raise HTTPException(status_code=400, detail="无效的主题")

    if body.theme_key == "default":
        db.query(ResourceTheme).filter(ResourceTheme.resource_id == resource_id).delete()
        db.commit()
        return ResourceThemeResponse(
            resource_id=resource_id,
            theme_key="default"
        )

    existing = db.query(ResourceTheme).filter(ResourceTheme.resource_id == resource_id).first()
    if existing:
        existing.theme_key = body.theme_key
    else:
        existing = ResourceTheme(resource_id=resource_id, theme_key=body.theme_key)
        db.add(existing)

    db.commit()
    db.refresh(existing)
    return ResourceThemeResponse.model_validate(existing)
