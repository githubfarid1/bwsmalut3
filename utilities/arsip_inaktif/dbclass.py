from sqlalchemy import Column, Integer, String, SmallInteger, Text, CHAR
from sqlalchemy.orm import  DeclarativeBase,  relationship
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from settings import *
import uuid

class Base(DeclarativeBase):
    pass

class Bundle(Base):
    __tablename__ = TABLE_PREFIX + BUNDLE_TABLE
    id: Mapped[int] = mapped_column(primary_key=True)
    box_number: Mapped[int] = mapped_column(SmallInteger)
    bundle_number: Mapped[int] = mapped_column(SmallInteger)
    code: Mapped[str] = mapped_column(String(20))
    title: Mapped[str] = mapped_column(Text)
    year: Mapped[str] = mapped_column(CHAR(4),  nullable=True)
    orinot: Mapped[str] = mapped_column(String(10), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)


class Doc(Base):
    __tablename__ = TABLE_PREFIX + DOC_TABLE
    id: Mapped[int] = mapped_column(primary_key=True)
    bundle_id: Mapped[int] = mapped_column(ForeignKey(TABLE_PREFIX + BUNDLE_TABLE + ".id"))
    doc_number: Mapped[int] = mapped_column(SmallInteger)
    doc_count: Mapped[int] = mapped_column(SmallInteger)
    orinot: Mapped[str] = mapped_column(String(10), nullable=True)
    doc_type: Mapped[str] = mapped_column(String(20), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    page_count: Mapped[str] = mapped_column(SmallInteger, nullable=True)
    filesize: Mapped[int] = mapped_column(Integer, nullable=True)
    uuid_id: Mapped[str] = mapped_column(String(36))
    access: Mapped[str] = mapped_column(String(50), nullable=True)

    bundle = relationship("Bundle")
    # comments = relationship("Comment")
