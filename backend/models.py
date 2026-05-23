from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    icon = Column(String(100), nullable=False)
    sort_order = Column(Integer, default=0)
    create_time = Column(DateTime, server_default=func.now())

    resources = relationship("Resource", back_populates="category")


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    name = Column(String(100), nullable=False)
    url = Column(String(500), nullable=False)
    description = Column(Text)
    status = Column(SmallInteger, default=1)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    category = relationship("Category", back_populates="resources")


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("organizations.id"))
    create_time = Column(DateTime, server_default=func.now())

    parent = relationship("Organization", remote_side=[id], backref="children")
    owners = relationship("Owner", back_populates="organization")


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100))
    phone = Column(String(20))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    create_time = Column(DateTime, server_default=func.now())

    organization = relationship("Organization", back_populates="owners")


class DevMachine(Base):
    __tablename__ = "dev_machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    ip = Column(String(50), nullable=False)
    port = Column(Integer, default=22)
    hostname = Column(String(100))
    cpu = Column(String(50))
    memory = Column(String(50))
    disk = Column(String(100))
    os = Column(String(100))
    status = Column(SmallInteger, default=1)
    environment = Column(String(50), default="dev")
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    create_time = Column(DateTime, server_default=func.now())

    owner = relationship("Owner", foreign_keys=[owner_id])
    organization = relationship("Organization", foreign_keys=[organization_id])


class DbInstance(Base):
    __tablename__ = "db_instances"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    db_type = Column(String(50), nullable=False)
    version = Column(String(50))
    ip = Column(String(50), nullable=False)
    port = Column(Integer, default=3306)
    charset = Column(String(20), default="utf8mb4")
    status = Column(SmallInteger, default=1)
    environment = Column(String(50), default="dev")
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    create_time = Column(DateTime, server_default=func.now())

    owner = relationship("Owner", foreign_keys=[owner_id])
    organization = relationship("Organization", foreign_keys=[organization_id])


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    password_hash = Column(String(255))
    role = Column(String(20), default="guest")
    is_active = Column(SmallInteger, default=1)
    can_edit = Column(SmallInteger, default=0)
    can_delete = Column(SmallInteger, default=0)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    permissions = relationship("UserPermission", back_populates="user")


class UserPermission(Base):
    __tablename__ = "user_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))
    permission_type = Column(String(20), default="view")
    create_time = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="permissions")


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    resource_type = Column(String(50), nullable=False)
    resource_id = Column(Integer, nullable=False)
    username = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    description = Column(Text)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Node(Base):
    __tablename__ = "nodes"

    id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    hostname = Column(String(100))
    address = Column(String(50), nullable=False)
    port = Column(Integer, default=22)
    user = Column(String(50), default="root")
    status = Column(String(20), default="active")
    groups = Column(JSON, default=[])
    labels = Column(JSON, default={})
    ssh_key = Column(String(500))
    ssh_password = Column(String(255))
    proxy_jump = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ApiKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    key_name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False)
    key_prefix = Column(String(20), nullable=False)
    scopes = Column(JSON, default=[])
    is_active = Column(SmallInteger, default=1)
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User")


class ApiKeyLog(Base):
    __tablename__ = "api_key_logs"

    id = Column(Integer, primary_key=True, index=True)
    api_key_id = Column(Integer, ForeignKey("api_keys.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    endpoint = Column(String(500), nullable=False)
    method = Column(String(20), nullable=False)
    ip_address = Column(String(100))
    user_agent = Column(String(500))
    request_body = Column(JSON)
    response_status = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

    api_key = relationship("ApiKey")
    user = relationship("User")


class EnumItem(Base):
    __tablename__ = "enum_items"

    id = Column(Integer, primary_key=True, index=True)
    enum_type = Column(String(50), nullable=False, index=True)
    enum_value = Column(String(50), nullable=False)
    enum_label = Column(String(100), nullable=False)
    description = Column(String(200))
    sort_order = Column(Integer, default=0)
    is_active = Column(SmallInteger, default=1)
    color = Column(String(20))
    icon = Column(String(50))
    create_time = Column(DateTime, server_default=func.now())
    update_time = Column(DateTime, server_default=func.now(), onupdate=func.now())