# app/schemas/management.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional, Dict

class ManagementProfile(BaseModel):
    id: UUID
    type: str  # "admin" or "staff"
    
    # Common
    email: Optional[str] = None
    
    # Admin fields
    username: Optional[str] = None
    
    # Staff fields
    name: Optional[str] = None
    role: Optional[str] = None
    accesses: Optional[Dict[str, bool]] = None