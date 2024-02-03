import uuid

from pydantic import BaseModel


class Menu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuIn(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class MenuOut(MenuIn):
    id: uuid.UUID
    submenus_count: int | None = 0
    dishes_count: int | None = 0


class Submenu(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SubmenuIn(BaseModel):
    title: str
    description: str

    class Config:
        orm_mode = True


class SubmenuOut(SubmenuIn):
    id: uuid.UUID
    dishes_count: int | None = 0


class Dish(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishIn(BaseModel):
    title: str
    description: str
    price: str

    class Config:
        orm_mode = True


class DishOut(DishIn):
    id: uuid.UUID
