from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from models import DevMachine, DbInstance, Resource, User, Organization, Owner, Category
from schemas import (
    DevMachineResponse,
    DevMachineCreate,
    DbInstanceResponse,
    DbInstanceCreate,
    ResourceResponse,
    ResourceCreate,
    OrganizationResponse,
    OwnerResponse,
    OwnerWithOrgName
)
from deps import get_current_user

router = APIRouter(prefix="/api", tags=["资源"])


def check_category_permission(current_user: User, category_name: str, db: Session):
    if current_user.role == "admin":
        return True
    
    if current_user.role == "guest":
        guest_categories = ["学习", "AI", "软件资源", "测试", "工具"]
        return category_name in guest_categories
    
    if current_user.role == "registered":
        if len(current_user.permissions) == 0:
            return True
        
        category = db.query(Category).filter(Category.name == category_name).first()
        if not category:
            return False
        
        for perm in current_user.permissions:
            if perm.category_id == category.id:
                return True
        return False
    
    return False


def machine_to_response(machine: DevMachine) -> DevMachineResponse:
    return DevMachineResponse(
        id=machine.id,
        name=machine.name,
        ip=machine.ip,
        port=machine.port,
        hostname=machine.hostname,
        cpu=machine.cpu,
        memory=machine.memory,
        disk=machine.disk,
        os=machine.os,
        status=machine.status,
        environment=machine.environment,
        description=machine.description,
        owner_id=machine.owner_id,
        organization_id=machine.organization_id,
        owner_name=machine.owner.username if machine.owner else None,
        organization_name=machine.organization.name if machine.organization else None,
        create_time=machine.create_time
    )


def instance_to_response(instance: DbInstance) -> DbInstanceResponse:
    return DbInstanceResponse(
        id=instance.id,
        name=instance.name,
        db_type=instance.db_type,
        version=instance.version,
        ip=instance.ip,
        port=instance.port,
        charset=instance.charset,
        status=instance.status,
        environment=instance.environment,
        description=instance.description,
        owner_id=instance.owner_id,
        organization_id=instance.organization_id,
        owner_name=instance.owner.username if instance.owner else None,
        organization_name=instance.organization.name if instance.organization else None,
        create_time=instance.create_time
    )


@router.get("/organizations", response_model=List[OrganizationResponse])
def get_organizations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户没有访问权限，请先登录"
        )
    organizations = db.query(Organization).order_by(Organization.id.asc()).all()
    return organizations


@router.get("/owners", response_model=List[OwnerWithOrgName])
def get_owners(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户没有访问权限，请先登录"
        )
    owners = db.query(Owner).order_by(Owner.id.asc()).all()
    result = []
    for owner in owners:
        result.append(OwnerWithOrgName(
            id=owner.id,
            username=owner.username,
            email=owner.email,
            phone=owner.phone,
            organization_id=owner.organization_id,
            organization_name=owner.organization.name if owner.organization else None,
            create_time=owner.create_time
        ))
    return result


@router.get("/owners/{owner_id}", response_model=OwnerWithOrgName)
def get_owner(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户没有访问权限，请先登录"
        )
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="责任人未找到")
    return OwnerWithOrgName(
        id=owner.id,
        username=owner.username,
        email=owner.email,
        phone=owner.phone,
        organization_id=owner.organization_id,
        organization_name=owner.organization.name if owner.organization else None,
        create_time=owner.create_time
    )


@router.get("/owners/{owner_id}/resources")
def get_owner_resources(
    owner_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户没有访问权限，请先登录"
        )
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="责任人未找到")

    machines = db.query(DevMachine).filter(DevMachine.owner_id == owner_id).all()
    instances = db.query(DbInstance).filter(DbInstance.owner_id == owner_id).all()

    return {
        "owner": {
            "id": owner.id,
            "username": owner.username,
            "email": owner.email,
            "phone": owner.phone,
            "organization_name": owner.organization.name if owner.organization else None
        },
        "dev_machines": [machine_to_response(m) for m in machines],
        "db_instances": [instance_to_response(i) for i in instances]
    }


@router.get("/dev-machines", response_model=List[DevMachineResponse])
def get_dev_machines(
    environment: Optional[str] = None,
    status: Optional[int] = None,
    owner_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not check_category_permission(current_user, "研发机器", db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有访问研发机器的权限"
        )

    query = db.query(DevMachine)

    if environment:
        query = query.filter(DevMachine.environment == environment)
    if status is not None:
        query = query.filter(DevMachine.status == status)
    if owner_id:
        query = query.filter(DevMachine.owner_id == owner_id)
    if organization_id:
        query = query.filter(DevMachine.organization_id == organization_id)

    machines = query.order_by(DevMachine.id.desc()).all()
    return [machine_to_response(m) for m in machines]


@router.get("/dev-machines/{machine_id}", response_model=DevMachineResponse)
def get_dev_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not check_category_permission(current_user, "研发机器", db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有访问研发机器的权限"
        )

    machine = db.query(DevMachine).filter(DevMachine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="服务器未找到")
    return machine_to_response(machine)


@router.get("/db-instances", response_model=List[DbInstanceResponse])
def get_db_instances(
    environment: Optional[str] = None,
    db_type: Optional[str] = None,
    status: Optional[int] = None,
    owner_id: Optional[int] = None,
    organization_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    if not check_category_permission(current_user, "数据库", db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有访问数据库的权限"
        )

    query = db.query(DbInstance)

    if environment:
        query = query.filter(DbInstance.environment == environment)
    if db_type:
        query = query.filter(DbInstance.db_type == db_type)
    if status is not None:
        query = query.filter(DbInstance.status == status)
    if owner_id:
        query = query.filter(DbInstance.owner_id == owner_id)
    if organization_id:
        query = query.filter(DbInstance.organization_id == organization_id)

    instances = query.order_by(DbInstance.id.desc()).all()
    return [instance_to_response(i) for i in instances]


@router.get("/db-instances/{instance_id}", response_model=DbInstanceResponse)
def get_db_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    if not check_category_permission(current_user, "数据库", db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有访问数据库的权限"
        )

    instance = db.query(DbInstance).filter(DbInstance.id == instance_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="数据库实例未找到")
    return instance_to_response(instance)


@router.get("/resources/{category_id}", response_model=List[ResourceResponse])
def get_resources(
    category_id: int,
    status: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "guest":
        guest_categories = ["学习", "AI", "软件资源", "测试", "工具"]
        from models import Category
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category or category.name not in guest_categories:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="访客用户没有访问此分类的权限，请先登录"
            )

    query = db.query(Resource).filter(Resource.category_id == category_id)

    if status is not None:
        query = query.filter(Resource.status == status)

    resources = query.order_by(Resource.id.desc()).all()
    return resources


@router.post("/resources", response_model=ResourceResponse)
def create_resource(
    resource_data: ResourceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户没有添加资源的权限，请先登录"
        )

    db_resource = Resource(
        category_id=resource_data.category_id,
        name=resource_data.name,
        url=resource_data.url,
        description=resource_data.description,
        status=resource_data.status
    )
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


@router.delete("/resources/{resource_id}")
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "guest":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="访客用户没有删除资源的权限，请先登录"
        )

    resource = db.query(Resource).filter(Resource.id == resource_id).first()
    if not resource:
        raise HTTPException(status_code=404, detail="资源未找到")

    db.delete(resource)
    db.commit()
    return {"message": "资源删除成功"}


@router.post("/dev-machines", response_model=DevMachineResponse)
def create_dev_machine(
    machine_data: DevMachineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and not current_user.can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有添加研发机器的权限"
        )

    db_machine = DevMachine(
        name=machine_data.name,
        ip=machine_data.ip,
        port=machine_data.port,
        hostname=machine_data.hostname,
        cpu=machine_data.cpu,
        memory=machine_data.memory,
        disk=machine_data.disk,
        os=machine_data.os,
        status=machine_data.status,
        environment=machine_data.environment,
        description=machine_data.description,
        owner_id=machine_data.owner_id,
        organization_id=machine_data.organization_id
    )
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return machine_to_response(db_machine)


@router.put("/dev-machines/{machine_id}", response_model=DevMachineResponse)
def update_dev_machine(
    machine_id: int,
    machine_data: DevMachineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and not current_user.can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有修改研发机器的权限"
        )

    machine = db.query(DevMachine).filter(DevMachine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="研发机器未找到")

    machine.name = machine_data.name
    machine.ip = machine_data.ip
    machine.port = machine_data.port
    machine.hostname = machine_data.hostname
    machine.cpu = machine_data.cpu
    machine.memory = machine_data.memory
    machine.disk = machine_data.disk
    machine.os = machine_data.os
    machine.status = machine_data.status
    machine.environment = machine_data.environment
    machine.description = machine_data.description
    machine.owner_id = machine_data.owner_id
    machine.organization_id = machine_data.organization_id

    db.commit()
    db.refresh(machine)
    return machine_to_response(machine)


@router.delete("/dev-machines/{machine_id}")
def delete_dev_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and not current_user.can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有删除研发机器的权限"
        )

    machine = db.query(DevMachine).filter(DevMachine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="研发机器未找到")

    db.delete(machine)
    db.commit()
    return {"message": "研发机器删除成功"}


@router.post("/db-instances", response_model=DbInstanceResponse)
def create_db_instance(
    instance_data: DbInstanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and not current_user.can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有添加数据库实例的权限"
        )

    db_instance = DbInstance(
        name=instance_data.name,
        db_type=instance_data.db_type,
        version=instance_data.version,
        ip=instance_data.ip,
        port=instance_data.port,
        charset=instance_data.charset,
        status=instance_data.status,
        environment=instance_data.environment,
        description=instance_data.description,
        owner_id=instance_data.owner_id,
        organization_id=instance_data.organization_id
    )
    db.add(db_instance)
    db.commit()
    db.refresh(db_instance)
    return instance_to_response(db_instance)


@router.put("/db-instances/{instance_id}", response_model=DbInstanceResponse)
def update_db_instance(
    instance_id: int,
    instance_data: DbInstanceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and not current_user.can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有修改数据库实例的权限"
        )

    instance = db.query(DbInstance).filter(DbInstance.id == instance_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="数据库实例未找到")

    instance.name = instance_data.name
    instance.db_type = instance_data.db_type
    instance.version = instance_data.version
    instance.ip = instance_data.ip
    instance.port = instance_data.port
    instance.charset = instance_data.charset
    instance.status = instance_data.status
    instance.environment = instance_data.environment
    instance.description = instance_data.description
    instance.owner_id = instance_data.owner_id
    instance.organization_id = instance_data.organization_id

    db.commit()
    db.refresh(instance)
    return instance_to_response(instance)


@router.delete("/db-instances/{instance_id}")
def delete_db_instance(
    instance_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin" and not current_user.can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="您没有删除数据库实例的权限"
        )

    instance = db.query(DbInstance).filter(DbInstance.id == instance_id).first()
    if not instance:
        raise HTTPException(status_code=404, detail="数据库实例未找到")

    db.delete(instance)
    db.commit()
    return {"message": "数据库实例删除成功"}
