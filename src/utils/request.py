import json
from pathlib import Path
from typing import List, Dict


class RequestUtils:
    FILE_PATH = Path(__file__).parent / "requests.json"

    @classmethod
    def load_requests(cls) -> List[Dict[str, str]]:
        if not cls.FILE_PATH.exists():
            return []
        try:
            with cls.FILE_PATH.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    @classmethod
    def save_requests(cls, requests: List[Dict[str, str]]) -> None:
        with cls.FILE_PATH.open("w", encoding="utf-8") as f:
            json.dump(requests, f, ensure_ascii=False, indent=4)

    @classmethod
    def has_request(cls, user_id: int, channel_id: str) -> bool:
        requests = cls.load_requests()
        return any(req.get(str(user_id)) == channel_id for req in requests)

    @classmethod
    def add_request(cls, user_id: int, channel_id: str) -> None:
        requests = cls.load_requests()
        if not cls.has_request(user_id, channel_id):
            requests.append({str(user_id): channel_id})
            cls.save_requests(requests)

    @classmethod
    def remove_request(cls, user_id: int, channel_id: str) -> None:
        requests = cls.load_requests()
        new_requests = [
            req for req in requests if not (req.get(str(user_id)) == channel_id)
        ]
        cls.save_requests(new_requests)
