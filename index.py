import asyncio
from playwright.async_api import async_playwright
from flask import Flask
from scraper import scraper
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/api/python")
async def main():
    async with async_playwright() as pw:
        print('connecting')
        browser = await pw.chromium.connect_over_cdp(os.getenv('BROWSER_URL'))
        print('connected')
        page = await browser.new_page()
        print('goto')
        await page.goto('https://www.pap.fr/annonce/locations-appartement', timeout=120000)
        print('done, evaluating')
        content = await page.inner_html('html')
        scraper(content, "properties.csv")
        await browser.close()

asyncio.run(main())
