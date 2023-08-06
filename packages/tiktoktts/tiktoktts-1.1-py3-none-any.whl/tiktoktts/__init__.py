import json
import requests
import os
import base64

class TextToSpeech:
    voices = '''{
    "Humans": [
        {
          "value": "en_us_001",
          "name": "Female"
        },
        {
          "value": "en_us_006",
          "name": "Male 1"
        },
        {
          "value": "en_us_007",
          "name": "Male 2"
        },
        {
          "value": "en_us_009",
          "name": "Male 3"
        },
        {
          "value": "en_us_010",
          "name": "Male 4"
        }
    ],
    "Characters": [
        {
            "name": "Ghostface (Scream)",
            "value": "en_us_ghostface"
        },
        {
            "name": "Chewbacca (Star Wars)",
            "value": "en_us_chewbacca"
        },
        {
            "name": "C3PO (Star Wars)",
            "value": "en_us_c3po"
        },
        {
            "name": "Stitch (Lilo & Stitch)",
            "value": "en_us_stitch"
        },
        {
            "name": "Stormtrooper (Star Wars)",
            "value": "en_us_stormtrooper"
        },
        {
            "name": "Rocket (Guardians of the Galaxy)",
            "value": "en_us_rocket"
        }
    ],
    "Singing": [
        {
            "name": "Alto",
            "value": "en_female_f08_salut_damour"
        },
        {
            "name": "Tenor",
            "value": "en_male_m03_lobby"
        },
        {
            "name": "Sunshine Soon",
            "value": "en_male_m03_sunshine_soon"
        },
        {
            "name": "Warmy Breeze",
            "value": "en_female_f08_warmy_breeze"
        },
        {
            "name": "Glorious",
            "value": "en_female_ht_f08_glorious"
        },
        {
            "name": "It Goes Up",
            "value": "en_male_sing_funny_it_goes_up"
        },
        {
            "name": "Chipmunk",
            "value": "en_male_m2_xhxs_m03_silly"
        },
        {
            "name": "Dramatic",
            "value": "en_female_ht_f08_wonderful_world"
        }
    ]
}'''

    output_file_name = "output.mp3"
    voice = "en_us_001"
    text = ""
    ENDPOINT = 'https://tiktok-tts.weilnet.workers.dev'
    TEXT_BYTE_LIMIT = 300

    def __init__(self, output_file_name: str="output.mp3", voice: str="en_us_001") -> None:
        self.output_file_name = output_file_name
        self.voice = voice

        print(f"+ Voice set to \"{self.voice}\"")
        pass

    def SetVoice(self, voice):
        j = json.loads(self.voices)

        voices = []
        for c in j:
            for v in j[c]:
                voices.append(v["value"])

        if voice not in voices:
            print(f"- Voice \"{voice}\" not found!")
        else:
            self.voice = voice
            print(f"+ Voice set to \"{self.voice}\"")

    def GetAllVoices(self):
        s = ""
        j = json.loads(self.voices)
        for c in j:
            s += f"Category \"{c}\":\n"
            for v in j[c]:
                s += f'\tVoice \"{v["name"]}\" [{v["value"]}]\n'
        return s

    def GetAllVoicesJson(self):
        return json.loads(self.voices)

    def CheckServiceAvailability(self):
        url = f"{self.ENDPOINT}/api/status"
        response = requests.get(url)
        if response.ok:
            data = json.loads(response.text)
            if data.get("data") and data["data"].get("available"):
                #print(f"* {data['data']['meta']['dc']} (age {data['data']['meta']['age']} minutes) is able to provide service.")
                return True
            else:
                error_message = f"Service not available: {data.get('message', '')}"
                #print(f"* {data['data']['meta']['dc']} (age {data['data']['meta']['age']} minutes) is unable to provide service.")
                raise Exception(error_message)
        else:
            error_message = f"- Error querying API status: {response.status_code}"
            raise Exception(error_message)
    
    def __genaudio__(self, text, voice):
        url = f"{self.ENDPOINT}/api/generation"
        payload = {
            "text": text,
            "voice": voice
        }
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        if response.ok:
            data = json.loads(response.text)
            
            if data.get("data") is not None:
                return data["data"], text
            else:
                error_message = f"Generation failed: {data.get('error', '')}"
                raise Exception(error_message)
        else:
            error_message = f"Error submitting form: {response.status_code}"
            raise Exception(error_message)
    
    def New(self, text, voice=None):
        try:
            self.CheckServiceAvailability()

            self.text = text
            voice = self.voice
            if len(text) == 0:
                text = "Thanks to FlipFlapsRU!"
            if len(text.encode("utf-8")) > self.TEXT_BYTE_LIMIT:
                raise Exception(f"Text must not be over {self.TEXT_BYTE_LIMIT} UTF-8 characters (currently at {len(text)})")
            
            audio_data = self.__genaudio__(text, voice)

            if os.path.exists(self.output_file_name):
                os.remove(self.output_file_name)

            try:
                with open(self.output_file_name, 'wb') as wav_file:
                    wav_file.write(base64.b64decode(audio_data[0]))
                    print(f"+ File {self.output_file_name} generated!")
            except Exception as e:
                print(f'Error saving MP3 file: {e}')
        except Exception as e:
            raise Exception(e)