from fastapi import FastAPI, Depends
# import dataModel.crud,dataModel.schemas
# from dataModel.database import SessionLocal, engine, Base
# from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from test import doTest,getMoreMovieReview
import json
import os
import uvicorn
app = FastAPI()
# Base.metadata.create_all(bind=engine) #数据库初始化，如果没有库或者表，会自动创建
# def get_db():

#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


def parseJSON():
  if (os.path.exists('data.json') and os.path.isfile('data.json')):
    f = open('data.json', 'r')
    data = json.loads(f.read())
    f.close()
    return data
  return False
def parseMovieReview(page):
  filePath='movieReviewPage/MovieReview{}'.format(page)
  if(os.path.exists(filePath)):
    f=open(filePath,'r')
    data = json.loads(f.read())
    f.close()
    return data
  return False
    
    

# 新建用户
# @app.post("/users/", response_model=dataModel.schemas.User)
# def create_user(user: dataModel.schemas.UserCreate, db: Session = Depends(get_db)):
#     return dataModel.crud.db_create_user(db=db, user=user)

# # 通过id查询用户
# @app.get("/user/{user_id}", response_model=dataModel.schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = dataModel.crud.get_user(db, user_id=user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user
app.add_middleware(
  CORSMiddleware,
  # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
  allow_origins=["*"],
  # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
  allow_credentials=False,
  # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
  allow_methods=["*"],
  # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
  # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
  allow_headers=["*"],
  # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
  # expose_headers=["*"]
  # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
  # max_age=1000
)


@app.get('/force_fetch')
async def 强制更新():
  return (doTest() and "更新成功！") or "更新失败！"


@app.get('/total')
async def 全部数据():
  return parseJSON() or (doTest() and parseJSON()) or "获取数据失败"


@app.get('/movie/lists')
async def 电影分目录列表():
  return (parseJSON() and parseJSON().get('movie',{}).get('lists',False)) \
      or (doTest() and parseJSON().get('movie',{}).get('lists',False)) \
      or "获取数据失败"


@app.get('/movie/top250')
async def 电影top250名():
  return (parseJSON() and parseJSON().get('movie',{}).get('top250',False)) \
      or (doTest() and parseJSON().get('movie',{}).get('top250',False)) \
      or "获取数据失败"


@app.get('/movie/overview')
async def 电影热点总览():
  return (parseJSON() and parseJSON().get('movie',{}).get('overview',False)) \
      or (doTest() and parseJSON().get('movie',{}).get('overview',False)) \
      or "获取数据失败"

@app.get('/movie/review')
async def 影评(page:int=1):
  if(page==1):  
    return (parseJSON() and parseJSON().get('movie',{}).get('reviewBest',False)) \
      or (doTest() and parseJSON().get('movie',{}).get('reviewBest',False)) \
      or "获取数据失败"
  return  parseMovieReview(page) or getMoreMovieReview(page) or "获取影评第{}页失败！".format(page)

@app.get('/book/lists')
async def 图书分目录列表():
  return (parseJSON() and parseJSON().get('book',{}).get('lists',False)) \
      or (doTest() and parseJSON().get('book',{}).get('lists',False)) \
      or "获取数据失败"


@app.get('/group/lists')
async def 小组分目录列表():
  return (parseJSON() and parseJSON().get('group',{}).get('lists',False)) \
      or (doTest() and parseJSON().get('group',{}).get('lists',False)) \
      or "获取数据失败"
if __name__=="__main__":
  uvicorn.run("main:app",host="0.0.0.0",port=8001,reload=True)
  