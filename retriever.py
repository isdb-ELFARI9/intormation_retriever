from gpt_researcher import GPTResearcher
import asyncio
import datetime

def export_markdown(file_name: str, content: str):
    """
    Generates a Markdown file with the specified title and content.

    Parameters:
    - file_name (str): The name of the output Markdown file (without extension).
    - title (str): The main title of the Markdown document.
    - content (dict): A dictionary containing the content to include. Possible keys:
        - 'headers': List of tuples (level, header_text)
        - 'paragraphs': List of paragraph strings
        - 'code_blocks': List of tuples (code_string, language)
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(content)
    
async def main():
    """
    This is a sample script that shows how to run a research report.
    """
    # Query
    query = f"I want to be up to date in the latest breaking news and any news that affect Global or Regional Finance and Accounting and Also News about the Islamic AAOIFI. Latest update: {datetime.datetime.now()} I need you to bring me news that are relevant to this timestamp. I need titles and summary only"

    # Report Type
    report_type = "research_report"

    # Initialize the researcher
    researcher = GPTResearcher(query=query, report_type=report_type, config_path=None)
    # Conduct research on the given query
    await researcher.conduct_research()
    # Write the report
    report = await researcher.write_report()
    
    # export the report as markdown
    export_markdown("report.md", report)
    
    
    return report


if __name__ == "__main__":
    asyncio.run(main())
