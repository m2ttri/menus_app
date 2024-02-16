import uuid

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str


class Menu(BaseModel):
    title: str
    description: str


class MenuIn(BaseModel):
    title: str
    description: str


class MenuListOut(MenuIn):
    id: uuid.UUID


class MenuOut(MenuIn):
    id: uuid.UUID
    submenus_count: int | None = 0
    dishes_count: int | None = 0


class Submenu(BaseModel):
    title: str
    description: str


class SubmenuIn(BaseModel):
    title: str
    description: str


class SubmenuListOut(SubmenuIn):
    id: uuid.UUID


class SubmenuOut(SubmenuIn):
    id: uuid.UUID
    dishes_count: int | None = 0


class Dish(BaseModel):
    title: str
    description: str
    price: str


class DishIn(BaseModel):
    title: str
    description: str
    price: str


class DishOut(DishIn):
    id: uuid.UUID


class DishOutExtra(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    price: str


class SubmenuOutExtra(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    dishes: list[DishOutExtra]


class MenuAllOut(MenuIn):
    id: uuid.UUID
    submenu: list[SubmenuOutExtra]
