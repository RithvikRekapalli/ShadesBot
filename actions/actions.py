import speech_recognition as sr
import os
from gtts import gTTS
from AppKit import NSSpeechSynthesizer
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

# 📌 Speech-to-Text (STT) Function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening... Please speak!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio)
            print(f"📝 Recognized Text: {text}")
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand your voice."
        except sr.RequestError:
            return "Speech recognition service is unavailable."

# 📌 Text-to-Speech (TTS) Function
def speak(text):
    """Convert text to speech using macOS's built-in text-to-speech engine."""
    synth = NSSpeechSynthesizer.alloc().init()
    synth.startSpeakingString_(text)


# 📌 Custom Action for Handling Voice Input
class ActionHandleVoiceInput(Action):
    def name(self):
        return "action_handle_voice_input"

    def run(self, dispatcher, tracker, domain):
        user_input = recognize_speech()  # Capture voice input
        dispatcher.utter_message(f"🗣 You said: {user_input}")

        # If user selects a menu option by voice
        if user_input.isdigit():
            return [SlotSet("option", user_input)]
        else:
            dispatcher.utter_message("⚠️ Please say a number to choose an option.")

        return []

# 📌 Custom Action for Handling Numbered Options
class ActionHandleServiceSelection(Action):
    def name(self):
        return "action_handle_service_selection"

    def run(self, dispatcher, tracker, domain):
        user_selection = tracker.get_slot("option")

        options = {
            "1": "🌐 You selected **Website & Software Development**. What do you need?\n1️⃣ Business Websites\n2️⃣ E-Commerce Platforms\n3️⃣ Custom Web Applications\n🔄 Say or type '0' to return.",
            "2": "📱 You selected **Mobile App Development**. What do you need?\n1️⃣ iOS App Development\n2️⃣ Android App Development\n3️⃣ Cross-Platform Apps\n🔄 Say or type '0' to return.",
            "3": "🤖 You selected **AI & Automation Solutions**. What do you need?\n1️⃣ AI-Powered Chatbots\n2️⃣ Business Process Automation\n3️⃣ Data Analytics & ML Models\n🔄 Say or type '0' to return.",
            "4": "🎨 You selected **Branding & Digital Presence**. What do you need?\n1️⃣ Logo & Branding\n2️⃣ Social Media Marketing\n3️⃣ SEO Optimization\n🔄 Say or type '0' to return.",
            "5": "👨‍💻 You selected **IT Staffing & Hiring**. What do you need?\n1️⃣ IT Staff Augmentation\n2️⃣ Dedicated Development Teams\n3️⃣ Recruitment & Hiring Services\n🔄 Say or type '0' to return.",
            "0": "🔄 Returning to the main menu...\n1️⃣ Website & Software Development\n2️⃣ Mobile App Development\n3️⃣ AI & Automation Solutions\n4️⃣ Branding & Digital Presence\n5️⃣ IT Staffing & Hiring\nSay a number to continue."
        }

        response = options.get(user_selection, "⚠️ Invalid option. Please say or type a number from the menu.")
        dispatcher.utter_message(text=response)
        speak(response)  # Convert text response to speech
        return []

# 📌 Custom Action for Ending Session and Providing Feedback Form
class ActionEndSession(Action):
    def name(self):
        return "action_session_end"

    def run(self, dispatcher, tracker, domain):
        feedback_link = "https://your-feedback-form.com"

        dispatcher.utter_message(text="👋 Thank you for using Shades LLC chatbot!")
        dispatcher.utter_message(text=f"👉 We'd love your feedback!\n[Click here to provide feedback]({feedback_link})")
        dispatcher.utter_message(text="🔗 Redirecting to the feedback form...")
        speak("Thank you for using Shades LLC chatbot. Please fill out the feedback form.")
        return []  # ✅ Corrected way to end session in Rasa 3.x+
