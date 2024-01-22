from sqlalchemy import Column, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid


class Menu(Base):
    """Модель меню"""
    __tablename__ = "menus"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    submenus = relationship("SubMenu", back_populates="menu", cascade="all, delete-orphan")


class SubMenu(Base):
    """Модель подменю"""
    __tablename__ = "submenus"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))
    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")


class Dish(Base):
    """Модель блюда"""
    __tablename__ = "dishes"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, unique=True, nullable=False)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"), index=True, nullable=False)
    submenu = relationship("SubMenu", back_populates="dishes")
