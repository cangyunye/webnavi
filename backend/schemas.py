from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional, List


class CategoryBase(BaseModel):
    name: str
    icon: str


class CategoryResponse(CategoryBase):
    id: int
    sort_order: int
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResourceBase(BaseModel):
    name: str
    url: str
    description: Optional[str] = None
    status: int = 1


class ResourceCreate(ResourceBase):
    category_id: int


class ResourceResponse(ResourceBase):
    id: int
    category_id: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class OrganizationResponse(OrganizationBase):
    id: int
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class OwnerBase(BaseModel):
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    organization_id: Optional[int] = None


class OwnerResponse(OwnerBase):
    id: int
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class OwnerWithOrgName(OwnerResponse):
    organization_name: Optional[str] = None


class DevMachineBase(BaseModel):
    name: str
    ip: str
    port: int = 22
    hostname: Optional[str] = None
    cpu: Optional[str] = None
    memory: Optional[str] = None
    disk: Optional[str] = None
    os: Optional[str] = None
    status: int = 1
    environment: str = "dev"
    description: Optional[str] = None


class DevMachineCreate(DevMachineBase):
    owner_id: Optional[int] = None
    organization_id: Optional[int] = None


class DevMachineResponse(DevMachineBase):
    id: int
    owner_id: Optional[int] = None
    organization_id: Optional[int] = None
    owner_name: Optional[str] = None
    organization_name: Optional[str] = None
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class DbInstanceBase(BaseModel):
    name: str
    db_type: str
    version: Optional[str] = None
    ip: str
    port: int = 3306
    charset: str = "utf8mb4"
    status: int = 1
    environment: str = "dev"
    description: Optional[str] = None


class DbInstanceCreate(DbInstanceBase):
    owner_id: Optional[int] = None
    organization_id: Optional[int] = None


class DbInstanceResponse(DbInstanceBase):
    id: int
    owner_id: Optional[int] = None
    organization_id: Optional[int] = None
    owner_name: Optional[str] = None
    organization_name: Optional[str] = None
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None


class UserCreate(UserBase):
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码长度至少为6位')
        return v


class UserLogin(BaseModel):
    username: str
    password: str


class UserPermissionInfo(BaseModel):
    category_id: int
    category_name: str
    permission_type: str

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    id: int
    role: str
    is_active: int
    can_edit: bool = False
    can_delete: bool = False
    permissions: List[UserPermissionInfo] = []
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserWithPermissions(UserResponse):
    pass

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role: str


class UserStatusUpdate(BaseModel):
    is_active: int


class CategoryPermissionItem(BaseModel):
    category_id: int
    enabled: bool = True


class UserCategoryPermissionsUpdate(BaseModel):
    category_permissions: List[CategoryPermissionItem]


class UserActionPermissionsUpdate(BaseModel):
    can_edit: bool = False
    can_delete: bool = False


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserPermissionBase(BaseModel):
    category_id: Optional[int] = None
    permission_type: str = "view"


class UserPermissionCreate(UserPermissionBase):
    pass


class UserPermissionResponse(UserPermissionBase):
    id: int
    user_id: int
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class CredentialBase(BaseModel):
    resource_type: str
    resource_id: int
    username: str
    password: str
    description: Optional[str] = None


class CredentialCreate(CredentialBase):
    pass


class CredentialUpdate(BaseModel):
    resource_type: Optional[str] = None
    resource_id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    description: Optional[str] = None


class CredentialResponse(CredentialBase):
    id: int
    resource_name: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True
