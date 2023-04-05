from datetime import datetime
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from app.data.state import state
from selenium import webdriver

router = APIRouter(prefix="/scrape", tags=[""])

class ScrapeRequest(BaseModel):
  type: str
  corporation: Optional[str]
  store: str
  items: List[str]
  requestDate: datetime


@router.post("/")
async def scrape(scrapeRequest: ScrapeRequest) -> bool:
  # TODO - Call Selenium scrape data
  # https://fastapi.tiangolo.com/tutorial/background-tasks/
  return True

@router.get("/status")
async def get_scrape_status() -> str:
  try:
    currentStatus = state.get_current_state()
    return currentStatus
  except Exception as e:
    print(e)
    # TODO - properr error logging
    return "failed"