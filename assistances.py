from openai import OpenAI
import time
from utils import load_json_file
#from gtts import gTTS

assJson = load_json_file("config/assistanceConfig_real.json")
mediaJson = load_json_file("config/mediaPath.json")

class ai:
    def __init__(self):
        self.client_ai = OpenAI(api_key=assJson["apikey"])
        self.name = 'mary'
        self.ass_id = assJson["ai"][self.name]["id"]
        self.voice = assJson["ai"][self.name]["voice"]

        self.active = False
        self.answer = False
        self.following_active = False

    def change_ai(self, new_ai_name):
        self.name = new_ai_name
        self.ass_id = assJson["ai"][new_ai_name]["id"]
        self.voice = assJson["ai"][new_ai_name]["voice"]


    def ai_call(self, text):
        if "Ferdinand" in text or "เฟอดินานด์" in text or "เฟอดินาน" in text or "ferdinand" in text or "เฟอร์ดินาน" in text:
            self.name = "ferdinand"
            self.active = True
            self.following_active = False
            self.change_ai(self.name)
            
        if "Mary" in text or "แมรี่" in text or "marry" in text :
            self.name = "mary"
            self.active = True
            self.change_ai(self.name)
        
        if "Migual" in text or "มิเกล" in text or "migual" in text :
            self.name = "migual"
            self.active = True
            self.change_ai(self.name)

    def new_thread(self):
        self.thread = self.client_ai.beta.threads.create()

    def gpt(self,input):
                
        self.client_ai.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=input)

        run = self.client_ai.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.ass_id,
            )

        while 1:
            run = self.client_ai.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id=run.id
                )
            if run.completed_at is not None:
                messages = self.client_ai.beta.threads.messages.list(
                    thread_id=self.thread.id
                    )
                return messages.data[0].content[0].text.value
            time.sleep(2)

    def make_file(self, message):
        #tts = gTTS(text=message, lang="th")
        #tts.save(self.media_json["answer_voice"])

        response = self.client_ai.audio.speech.create(
            model="tts-1",
            voice=self.voice,
            input=message,
        )
        response.stream_to_file(mediaJson["answer"])


       

    