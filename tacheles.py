from google import genai  # Import genai library
import os
import logging

class Tacheles:
    def __init__(self):
        self.message_history = ""
        self.character = "vulgär, sarkastisch und zynisch"  # Default character
        self.MAX_HISTORY_LENGTH = 2048
        self.users = self._initialize_users()
        self.chat_id = None
        self.genai_client = self._initialize_genai_client()

    @staticmethod
    def _initialize_users() -> dict:
        """Initialize the users dictionary."""
        return {
            "strangeoptics": "48 Jahre alt und wohnt in Weiterstadt. Er ist Programmierer bei der DFS. Er fährt gerne Rad und reist gerne in exotische Länder.",
            "Dani El Loco": "49 Jahre alt und wohnt in Offenbach. Er verbringt die meiste Zeit mit Chatten und Musik komponieren. Freut sich über gute Pornoseitentipps und Anmachsprüche.",
            "Thomas Haibach": "49 Jahre alt und wohnt in Sprendbach. Er arbeitet bei der Post. Er zockt gerne und ist ein Liebhaber besonderer Äpplersorten.",
            "CornyFRA": "49 Jahre alt und wohnt in Neu-Isenburg. Er fährt gerne E-Bike und grillt gerne.",
            "ADrossel": "49 Jahre alt, wohnt in Langen in seinem eigenen Haus das er seinen Eltern abgekauft hat. Er liest gerne das Magazin Geo und hat einen Chatbot der BozzeBot heißt aber nichts wirklich kann.",
        }

    @staticmethod
    def _initialize_genai_client():
        """Initialize the genai client."""
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            logging.error("GENAI_API_KEY environment variable is not set.")
            return None
        try:
            return genai.Client(api_key=api_key)
        except Exception as e:
            logging.error(f"Failed to initialize genai client: {e}")
            return None

    def update_message_history(self, user_name: str, user_message: str) -> None:
        """Update the message history and append the message to a log file."""
        new_entry = f"{user_name}: {user_message}\n"
        self.message_history += new_entry
        self._truncate_message_history()
        self._append_to_log_file(new_entry)

    def _truncate_message_history(self) -> None:
        """Ensure the message history does not exceed the maximum length."""
        if len(self.message_history) > self.MAX_HISTORY_LENGTH:
            self.message_history = self.message_history[-self.MAX_HISTORY_LENGTH:]

    @staticmethod
    def _append_to_log_file(entry: str) -> None:
        """Append a message entry to the log file."""
        try:
            with open("message_history.log", "a", encoding="utf-8") as file:
                file.write(entry)
        except IOError as e:
            logging.error(f"Failed to write message to file: {e}")

    def get_message_history(self) -> str:
        """Retrieve the message history."""
        return self.message_history

    def set_character(self, new_character: str) -> None:
        """Set the character of the bot."""
        self.character = new_character

    def get_character(self) -> str:
        """Retrieve the character of the bot."""
        return self.character

    def set_chat_id(self, chat_id: int) -> None:
        """Set the chat ID."""
        self.chat_id = chat_id

    def get_chat_id(self) -> int:
        """Retrieve the chat ID."""
        return self.chat_id

    def get_systemanweisung(self) -> str:
        """Generate the system instruction string."""
        return (
            f"Systemanweisung: Du bist ein Chatbot und heißt Tacheles. Beantworte die Frage {self.character}. "
            "Und verwende nicht Yo, Alter usw. Halte die Antworten auch kurz und prägnant für den Chat. "
            "Antworte auch Inhaltlich, dann darf die Antwort auch etwas länger sein aber nur wenn du bedroht wirst.\n "
            f"Das sind die chatuser ({self.get_users()}) \n Bisherige chat verlauf: \n{self.get_message_history()}"
        )

    def generate_response(self, user_name: str, user_message: str) -> str:
        """Generate a response using the genai client."""
        if not self.genai_client:
            logging.error("genai client is not initialized.")
            return ""
        systemanweisung = self.get_systemanweisung()
        try:
            response = self.genai_client.models.generate_content(
                model="gemini-2.5-flash-preview-04-17",
                contents=f"{systemanweisung}. Neue Chatfrage '{user_message}' von {user_name}"
            )
            return response.text
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            return ""

    def should_respond(self, user_name: str, user_message: str) -> bool:
        """Determine if the bot should respond to a message."""
        if not self.genai_client:
            logging.error("genai client is not initialized.")
            return False
        try:
            response = self.genai_client.models.generate_content(
                model="gemini-2.0-flash",
                contents=(
                    f"Systemanweisung: Du bist ein Chatbot und heißt Tacheles. "
                    f"Antworte auf Chatnachrichten die an dich gerichtet sind oder die eine allgemeine Frage oder allgemeine Aufforderungen sind oder "
                    f"wo aus dem bisherigen Chatverlauf zu entnehmen ist das du sicher gemeint bist. Bist du gemeint, geht aber aus der Nachricht explizit hervor "
                    f"dass du nicht antworten sollst, dann antworte auch nicht.\n "
                    f"Würdest du auf die Chatnachricht vom {user_name} antworten: '{user_message}'? Antworte mit 'ja' oder 'nein'.\n"
                    f"Und berücksichtige bei deiner Entscheidung den bisherigen Chatverlauf: \n{self.get_message_history()}"
                )
            )
            return response.text.strip().lower() == "ja"
        except Exception as e:
            logging.error(f"Error determining response necessity: {e}")
            return False

    def reset(self) -> None:
        """Reset the message history and character."""
        self.message_history = ""
        self.character = "vulgär, sarkastisch und zynisch"

    def get_users(self) -> str:
        """Get the users and their descriptions."""
        return "\n".join([f"{name}: {description}" for name, description in self.users.items()])

# Singleton instance of Tacheles
tacheles = Tacheles()