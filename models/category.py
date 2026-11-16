from sqlalchemy import String,ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from core.database import Base


class MainCategory(Base):
    # Основная категория: Farming, Mining, Combat, Woods & Fishes, Oddities
    __tablename__ = 'main_categories'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    
    subcategories: Mapped[List['SubCategory']] = relationship(
        back_populates ='main_category',
        cascade= 'all, delete-orphan',
    )
    
class SubCategory(Base):
    # Подкатегория внутри основной: "Wheat & Seeds", "Diamond" и т.д
    __tablename__ = 'sub_categories'
    
    __table_args__ = (
        UniqueConstraint('main_category_id', 'name', name = 'uq_subcat_in_main')),
    
    id: Mapped[int] = mapped_column(primary_key=True)
    main_category_id: Mapped[int] = mapped_column(ForeignKey('main_categories.id', ondelete='CASCADE'), index=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    
    main_category: Mapped['MainCategory'] = relationship(back_populates='subcategories')
    