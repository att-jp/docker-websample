#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import sqlalchemy
import os
import re
import sys

Base = declarative_base()

class Users(Base):
    __tablename__ = 'testtable01'

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable = False)


class MySQL():
    def __init__(self, **argv):
        user   = argv.get('user')
        passwd = argv.get('passwd')
        host   = argv.get('host')
        db     = argv.get('db')
        self.url = "mysql+pymysql://{}:{}@{}/{}?charset=utf8".format(user, passwd, host, db)
        self.engine = sqlalchemy.create_engine(self.url, echo=True)
        self.session = sqlalchemy.orm.sessionmaker(bind=self.engine)()


if __name__ == '__main__':
    argv = sys.argv
    s = MySQL(user=argv[1], passwd=argv[2], host=argv[3], db=argv[4])
    print s.url
    r = s.session.query(Users).all()
    for v in r:
        if not v:
            continue
        print v.name

