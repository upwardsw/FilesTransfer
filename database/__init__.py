from sqlalchemy import *
from sqlalchemy.orm import *

from .tables import user,filerecord,userrelationship,files,sendrecord

engine = create_engine(
    'mysql+pymysql://arlen:5609651Wmm!@47.94.138.25:3306/FileSTransfer?charset=utf8', encoding="utf-8", echo=True,
    pool_recycle=21600, pool_size=8, max_overflow=5)
DBSession = sessionmaker(bind=engine)