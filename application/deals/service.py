from infrastructure.db.repositories.deal_message import DealMessageRepo

class DealService:
    def __init__(self, repo: DealMessageRepo = None):
        self.repo = repo or DealMessageRepo()

    async def send_message(self, deal_id: int, sender_id: int, text: str):
        return await self.repo.create(deal_id=deal_id, sender_id=sender_id, message=text)
