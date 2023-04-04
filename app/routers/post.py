from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/scrape", tags=[""])

class ScrapeRequest(BaseModel):
  type: str
  corporation: Optional(str)
  store: str
  items: List[str]
  requestDate: datetime


@router.post("/")
async def scrape(scrapeRequest: ScrapeRequest):
  print(scrapeRequest)
  return scrapeRequest
