from langchain_core.tools import BaseToolkit

from toolkit.execute_tool import SupaExecuteTool
from toolkit.search_tool import SupaSearchTool


class SupaToolkit(BaseToolkit):
    """
    A toolkit that contains the supa_search and supa_execute tools to build Supatool enabled agents.
    """

    def get_tools(self):
        """
        Get tools in the toolkit.
        """
        return [SupaSearchTool(), SupaExecuteTool()]
