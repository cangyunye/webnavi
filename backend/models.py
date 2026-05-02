from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, SmallInteger
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
