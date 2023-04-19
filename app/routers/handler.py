import time
from datetime import datetime
from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import Response, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
from app.data.state import state
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from app.data.constants import dictOfStores
import logging as log
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
#                 log.info(f"Paginating for more products...")
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
#                 log.info("We'd go brute force here")
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
#         log.error(
#             "\n We've caught an error while trying to initiate the scrape request."
#         )
#         log.error(e)
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


# Below are a list of espected_conditions -> EC ->
# title_is
# title_contains
# presence_of_element_located
# visibility_of_element_located
# visibility_of
# presence_of_all_elements_located
# text_to_be_present_in_element
# text_to_be_present_in_element_value
# frame_to_be_available_and_switch_to_it
# invisibility_of_element_located
# element_to_be_clickable
# staleness_of
# element_to_be_selected
# element_located_to_be_selected
# element_selection_state_to_be
# element_located_selection_state_to_be
# alert_is_present


def getProductsInCategory(driver, category: str) -> List[Product]:
    try:
        hasPagination = True

        # 1. Get search bar
        log.info("finding input element")
        try:
            pageInputElements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//*[@id="skip-main-content"]')
                )
            )
        except TimeoutException:
            raise TimeoutException("Timeout occured for finding input element")

        if len(pageInputElements) == 0:
            raise Exception("Could not find input")
        else:
            log.info("Found input element")

        pageInputElement = pageInputElements[0]

        # 1.5 Check if input has text
        pageInputElement.clear()

        # 2. Input category text and
        # pageInputElement.send_keys("black" + Keys.SPACE + "beans" + Keys.ENTER)
        actions = ActionChains(driver)
        actions.click(pageInputElement)
        actions.send_keys(category, Keys.ENTER)
        actions.perform()

        # 3. Check for pagination -> Load all in 1 page
        while hasPagination:
            try:
                paginationElements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.XPATH,
                            "/html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[3]/div[2]/search-grid/div[4]/button",
                        )
                    )
                )
            except TimeoutException:
                log.warning("Timeout occured for finding pagination")
                paginationElements = []

            if len(paginationElements) == 0:
                log.info("No pagination")
                hasPagination = False
                break
            else:
                paginationElement = paginationElements[0]
                paginationElement.click()

        log.info("Loaded all products")

        returnList = []
        # 4. Get all products on the page
        try:
            productsList = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "product-item-v2"))
            )
        except TimeoutException:
            raise TimeoutException("No products found")

        log.info(f"Found {len(productsList)} products")

        time.sleep(3)

        # 5. Get data from each product on the page
        for product in productsList:
            name = ""
            price = ""

            try:
                name = product.find_element(By.CLASS_NAME, "product-title__name").text
                price = product.find_element(By.CLASS_NAME, "product-price__saleprice")

                try:
                    name = product.find_element(
                        By.CLASS_NAME, "product-item-title-tooltip__inner"
                    ).text
                except NoSuchElementException:
                    pass

                splitPrice = price.text
                listPrice = splitPrice.split()[2]
                sortedList = listPrice[1:].split(".")

                price = {
                    "dollars": int(sortedList[0]),
                    "cents": int(sortedList[1]),
                }

                returnList.append({"name": name, "price": price})
            except TimeoutError:
                log.warning(
                    f"Timeout occured for finding product Name: {name} -- Price: {price}"
                )
            except NoSuchElementException:
                log.warning(f"Could not find product Name: {name} -- Price: {price}")
            except Exception as e:
                log.error(e)

        return returnList

    except TimeoutException as TE:
        log.error(TE)
        return "failed - could not find a required element"

    except Exception as e:
        log.error(e)
        return "failed"


@router.post("/seedproducts")
async def seedProducts(categoryList: List[str]):
    try:
        state.set_busy_state()

        products = {}

        # 1. Open browser and go to store site
        driver = webdriver.Firefox()
        driver.get("https://www.safeway.com/")

        time.sleep(2)

        # 2. Cookie handler
        try:
            cookieBanner = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="onetrust-reject-all-handler"]')
                )
            )

            cookieBanner.click()

        except TimeoutException:
            log.warning("Timeout occured for finding cookie banner")
        except NoSuchElementException:
            log.warning("Could not find cookie banner")

        # 3. Scrape each category
        # TODO -> Add as a background task
        for category in categoryList:
            log.info(f"Seeding {category}")
            products[category] = getProductsInCategory(driver, category)

        log.info("Seeding complete")
        return JSONResponse(status_code=200, content=products)

    except Exception as e:
        log.info("Failed to seed")
        log.error(e)
        return "failed"
    finally:
        # driver.quit()
        state.set_idle_state()


@router.get("/status")
async def get_scrape_status() -> str:
    try:
        currentStatus = state.isStateBusy()
        return currentStatus
    except Exception as e:
        print(e)
        # TODO - properr error log
        return "failed"
