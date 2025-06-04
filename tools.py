from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun, AskNewsSearch
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
 # ^This import i used to create your own tool
from datetime import datetime

search = DuckDuckGoSearchRun()
search_tool = Tool(
    name = "search",
    func = search.run,
    description = "Use this tool to search the web for information."
)

# doc content is limited to only 100 characters here but this can be changed
api_wrapper = WikipediaAPIWrapper(top_k_results = 1, doc_content_chars_max = 100)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)

# This function saves the research output to a text file with a timestamp and is a tool created by me and that the llm can use
def save_to_txt(data: str, filename:str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data saved to {filename} at {timestamp}."

save_tool = Tool(
    name = "save_to_txt",
    func = save_to_txt,
    description = "Use this tool to save the research output to a text file."
)