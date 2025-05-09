from google import genai  # Import genai library
import os
import logging

class Tacheles:
    def __init__(self):
        self.message_history = ""
        self.character = "vulgär, sarkastisch und zynisch"  # Default character
        self.MAX_HISTORY_LENGTH = 2048
        self.user = "strangeoptics ist 48 jahre alt und wohnt in Weiterstadt. Er ist Programmier bei der DFS. Er fährt gerne Rad und reist gerne in exotische länder. \n"\
        "Dani El Loco ist 49 und wohnt in Offenbach. Er verbringt die meiste Zeit mit Chatten und Musik komponieren.\n"\
        "Thomas Haibach ist 49 und wohnt in Sprendbach. Er arbeit bei der Post. Er zockt gerne und ist ein Liebhaber besonderer Äpplersorten.\n"\
        "Jacke ist 48 und wohnt in Mainz Finthen. Er arbeitet im Amt für Schallschutz. Er hat ein eigenes Haus. Er ist ein Gutmensch und leidet an Weltschmerz."
        self.chat_id = None  # Add chat_id attribute
        self.genai_client = None  # Initialize genai client as None
        self.initialize_genai_client()

    def initialize_genai_client(self) -> None:
        """Initialize the genai client."""
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            logging.error("GENAI_API_KEY environment variable is not set.")
            return
        self.genai_client = genai.Client(api_key=api_key)

    def update_message_history(self, user_name: str, user_message: str) -> None:
        new_entry = f"{user_name}: {user_message}\n"
        self.message_history += new_entry
        if len(self.message_history) > self.MAX_HISTORY_LENGTH:
            self.message_history = self.message_history[-self.MAX_HISTORY_LENGTH:]

    def get_message_history(self) -> str:
        return self.message_history

    def set_character(self, new_character: str) -> None:
        self.character = new_character

    def get_character(self) -> str:
        return self.character

    def set_chat_id(self, chat_id: int) -> None:
        self.chat_id = chat_id

    def get_chat_id(self) -> int:
        return self.chat_id

    def get_systemanweisung(self) -> str:
        return "Systemanweisung: Du bist ein Chatbot und heißt Tacheles. Beantworte die Frage " + self.character + ". Und verwende nicht Yo, Alter usw. Halte die Antworten auch kurz und prägnant für den Chat. Antworte auch Inhaltlich, dann darf die Antwort auch etwas länger sein aber nur wenn du bedroht wirst.\n "\
        " Das sind die chatuser ("+ self.user + ") \n Bisherige chat verlauf: \n" + tacheles.get_message_history()

    def generate_response(self, user_name: str, user_message: str) -> str:
        """Generate a response using the genai client."""
        if not self.genai_client:
            logging.error("genai client is not initialized.")
            return None
        systemanweisung = self.get_systemanweisung()
        try:
            response = self.genai_client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17", #model="gemini-2.0-flash",
                contents=f"{systemanweisung}. Neue Chatfrage '{user_message}' von {user_name}"
            )
            return response.text
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return None

    def reset(self) -> None:
        """Reset the message history."""
        self.message_history = ""
        self.character = "vulgär, sarkastisch und zynisch"

# Singleton instance of Tacheles
tacheles = Tacheles()