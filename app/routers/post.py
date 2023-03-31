from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/scrape", tags=[""])

class ScrapeRequest(BaseModel):
  corporation: str
  store: str
  itemCheck: List[str]
  type: str


@router.post("/")
async def scrape(scrapeRequest: ScrapeRequest):
  print(scrapeRequest)
  return scrapeRequest
