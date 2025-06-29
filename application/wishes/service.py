# application/wishes/service.py

from domain.models import WishStatus
from infrastructure.db.repositories.wish import WishRepo
from infrastructure.db.repositories.deal import DealRepo
from infrastructure.db.repositories.wish_question import WishQuestionRepo

class WishService:
    def __init__(
        self,
        wish_repo: WishRepo,
        deal_repo: DealRepo = None,
        question_repo: WishQuestionRepo = None,
    ):
        self.wish_repo = wish_repo
        self.deal_repo = deal_repo or DealRepo()
        self.question_repo = question_repo or WishQuestionRepo()

    async def create_wish(
        self,
        user_id: int,
        id_category: int,
        description: str,
        amount,
        currency: str,
        deadline,
    ):
        # Можно здесь добавить валидации (лимиты, статус аккаунта и т.д.)
        return await self.wish_repo.create(
            id_requester=user_id,
            id_category=id_category,
            description=description,
            amount=amount,
            currency=currency,
            deadline=deadline,
        )

    async def list_open_wishes(self, limit: int = 5, offset: int = 0):
        return await self.wish_repo.list_open(limit, offset)

    async def take_wish(self, wish_id: int, user_id: int):
        wish = await self.wish_repo.get_by_id(wish_id)
        if wish is None:
            raise ValueError("Заявка не найдена")
        if wish.id_requester == user_id:
            raise ValueError("Нельзя взять свою заявку")
        if wish.status != WishStatus.open:
            raise ValueError("Заявка уже занята")
        deal = await self.deal_repo.create(wish_id=wish_id, wishmaker_id=user_id)
        await self.wish_repo.update_status(wish_id, WishStatus.taken.value)
        return deal

    async def ask_question(
        self,
        wish_id: int,
        sender_id: int,
        receiver_id: int,
        question: str,
    ):
        wish = await self.wish_repo.get_by_id(wish_id)
        if wish is None or wish.status != WishStatus.open:
            raise ValueError("Нельзя задавать вопрос по этой заявке")
        return await self.question_repo.create(
            wish_id=wish_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            question=question,
        )
