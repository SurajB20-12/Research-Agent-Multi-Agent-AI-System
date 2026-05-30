from src.tools.tools import web_search, scrape_url
from rich import print

result = scrape_url.invoke(
    "https://yaleclimateconnections.org/2025/09/what-you-need-to-know-about-ai-and-climate-change/"
)
print(result)
