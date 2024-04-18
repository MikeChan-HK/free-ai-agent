class available_tools:
    def import_all_tools():
        from langchain.tools import DuckDuckGoSearchRun
        from langchain.agents.tools import Tool
        from langchain.chains import LLMMathChain

        search = DuckDuckGoSearchRun()
        llm_math_chain = LLMMathChain(llm=llm, verbose=True)

        return search, llm_math_chain