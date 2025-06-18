from infrastructure.db.repositories.wish import WishRepo

class WishService:
    def __init__(self, repo: WishRepo):
        self.repo = repo

    async def create_wish(
        self, user_id: int, id_category: int,
        description: str, amount, currency: str, deadline
    ):
        # здесь можно вставить проверки (баны, лимиты)
        return await self.repo.create(
            id_requester=user_id,
            id_category=id_category,
            description=description,
            amount=amount,
            currency=currency,
            deadline=deadline
        )
