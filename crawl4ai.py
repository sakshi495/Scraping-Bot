import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.chunking_strategy import RegexChunking

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(url="https://en.wikipedia.org/wiki/3_Idiots", bypass_cache=False)
        print(f"Extracted content: {result.extracted_content}")

asyncio.run(main())
