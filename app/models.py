import uuid

from sqlalchemy import Column, ForeignKey, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


# Модель меню
class Menu(Base):
    __tablename__ = 'menus'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    submenus = relationship('SubMenu', back_populates='menu', cascade='all, delete-orphan')


# Модель подменю
class SubMenu(Base):
    __tablename__ = 'submenus'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey('menus.id'))
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu', cascade='all, delete-orphan')


# Модель блюда
class Dish(Base):
    __tablename__ = 'dishes'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Numeric(precision=12, scale=2), nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey('submenus.id'), index=True, nullable=False)
    submenu = relationship('SubMenu', back_populates='dishes')
