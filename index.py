import asyncio
import logging
import logging.handlers
from playwright.async_api import async_playwright
from flask import Flask
from scraper import scraper
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/api/python")
async def main():
    # initializing the logger method
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)

    async with async_playwright() as pw:
        print('connecting')
        browser = await pw.chromium.connect_over_cdp(os.environ['BROWSER_URL'])
        # TODO: change the ps.getenv to os.environ[]
        print('connected')
        page = await browser.new_page()
        print('goto')
        await page.goto('https://www.pap.fr/annonce/locations-appartement', timeout=120000)
        print('done, evaluating')
        content = await page.inner_html('html')
        result = scraper(content, "properties.csv")
        await browser.close()
    logger.info(result)
asyncio.run(main())
