from datetime import datetime
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Optional
from app.data.state import state
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from app.data.constants import dictOfStores

router = APIRouter(prefix="/scrape", tags=[""])

class ScrapeRequest(BaseModel):
  type: str
  storeName: Optional[str]
  storeLocation: str
  items: List[str]
  requestDate: datetime

def getItemData(driver: webdriver, item: str) -> str:
  """ Takes in the driver and the item to be scraped 
      and returns the item's data
  Args:
      driver (webdriver): The Selenium webdriver.
      item (str): The item to get the data for.
  Returns:
      str: _description_
  """
  driver


# TODO https://www.zenrows.com/blog/selenium-avoid-bot-detection#ip-rotation-proxy
def scrapeData(scrapeRequest: ScrapeRequest) -> None:
  # A. Check if we know the store
  if scrapeRequest.storeName in dictOfStores:
    # 1. get store
    currentStore = dictOfStores[scrapeRequest.storeName]
    print(f"Found store: {currentStore}")
    # 2. Start Driver
    driver = webdriver.Firefox()
    # 3. Get website
    driver.get(currentStore["url"])
    # 4. Wait for page to load
    WebDriverWait(driver, 10).until(lambda driver: driver.find_elements(By.XPATH, currentStore["xpathToInput"]))
    elementsLength = len(driver.find_elements(By.XPATH, currentStore["xpathToInput"]))
    if elementsLength > 0:
      # 5. Focus on element by clicking on the input
      driver.find_element(By.XPATH, currentStore["xpathToInput"]).click()
      # 6. Input items
      itemsList = currentStore['items']
      print("Getting item prices...")
      for item in itemsList:
        getItemData(driver, item)
    else :
      # 5-E Failed to find the input
      print(f"Failed to find the input : {elementsLength}")
      # POST to Carver with an appropriate error message

    

  else:
    # Deal with generic outcome
    print(f"Store {scrapeRequest.storeName} not found in dictionary")

  # driver.close()
  return None
  

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