from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    """
    请求模型验证：
    email:
    password:
    """
    password: str


class User(UserBase):
    """
    响应模型：
    id:
    email:
    is_active
    并且设置orm_mode与之兼容
    """
    id: int
    is_active: bool

    class Config:
        orm_mode = True