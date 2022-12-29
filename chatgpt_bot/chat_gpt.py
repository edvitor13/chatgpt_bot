import openai

from .db import Database



class ChatGPT:
    
    def __init__(
        self, 
        api_key: str | None = None, 
        id_user_discord: str | None = None
    ):
        self._db: Database
        self._connect_db()
        
        self.api_key = api_key
        if self.api_key is None and id_user_discord is not None:
            self.api_key = self.get_api_key_by_id_discord(
                id_user_discord)

        # if self.api_key is None:
        #     if 'CHATGPT_API_KEY' in os.environ:
        #         self.api_key = os.environ['CHATGPT_API_KEY']
        
        self.__last_response: dict = None


    def ask(self, message: str) -> str | None:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=message,
            temperature=0,
            max_tokens=1024,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["<|endoftext|>"],
            api_key=self.api_key
        )

        self.__last_response = response
        return response['choices'][0]["text"]


    def _connect_db(self):
        self._db = Database("chat_gpt.db")

        cur = self._db.execute(
            "SELECT name FROM sqlite_master WHERE "
            "type='table' AND name='open_api_keys'"
        )

        results = cur.fetchall()

        if len(results) != 1:
            self._db.execute(
                """
                CREATE TABLE open_api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_discord TEXT,
                    key_open_api TEXT
                )
                """
            )

            self._db.commit()


    def get_api_key_by_id_discord(self, id_discord: str) -> str | None:
        results = self._db.execute(
            "SELECT key_open_api FROM open_api_keys WHERE id_discord=?",
            (id_discord,)
        ).fetchall()

        if len(results) == 0:
            return None
        
        return results[0]['key_open_api']


    def insert_api_key(self, id_user_discord: str, api_key: str):
        results = self._db.execute(
            "SELECT key_open_api FROM open_api_keys WHERE id_discord=?",
            (id_user_discord,)
        ).fetchall()

        if len(results) > 0:
            return None

        self._db.execute(
            "INSERT INTO open_api_keys (id_discord, key_open_api) "
            "VALUES (?,?)",
            (id_user_discord, api_key)
        )

        self._db.commit()
