import azure.cognitiveservices.speech as speechsdk
import os
import openai
from dotenv import load_dotenv

load_dotenv()

speech_key = os.getenv("SPEECH_KEY")
service_region = os.getenv("REGION")
openai.api_key = os.getenv("OPENAI_API_KEY")
endpoint_id = os.getenv("ENDPONT_ID")
voices = {
    "france": "fr-FR-AlainNeural",
    "quebec": "fr-CA-AntoineNeural",
    "suisse": "fr-CH-FabriceNeural",
    "belgique": "fr-BE-GerardNeural",
    "inde": "hi-IN-MadhurNeural"}


class Speech():

    def __init__(self, reco_language='fr-FR') -> None:

        self.speech_config = speechsdk.SpeechConfig(
            subscription=speech_key, region=service_region, speech_recognition_language=reco_language)
        # self.speech_config.endpoint_id = endpoint_id

    def talk_in_mic(self):
        self.speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=self.speech_config)
        print("Parlez...")
        result = self.speech_recognizer.recognize_once()
        return result

    def check_voice(self, result):
        # Checks result of get_from_mic method
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("Recognized: {}".format(result.text))
            return True
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("No speech could be recognized: {}".format(
                result.no_match_details))
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech Recognition canceled: {}".format(
                cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(
                    cancellation_details.error_details))
        return False

    def get_textual_answers(self, prompt, n_answers=1, temp=0.6):
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=1024,
            n=n_answers,
            temperature=temp,
        )
        return completions.choices[0].text

    def get_vocal_answers(self, ai_answer, language):
        audio_config = speechsdk.audio.AudioOutputConfig(
            use_default_speaker=True)
        self.speech_config.speech_synthesis_voice_name = voices[language]
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=self.speech_config, audio_config=audio_config)
        synthesizer.speak_text_async(ai_answer).get()
