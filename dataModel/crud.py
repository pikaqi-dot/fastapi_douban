from sqlalchemy.orm import Session
import dataModel.schemas
from dataModel.models import User


# 通过id查询用户
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# 新建用户
def db_create_user(db: Session, user: dataModel.schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()  # 提交保存到数据库中
    db.refresh(db_user)  # 刷新
    return db_user