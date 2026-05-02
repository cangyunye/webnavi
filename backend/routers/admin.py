from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
import bcrypt

from database import get_db
from models import User, UserPermission, Category, Credential, DevMachine, DbInstance
from schemas import (
    UserResponse,
    UserWithPermissions,
    UserPermissionCreate,
    UserPermissionResponse,
    UserPermissionInfo,
    UserRoleUpdate,
    UserStatusUpdate,
    UserCategoryPermissionsUpdate,
    UserActionPermissionsUpdate,
    UserCreate,
    CredentialCreate,
    CredentialUpdate,
    CredentialResponse
)
from deps import get_current_user

router = APIRouter(prefix="/api/admin", tags=["用户管理"])


async def get_current_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="仅管理员可以访问此接口"
        )
    return current_user


def get_resource_name(db: Session, resource_type: str, resource_id: int) -> str:
    if resource_type == "dev_machine":
        machine = db.query(DevMachine).filter(DevMachine.id == resource_id).first()
        return machine.name if machine else f"机器{resource_id}"
    elif resource_type == "db_instance":
        instance = db.query(DbInstance).filter(DbInstance.id == resource_id).first()
        return instance.name if instance else f"数据库{resource_id}"
    return ""


def build_user_with_permissions(db: Session, user: User) -> UserWithPermissions:
    permissions = []
    for perm in user.permissions:
        category = db.query(Category).filter(Category.id == perm.category_id).first()
        if category:
            permissions.append(UserPermissionInfo(
                category_id=perm.category_id,
                category_name=category.name,
                permission_type=perm.permission_type
            ))

    return UserWithPermissions(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        can_edit=bool(user.can_edit),
        can_delete=bool(user.can_delete),
        permissions=permissions,
        create_time=user.create_time
    )


@router.get("/users", response_model=List[UserWithPermissions])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    users = db.query(User).filter(User.id != 0).order_by(User.id.desc()).all()
    return [build_user_with_permissions(db, u) for u in users]


@router.get("/users/{user_id}", response_model=UserWithPermissions)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return build_user_with_permissions(db, user)


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    if role_data.role not in ["guest", "registered", "admin"]:
        raise HTTPException(status_code=400, detail="无效的角色")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    user.role = role_data.role
    db.commit()
    return {"message": "角色更新成功"}


@router.put("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    status_data: UserStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    user.is_active = status_data.is_active
    db.commit()
    return {"message": "状态更新成功"}


@router.put("/users/{user_id}/categories")
def update_user_categories(
    user_id: int,
    perm_data: UserCategoryPermissionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    db.query(UserPermission).filter(UserPermission.user_id == user_id).delete()

    for item in perm_data.category_permissions:
        if item.enabled:
            category = db.query(Category).filter(Category.id == item.category_id).first()
            if category:
                perm = UserPermission(
                    user_id=user_id,
                    category_id=item.category_id,
                    permission_type="view"
                )
                db.add(perm)

    db.commit()
    return {"message": "分类权限更新成功"}


@router.put("/users/{user_id}/actions")
def update_user_actions(
    user_id: int,
    action_data: UserActionPermissionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    user.can_edit = 1 if action_data.can_edit else 0
    user.can_delete = 1 if action_data.can_delete else 0
    db.commit()
    return {"message": "操作权限更新成功"}


class ResetPasswordRequest(BaseModel):
    password: str


@router.post("/users/{user_id}/reset-password")
def reset_user_password(
    user_id: int,
    password_data: ResetPasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    if len(password_data.password) < 6:
        raise HTTPException(status_code=400, detail="密码长度至少6位")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    user.password_hash = bcrypt.hashpw(password_data.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    db.commit()
    return {"message": "密码重置成功"}


@router.get("/users/{user_id}/permissions", response_model=List[UserPermissionResponse])
def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    permissions = db.query(UserPermission).filter(UserPermission.user_id == user_id).all()
    return permissions


@router.post("/users/{user_id}/permissions", response_model=UserPermissionResponse)
def add_user_permission(
    user_id: int,
    permission_data: UserPermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")

    if permission_data.category_id:
        category = db.query(Category).filter(Category.id == permission_data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="分类未找到")

    db_permission = UserPermission(
        user_id=user_id,
        category_id=permission_data.category_id,
        permission_type=permission_data.permission_type
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission


@router.delete("/users/{user_id}/permissions/{permission_id}")
def delete_user_permission(
    user_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    permission = db.query(UserPermission).filter(
        UserPermission.id == permission_id,
        UserPermission.user_id == user_id
    ).first()
    if not permission:
        raise HTTPException(status_code=404, detail="权限未找到")

    db.delete(permission)
    db.commit()
    return {"message": "权限删除成功"}


@router.get("/credentials", response_model=List[CredentialResponse])
def get_credentials(
    resource_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    query = db.query(Credential)
    if resource_type:
        query = query.filter(Credential.resource_type == resource_type)
    credentials = query.order_by(Credential.id.desc()).all()

    result = []
    for cred in credentials:
        res = CredentialResponse(
            id=cred.id,
            resource_type=cred.resource_type,
            resource_id=cred.resource_id,
            username=cred.username,
            password=cred.password,
            description=cred.description,
            resource_name=get_resource_name(db, cred.resource_type, cred.resource_id),
            create_time=cred.create_time,
            update_time=cred.update_time
        )
        result.append(res)
    return result


@router.get("/credentials/{cred_id}", response_model=CredentialResponse)
def get_credential(
    cred_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    cred = db.query(Credential).filter(Credential.id == cred_id).first()
    if not cred:
        raise HTTPException(status_code=404, detail="凭据未找到")

    return CredentialResponse(
        id=cred.id,
        resource_type=cred.resource_type,
        resource_id=cred.resource_id,
        username=cred.username,
        password=cred.password,
        description=cred.description,
        resource_name=get_resource_name(db, cred.resource_type, cred.resource_id),
        create_time=cred.create_time,
        update_time=cred.update_time
    )


@router.post("/credentials", response_model=CredentialResponse)
def create_credential(
    cred_data: CredentialCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    db_cred = Credential(
        resource_type=cred_data.resource_type,
        resource_id=cred_data.resource_id,
        username=cred_data.username,
        password=cred_data.password,
        description=cred_data.description
    )
    db.add(db_cred)
    db.commit()
    db.refresh(db_cred)

    return CredentialResponse(
        id=db_cred.id,
        resource_type=db_cred.resource_type,
        resource_id=db_cred.resource_id,
        username=db_cred.username,
        password=db_cred.password,
        description=db_cred.description,
        resource_name=get_resource_name(db, db_cred.resource_type, db_cred.resource_id),
        create_time=db_cred.create_time,
        update_time=db_cred.update_time
    )


@router.put("/credentials/{cred_id}", response_model=CredentialResponse)
def update_credential(
    cred_id: int,
    cred_data: CredentialUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    cred = db.query(Credential).filter(Credential.id == cred_id).first()
    if not cred:
        raise HTTPException(status_code=404, detail="凭据未找到")

    update_data = cred_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cred, field, value)

    db.commit()
    db.refresh(cred)

    return CredentialResponse(
        id=cred.id,
        resource_type=cred.resource_type,
        resource_id=cred.resource_id,
        username=cred.username,
        password=cred.password,
        description=cred.description,
        resource_name=get_resource_name(db, cred.resource_type, cred.resource_id),
        create_time=cred.create_time,
        update_time=cred.update_time
    )


@router.delete("/credentials/{cred_id}")
def delete_credential(
    cred_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    cred = db.query(Credential).filter(Credential.id == cred_id).first()
    if not cred:
        raise HTTPException(status_code=404, detail="凭据未找到")

    db.delete(cred)
    db.commit()
    return {"message": "凭据删除成功"}
