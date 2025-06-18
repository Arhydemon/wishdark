from infrastructure.db.repo_base import get_conn
from domain.models import Category

class CategoryRepo:
    async def list_all(self) -> list[Category]:
        sql = "SELECT id_category, name FROM public.category ORDER BY name"
        rows = await get_conn().fetch(sql)
        return [Category(id=r["id_category"], name=r["name"]) for r in rows]
