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
import logging as logger
import requests
import os

router = APIRouter(prefix="/scrape", tags=[""])


# {
# "storeName": "safeway",
# "storeLocation": "testStore",
# "requestDate": "datetime.now",
# "url": "safeway.com",
# "items": ["milk", "eggs"],
# "xpathToPagination": "/html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[2]/search-grid/div[4]/button",
# "paginationType": "scroll",
# "paginationElementValue": "Load more",
# "hasInput": True,
# "xpathToInput": "//*[@id="skip-main-content"]",
# "iterables": None,
# "version": "0.0.1"
# }


class ScrapeRequest(BaseModel):
    storeName: Optional[str]
    storeLocation: str
    url: str
    items: List[str]
    requestDate: datetime
    xpathToPagination: Optional[str]
    paginationType: Optional[str]
    paginationElementValue: Optional[str]
    hasInput: bool  # Determines what steps the driver should take. Priority: 1
    xpathToInput: Optional[str]  # Use this to get the input element
    pathToProduct: Optional[List[str]]
    iterables: Optional[
        List[str]
    ]  # Used to find an input element if there's one but no xPath given. Or used to find a given element.
    version: str


class ScrapeItemData(BaseModel):
    name: str
    price: str
    quantity: Optional[str]
    perQuantity: Optional[str]
    ratingAtStore: Optional[str]


# def getItemDataByPath(
#     driver: webdriver,
#     item: str,
#     xpathToInput: str,
#     paginationType: str,
#     xpathToPagination: str,
#     paginationElementValue: str,
# ) -> ScrapeItemData:
#     """Takes in an item to search and iterates through all the products listed.
#     If the item is not found, then it will return None.
#     If the item is found, then it will return a ScrapeItemData object.

#     Args:
#         driver (webdriver): _description_
#         item (str): _description_
#         xpathToInput (str): _description_
#         paginationType (str): _description_
#         xpathToPagination (str): _description_
#         paginationElementValue (str): _description_

#     Raises:
#         Exception: _description_

#     Returns:
#         ScrapeItemData: _description_
#     """

#     try:
#         possiblePaginationElementTexts = ["Load more", "Show more"]
#         possiblePagePaginationElementTexts = ["Next page"]

#         driver.find_element_by_xpath(xpathToInput).send_keys(item + Keys.ENTER)

#         WebDriverWait(driver, 10).until(
#             listOfProducts=driver.find_element_by_xpath(
#                 "/html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[2]/search-grid/div[1]"
#             )
#         )

#         # 1. Check if we have propigating pagination or numbered
#         # Check -> if paginationType is Truthy
#         if paginationType:
#             # Get/Wait for element
#             element = WebDriverWait(driver, 10).until(
#                 driver.get_element_by_xpath(xpathToPagination)
#             )

#             # if no element, then raise exception
#             if not element:
#                 raise Exception(f"Could not find {xpathToPagination}")

#             # if element exists, then keep clicking load more
#             # Handle scrolling pagination
#             if element.get_attribute(
#                 "value"
#             ) == paginationElementValue or possiblePaginationElementTexts.index(
#                 element.get_attribute("value")
#             ):
#                 logger.info(f"Paginating for more products...")
#                 WebDriverWait(driver, 10).until(
#                     driver.get_element_by_xpath(xpathToPagination)
#                 )

#                 # Pagination found -> Go til no more items need to be loaded
#                 while element:
#                     driver.get_element_by_xpath(xpathToPagination).click()
#                     element = WebDriverWait(driver, 10).until(
#                         driver.get_element_by_xpath(xpathToPagination)
#                     )
#             else:
#                 # TODO - Handle page pagination
#                 logger.info("We'd go brute force here")
#     except Exception as e:
#         return e
#     return


# def scrapeByInput(scrapeRequest: ScrapeRequest) -> List[ScrapeItemData]:
#     """Accepts an input driven scrape. Meaning we know that we have an input on the page.
#     Args:
#         scrapeRequest (ScrapeRequest): We expect this to haven xpathToInput.
#     Returns:
#         List[ScrapeItemData] : Expected to return a list of ScrapeItemData objects.
#     """
#     results: List[ScrapeItemData] = []

#     try:
#         driver = webdriver.Firefox()
#         driver.get(scrapeRequest.url)

#         # Scrape each item by input
#         if scrapeRequest.xpathToInput:
#             for item in scrapeRequest.items:
#                 results.append(
#                     getItemDataByPath(
#                         driver,
#                         item,
#                         scrapeRequest.xpathToInput,
#                         scrapeRequest.paginationType,
#                         scrapeRequest.xpathToPagination,
#                         scrapeRequest.paginationElementValue,
#                     )
#                 )

#         return results
#     except Exception as e:
#         return e
#     finally:
#         driver.quit()


# # def tryBeforeYouQuit(scrapeRequest: ScrapeRequest) -> None:
# #     return None


# # # TODO https://www.zenrows.com/blog/selenium-avoid-bot-detection#ip-rotation-proxy
# def scrapeData(scrapeRequest: ScrapeRequest) -> None:
#     results: List[ScrapeItemData] = []

#     try:
#         # 1. Check if we have items to scrape
#         if len(scrapeRequest.items) == 0:
#             raise Exception("No items to scrape")
#         elif scrapeRequest.hasInput:
#             results = scrapeByInput(scrapeRequest)
#             print("\n\nresults\n\n")
#             print(results)
#         # else:
#         #     results = tryBeforeYouQuit(scrapeRequest)
#     except Exception as e:
#         logger.error(
#             "\n We've caught an error while trying to initiate the scrape request."
#         )
#         logger.error(e)
#         # requests.post(
#         #     os.environ.get("ORGANIZER_URL"), json={"error": "true", "data": results}
#         # )

#         return None
#     # TODO - Response to Organizer
#     # requests.post(
#     #     os.environ.get("ORGANIZER_URL"), json={"error": "true", "data": results}
#     # )

#     return None


# # REVIEW This is on hold for now
# @router.post("/")
# async def scrape(scrapeRequest: ScrapeRequest, background_Tasks: BackgroundTasks):
#     # TODO - Call Selenium scrape data
#     # https://fastapi.tiangolo.com/tutorial/background-tasks/
#     if os.environ.get("ORGANIZER_URL") == "true":
#         background_Tasks.add_task(scrapeData, scrapeRequest)
#     else:
#         return Response(status_code=500)
#     return Response(status_code=200)

class Product(BaseModel):
    name: str
    price: int

class Location(BaseModel):
    lat: Optional[float]
    lon: Optional[float]
    city_name: Optional[str]
    address: Optional[str]
    zip_code: Optional[str]


def getProductsInCategory() -> List[Product]:

@router.post("/seedproducts")
async def seedProducts(categoryList : List[str], location: Location):
    try:
        state.set_busy_state()
        for category in categoryList:
            getProductsInCategory(category)
        



    except Exception as e:
        print(e)
        # TODO - properr error logger
        return "failed"


@router.get("/status")
async def get_scrape_status() -> str:
    try:
        currentStatus = state.get_current_state()
        return currentStatus
    except Exception as e:
        print(e)
        # TODO - properr error logger
        return "failed"
