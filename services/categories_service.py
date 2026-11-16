from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.utils.category_utils import flatten_categories
from models.category import MainCategory, SubCategory
from models.seed_data import BAZAAR_CATEGORIES


class CategoryService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def seed_categories(self) -> None:
        """
        Идемпотентно создаёт main/sub категории из BAZAAR_CATEGORIES.

          Создаёт подкатегории для всех уровней вложенности
          (например, для ('Mining', 'Gemstones', 'Jade Gemstone')
          появятся SubCategory 'Gemstones' и 'Jade Gemstone').
          Не пересоздаёт уже существующие.
        """
        mains: dict[str, MainCategory] = {}
        seen_subs: set[tuple[int, str]] = set()

        for path, _display in flatten_categories(BAZAAR_CATEGORIES):
            main_name = path[0]

            main = mains.get(main_name)
            if main is None:
                stmt = select(MainCategory).where(MainCategory.name == main_name)
                main = (await self.session.execute(stmt)).scalar_one_or_none()
                if main is None:
                    main = MainCategory(name=main_name)
                    self.session.add(main)
                    await self.session.flush()   
                mains[main_name] = main

            # подкатегории из path 
            for sub_name in path[1:]:
                key = (main.id, sub_name)
                if key in seen_subs:
                    continue
                seen_subs.add(key)

                stmt = select(SubCategory).where(
                    SubCategory.main_category_id == main.id,
                    SubCategory.name == sub_name,
                )
                sub = (await self.session.execute(stmt)).scalar_one_or_none()
                if sub is None:
                    self.session.add(
                        SubCategory(main_category_id=main.id, name=sub_name)
                    )

        await self.session.commit()

    async def get_id_by_names(
        self, main_name: str, sub_name: str,
    ) -> int | None:
        stmt = (
            select(SubCategory.id)
            .join(MainCategory, SubCategory.main_category_id == MainCategory.id)
            .where(MainCategory.name == main_name, SubCategory.name == sub_name)
        )
        row = (await self.session.execute(stmt)).first()
        return row[0] if row else None