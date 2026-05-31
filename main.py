from src.pipelines.pipeline import run_research_pipeline
from src.tools.tools import web_search, scrape_url
from rich import print


topic = "What are the latest advancements in AI research as of 2026?"

run_research_pipeline(topic)
