# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionHandleServiceSelection(Action):
    def name(self):
        return "action_handle_service_selection"

    def run(self, dispatcher, tracker, domain):
        user_selection = tracker.latest_message.get("text")

        options = {
            "1": "🌐 You selected **Website & Software Development**. What do you need?\n1️⃣ Business Websites\n2️⃣ E-Commerce Platforms\n3️⃣ Custom Web Applications\n🔄 Type '0' to return to the main menu.",
            "2": "📱 You selected **Mobile App Development**. What do you need?\n1️⃣ iOS App Development\n2️⃣ Android App Development\n3️⃣ Cross-Platform Apps\n🔄 Type '0' to return to the main menu.",
            "3": "🤖 You selected **AI & Automation Solutions**. What do you need?\n1️⃣ AI-Powered Chatbots\n2️⃣ Business Process Automation\n3️⃣ Data Analytics & ML Models\n🔄 Type '0' to return to the main menu.",
            "4": "🎨 You selected **Branding & Digital Presence**. What do you need?\n1️⃣ Logo & Branding\n2️⃣ Social Media Marketing\n3️⃣ SEO Optimization\n🔄 Type '0' to return to the main menu.",
            "5": "👨‍💻 You selected **IT Staffing & Hiring**. What do you need?\n1️⃣ IT Staff Augmentation\n2️⃣ Dedicated Development Teams\n3️⃣ Recruitment & Hiring Services\n🔄 Type '0' to return to the main menu.",
            "0": "🔄 Returning to the main menu...\n1️⃣ Website & Software Development\n2️⃣ Mobile App Development\n3️⃣ AI & Automation Solutions\n4️⃣ Branding & Digital Presence\n5️⃣ IT Staffing & Hiring\n(Type a number to continue)"
        }

        response = options.get(user_selection, "⚠️ I'm not sure I understand. Please enter a number from the menu.")
        dispatcher.utter_message(text=response)
        return [SlotSet("option", user_selection)]
