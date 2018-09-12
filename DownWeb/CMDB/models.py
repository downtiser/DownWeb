from django.db import models
# Create your models here.
# from sqlalchemy import create_engine, func
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, String, CHAR, Date, ForeignKey
# from sqlalchemy.orm import sessionmaker, relationship
#
# engine = create_engine('mysql+mysqlconnector://root:gu996080@localhost/cmdb', encoding='utf-8')
# Base = declarative_base()
#
# class HostInfo(Base):
#     __tablename__ = 'host_info'
#     id = Column(Integer, primary_key=True)
#     region = Column(String(32), nullable=False)
#     host_name = Column(String(64), nullable=False)
#     host_ip = Column(String(64), nullable=False)
#     host_port = Column(String(32), nullable=False)
#     user_id = Column(Integer, ForeignKey('user_info.id'), nullable=False)
#     statue = Column(String(64), nullable=False)
#     os = Column(String(64), nullable=False)
#     users_info = relationship('UserInfo', backref='your_host_info')
#
# class UserInfo(Base):
#     __tablename__ = 'user_info'
#     id = Column(Integer, primary_key=True)
#     user_name = Column(String(128), unique=True, nullable=False)
#     password = Column(String(128), nullable=False)
#
# session_class = sessionmaker()
# session = session_class(bind=engine)

class UserInfo(models.Model):
    uid = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=64, null=False, unique=True)
    password = models.CharField(max_length=128, null=False)
    ctime = models.DateTimeField(auto_now_add=True, null=True)
    uptime = models.DateTimeField(auto_now=True, null=True)

class HostInfo(models.Model):
    nid = models.AutoField(primary_key=True)
    region = models.CharField(max_length=32, null=False)
    host_name = models.CharField(max_length=64, null=False)
    host_ip = models.GenericIPAddressField(protocol='both')
    host_port = models.IntegerField(null=False)
    statue = models.CharField(max_length=64, null=False, default='running')
    os = models.CharField(max_length=128, null=False)
    user_info = models.ForeignKey('UserInfo', to_field='uid', on_delete=models.PROTECT)

class Applications(models.Model):
    aid = models.AutoField(primary_key=True)
    caption = models.CharField(max_length=64, null=False)
    host = models.ManyToManyField('HostInfo')
