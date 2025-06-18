from infrastructure.db.repo_base import get_conn
from domain.models import WishQuestion

class WishQuestionRepo:
    async def create(self, *, wish_id: int, sender_id: int,
                     receiver_id: int, question: str) -> WishQuestion:
        sql = """
        INSERT INTO public.wish_question (
            id_wish, sender_id, receiver_id, question
        ) VALUES ($1, $2, $3, $4)
        RETURNING *;
        """
        row = await get_conn().fetchrow(
            sql, wish_id, sender_id, receiver_id, question
        )
        return WishQuestion.model_validate(dict(row))

    async def list_for_wish(self, wish_id: int) -> list[WishQuestion]:
        sql = """
        SELECT * FROM public.wish_question
        WHERE id_wish = $1
        ORDER BY created_at;
        """
        rows = await get_conn().fetch(sql, wish_id)
        return [WishQuestion.model_validate(dict(r)) for r in rows]
