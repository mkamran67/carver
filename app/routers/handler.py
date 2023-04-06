from datetime import datetime
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
from app.data.state import state
from selenium import webdriver
from app.data.constants import dictOfStores

router = APIRouter(prefix="/scrape", tags=[""])

class ScrapeRequest(BaseModel):
  type: str
  storeName: Optional[str]
  storeLocation: str
  items: List[str]
  requestDate: datetime



def scrapeData(scrapeRequest: ScrapeRequest) -> None:

  # 1. Check if we know the store
  dictOfStores.get(scrapeRequest.storeName);
  driver = webdriver.Firefox()
  

@router.post("/")
async def scrape(scrapeRequest: ScrapeRequest, background_Tasks: BackgroundTasks) -> bool:
  # TODO - Call Selenium scrape data
  # https://fastapi.tiangolo.com/tutorial/background-tasks/

  background_Tasks.add_task(scrapeData, scrapeRequest)
  return Response(status_code=200)

@router.get("/status")
async def get_scrape_status() -> str:
  try:
    currentStatus = state.get_current_state()
    return currentStatus
  except Exception as e:
    print(e)
    # TODO - properr error logging
    return "failed"