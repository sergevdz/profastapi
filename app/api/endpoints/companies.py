from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from app.schemas.company import CompanyResponse, CompanyCreate, CompanyUpdate
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
# from passlib.context import CryptContext
from app import models
# from pydantic import Field, EmailStr

router = APIRouter()


@router.get("/", response_model=List[CompanyResponse])
def read_companies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
    # current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Retrieve companies.
    """
    companies = crud.company.get_all(db, skip=skip, limit=limit)
    return companies


@router.post("/", response_model=CompanyResponse)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    company_create: CompanyCreate
    # current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Create new company.
    """
    # user = crud.user.get_by_email(db, email=company_create.email)
    # if user:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="The user with this email already exists.",
    #     )
    company = crud.company.create(db, obj_in=company_create)
    return company

@router.put("/{user_id}", response_model=CompanyResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int,
    company_update: CompanyUpdate
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a company.
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company does not exist.",
        )
    company = crud.company.update(db, db_obj=company, obj_in=company_update)
    return company

@router.delete("/{user_id}", response_model=CompanyResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    company_id: int
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Delete a company.
    """
    company = crud.company.get(db, id=company_id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company does not exist.",
        )
    
    company = crud.company.delete(db, id=company_id)
    return company
