from agent import Agent
from tools.time_tool import TimeTool

if __name__ == "__main__":
    agent = Agent([TimeTool()])
    agent.invoke("What time is it?")
    agent.speak()
