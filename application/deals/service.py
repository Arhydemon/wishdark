from infrastructure.db.repositories.deal_message import DealMessageRepo

class DealService:
    def __init__(self, msg_repo: DealMessageRepo = None):
        self.msg_repo = msg_repo or DealMessageRepo()

    async def send_message(self, deal_id: int, sender_id: int, text: str):
        return await self.msg_repo.create(
            deal_id=deal_id,
            sender_id=sender_id,
            message=text
        )
