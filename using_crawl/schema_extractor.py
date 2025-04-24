import asyncio
import os
import json
import base64
from pathlib import Path
from typing import List
from crawl4ai.proxy_strategy import ProxyConfig

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, CrawlResult
from crawl4ai import RoundRobinProxyStrategy
from crawl4ai import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai import LLMConfig
from crawl4ai import PruningContentFilter, BM25ContentFilter
from crawl4ai import DefaultMarkdownGenerator
from crawl4ai import BFSDeepCrawlStrategy, DomainFilter, FilterChain
from crawl4ai import BrowserConfig
from pydantic import BaseModel, Field

from dotenv import load_dotenv
import os

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

__cur_dir__ = Path(__file__).parent

async def demo_css_structured_extraction_no_schema():
    """Extract structured data using CSS selectors"""
    print("\n=== Structured Extraction ===")
    # Sample HTML for schema generation (one-time cost)

    sample_html = """
<div class="traffic-card-gallery" data-product_id="1601326906180" ...>
  <a href="https://www.alibaba.com/product-detail/OLED-13-3-Inch-Portable-Monitor_1601326906180.html" class="product-image ..." ...>
    <div class="il-relative" role="region" aria-roledescription="carousel">
      <div class="il-overflow-hidden">
        <div class="il-flex" style="transform: translate3d(0px, 0px, 0px);">
          <div role="group" aria-roledescription="slide" class="...">
            <img fetchpriority="high" src="//s.alicdn.com/@sc04/kf/H0b4322c62b2047349751a34a8e27796fI.jpg_300x300.jpg" loading="eager">
        </div>
      </div>
  </a>

  <div class="il-flex il-flex-1 il-flex-col il-justify-start">
    <a class="product-title ...">
      <h2 style="display: inline;">
        21-inch HD Slim Touch Tablet PC 64G/512G SSD 2.48GHz Windows 7/8/10 Industrial Tablet PC
      </h2>
    </a>
    <div class="il-mb-[0.125rem] il-text-xl il-font-bold il-flex il-items-start" data-component="ProductPrice">
        $281.00-291.00
    </div>
    <div class="il-text-sm il-text-secondary-foreground" data-component="ProductMoq">
        Min. Order: 1 set
    </div>
    ...
  </div>
</div>
"""

    # Check if schema file exists
    schema_file_path = f"{__cur_dir__}/tmp/schema.json"
    if os.path.exists(schema_file_path):
        with open(schema_file_path, "r") as f:
            schema = json.load(f)
    else:
        print("Print the schema")
        # Generate schema using LLM (one-time setup)
        schema = JsonCssExtractionStrategy.generate_schema(
            html=sample_html,
            llm_config=LLMConfig
            (
                provider="groq/llama3-8b-8192",
                api_token= groq_key,
            ),
            query=
            (
                "From https://www.alibaba.com/showroom/laptop.html, "
                "I have shared a sample of one product card. "
                "Please extract: product image URL, product title, product URL, price, and minimum order quantity."
            ),
        )    

    print(f"Generated schema: {json.dumps(schema, indent=2)}")
    # Save the schema to a file , and use it for future extractions, in result for such extraction you will call LLM once
    with open(f"{__cur_dir__}/tmp/schema.json", "w") as f:
        json.dump(schema, f, indent=2)

    # Create no-LLM extraction strategy with the generated schema
    extraction_strategy = JsonCssExtractionStrategy(schema)
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    # Use the fast CSS extraction (no LLM calls during extraction)
    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            "https://www.alibaba.com/showroom/laptop.html", config=config
        )
        
        for result in results:
            print(f"URL: {result.url}")
            print(f"Success: {result.success}")
            
            if result.success:
            
                data = json.loads(result.extracted_content)
                print(f"Number of items extracted: {len(data)}") 
                for item in data:
                    item["image"] = "https:" + item["image"]
                print(f"{json.dumps(data, indent=2)}")
            else:
                print("Failed to extract structured data")
       
async def main():
   
    crawler_cfg = CrawlerRunConfig(
            exclude_external_links=True,          # No links outside primary domain
            exclude_social_media_links=True       # Skip recognized social media domains
    )
    await demo_css_structured_extraction_no_schema()

    print("\n===Completed ===")

if __name__ == "__main__":
    asyncio.run(main())


    