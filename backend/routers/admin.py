from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional
import bcrypt

from database import get_db
from models import User, Category, Credential, DevMachine, DbInstance
from schemas import (
    UserResponse,
    UserRoleUpdate,
    UserStatusUpdate,
    UserCreate,
    CredentialCreate,
    CredentialUpdate,
    CredentialResponse
)
from deps import get_current_user, get_password_hash


class AdminUserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    password: str
    role: str = "registered"


class UserActionPermissionsUpdate(BaseModel):
    can_edit: bool = False
    can_delete: bool = False

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


@router.get("/users", response_model=List[UserResponse])
def get_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    users = db.query(User).filter(User.id != 0).order_by(User.id.desc()).all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    return user


@router.put("/users/{user_id}/role")
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    if role_data.role not in ["guest", "registered", "learning_mentor", "ops_expert", "admin"]:
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


@router.put("/users/{user_id}/actions")
def update_user_actions(
    user_id: int,
    actions: UserActionPermissionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户未找到")
    user.can_edit = 1 if actions.can_edit else 0
    user.can_delete = 1 if actions.can_delete else 0
    db.commit()
    return {"message": "操作权限更新成功"}


@router.post("/users", response_model=UserResponse)
def admin_create_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    if user_data.role not in ["registered", "learning_mentor", "ops_expert", "admin"]:
        raise HTTPException(status_code=400, detail="无效的角色")

    if len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="密码长度至少为6位")

    existing = db.query(User).filter(User.username == user_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    if user_data.email:
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="邮箱已被使用")

    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
        role=user_data.role,
        is_active=1
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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
