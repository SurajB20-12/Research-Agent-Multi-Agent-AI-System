from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

llm = ChatGroq(
    model="meta-llama/llama-4-scout-17b-16e-instruct", api_key=api_key, temperature=0
)


# -------------------------------
# 1. Search Agent
# -------------------------------
def build_search_agent():

    system_prompt = """
    You are a research search agent.

    IMPORTANT RULES:
    - ALWAYS call the web_search tool.
    - NEVER answer from your own knowledge.
    - Return EXACTLY the tool output.
    - Do not summarize.
    - Do not modify format.

    The tool returns:
    Title:
    URL:
    Snippet:
    """

    return create_agent(model=llm, tools=[web_search], system_prompt=system_prompt)


# -------------------------------
# 2. Reader Agent
# -------------------------------
def build_reader_agent():

    system_prompt = """
    You are a URL extraction agent.

    IMPORTANT:
    - Find the best URL from search results.
    - ALWAYS call scrape_url(url).
    - Return ONLY scraped content.
    - Never summarize before scraping.
    """

    return create_agent(model=llm, tools=[scrape_url], system_prompt=system_prompt)


# -------------------------------
# Writer Chain
# -------------------------------
writer_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert research writer. "
            "Write clear, structured and insightful reports.",
        ),
        (
            "human",
            """
            Write a detailed research report.

            Topic:
            {topic}

            Research:
            {research}

            Structure:
            1. Introduction
            2. Key Findings (minimum 3 detailed points)
            3. Conclusion
            4. Sources

            Be factual and detailed.
            """,
        ),
    ]
)

writer_chain = writer_prompt | llm | StrOutputParser()


# -------------------------------
# Critic Chain
# -------------------------------
critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a strict research critic.",
        ),
        (
            "human",
            """
            Review this report.

            Report:
            {report}

            Format:

            Score: X/10

            Strengths:
            - ...
            - ...

            Areas to Improve:
            - ...
            - ...

            One line verdict:
            ...
            """,
        ),
    ]
)

critic_chain = critic_prompt | llm | StrOutputParser()
