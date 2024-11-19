import io
import os
from typing import List

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents import create_react_agent
from langchain.tools import BaseTool
from langchain_groq.chat_models import ChatGroq
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()


class Agent:
    def __init__(self, tools: List[BaseTool]):
        self.llm = ChatGroq(model="llama-3.2-90b-text-preview", temperature=0)
        # self.stt = ChatGroq(model="distil-whisper-large-v3-en", temperature=0)
        self.memory = None
        self.tools = tools
        self.prompt = hub.pull("hwchase17/react")
        self._agent = create_react_agent(
            llm=self.llm, tools=self.tools, prompt=self.prompt
        )
        self.executor = AgentExecutor(agent=self._agent, tools=self.tools, verbose=True)
        self.audio_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def invoke(self, input):
        response = self.executor.invoke({"input": input})
        self.response = response["output"]
        return self.response

    def speak(self):
        # self.audio_client.generate(text=self.response)
        response = self.audio_client.text_to_speech.convert(
            voice_id="9BWtsMINqrJLrRacOk9x", text=self.response
        )

        # Convert the response (stream) to a bytes-like object
        audio_content = b"".join(response)

        # Create an audio segment from the byte content
        audio = AudioSegment.from_mp3(io.BytesIO(audio_content))

        # Play the audio
        play(audio)
