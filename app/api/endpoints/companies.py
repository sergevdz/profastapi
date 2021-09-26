from typing import Any, List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from app.schemas.company import CompanyResponse, CompanyCreate, CompanyUpdate
from sqlalchemy.orm import Session
from app.api import dependencies as deps
from app import crud
from app import models

router = APIRouter()


@router.get("/", response_model=List[CompanyResponse])
def read_companies(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
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
    company_create: CompanyCreate,
    current_user: models.User = Depends(deps.get_current_active_user)
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
    company = crud.company.create(
        db,
        obj_in=company_create,
        created_by=current_user.id
    )
    return company

@router.put("/{id}", response_model=CompanyResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    company_update: CompanyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update a company.
    """
    company = crud.company.get(db, id=id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company does not exist.",
        )
    company = crud.company.update(
        db,
        db_obj=company,
        obj_in=company_update,
        modified_by=current_user.id
    )
    return company

@router.delete("/{id}", response_model=CompanyResponse)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    # current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    """
    Delete a company.
    """
    company = crud.company.get(db, id=id)
    if not company:
        raise HTTPException(
            status_code=404,
            detail="The company does not exist.",
        )
    
    company = crud.company.delete(db, id=id)
    return company
