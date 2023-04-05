# https://docs.pytest.org/en/7.1.x/getting-started.html#install-pytest
import pytest
import datetime
from app.routers.handler import scrape, get_scrape_status

dummy_request = {
  "type": "scrape",
  "store": "safeway",
  "items": ["water", "milk", "beer"],
  "requestDate": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

class TestScrape:
  
  # Marker is required for pytest to know
  @pytest.mark.asyncio
  async def test_scrape_post(self):
    response = await scrape(dummy_request)
    assert response == True, "Scraper should return True as an acceptance response"
  
  @pytest.mark.asyncio
  async def test_get_status(self):
    response = await get_scrape_status()
    assert response == "not_running", "should not be running"

  @pytest.mark.asyncio
  async def test_get_status_failed(self, mocker):
    mocker.patch("app.routers.handler.state.get_current_state", Exception("Waa I failed!"))
    response = await get_scrape_status()
    assert response == "failed", "should fail due to an exception"


