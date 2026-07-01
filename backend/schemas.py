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
    theme_key: Optional[str] = None
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
    status: str = "online"
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
    status: str = "online"
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


class UserResponse(UserBase):
    id: int
    role: str
    is_active: int
    can_edit: bool = False
    can_delete: bool = False
    create_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserRoleUpdate(BaseModel):
    role: str


class UserStatusUpdate(BaseModel):
    is_active: int


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    user_id: Optional[int] = None


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


class NodeBase(BaseModel):
    name: str
    hostname: Optional[str] = ""
    address: str
    port: int = 22
    user: str = "root"
    status: str = "active"
    groups: List[str] = []
    labels: dict = {}
    ssh_key: Optional[str] = ""
    ssh_password: Optional[str] = ""
    proxy_jump: Optional[str] = ""


class NodeCreate(NodeBase):
    id: str


class NodeResponse(NodeBase):
    id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NodeListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[NodeResponse]


class APIResponse(BaseModel):
    code: int
    message: str
    data: Optional[dict] = None


class ApiKeyBase(BaseModel):
    key_name: str
    scopes: Optional[List[str]] = []
    expires_at: Optional[datetime] = None


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKeyResponse(ApiKeyBase):
    id: int
    key_prefix: str
    is_active: int
    last_used_at: Optional[datetime] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class ApiKeyCreateResponse(ApiKeyResponse):
    api_key: str  # 仅在创建时返回完整的 API Key


class ApiKeyLogBase(BaseModel):
    endpoint: str
    method: str
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    request_body: Optional[dict] = None
    response_status: Optional[int] = None


class ApiKeyLogCreate(ApiKeyLogBase):
    api_key_id: int
    user_id: int


class ApiKeyLogResponse(ApiKeyLogBase):
    id: int
    api_key_id: int
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class EnumItemBase(BaseModel):
    enum_value: Optional[str] = None
    enum_label: Optional[str] = None
    description: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[int] = None
    color: Optional[str] = None
    icon: Optional[str] = None


class EnumItemCreate(EnumItemBase):
    enum_type: str
    enum_value: str
    enum_label: str


class EnumItemResponse(EnumItemBase):
    id: int
    enum_type: str
    enum_value: str
    enum_label: str
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class ResourceThemeUpdate(BaseModel):
    theme_key: str


class ResourceThemeResponse(BaseModel):
    resource_id: int
    theme_key: str
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True
