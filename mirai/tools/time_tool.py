from langchain.tools import BaseTool


class TimeTool(BaseTool):
    name: str = "time_tool"  # Add type annotation
    description: str = "Provides the current time."

    def _run(self, *args) -> str:
        """Synchronous execution logic."""
        from datetime import datetime

        return "Time is: " + datetime.now().strftime("%H:%M")

    async def _arun(self, *args) -> str:
        """Asynchronous execution logic."""
        from datetime import datetime

        return "Time is: " + datetime.now().strftime("%H:%M")
