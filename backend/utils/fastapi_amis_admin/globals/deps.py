from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from utils.fastapi_amis_admin.globals import async_db, sync_db

SyncSess = Annotated[Session, Depends(sync_db.session_generator)]
AsyncSess = Annotated[AsyncSession, Depends(async_db.session_generator)]
