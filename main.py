import email
from typing import List
from typing import Optional
from flask import session
# from requests import Session
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


engine = create_engine("sqlite:///database/data.db", echo=True)


class Base(DeclarativeBase):
    pass


UserCourses = Table(
    "userandcourses",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("userId", ForeignKey("user.id")),
    Column("subjectId", ForeignKey("course.id"))
)

class Lecture(Base):
    __tablename__ = "lectures"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    path: Mapped[str] = mapped_column(String())

    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(50))
    password_hash: Mapped[str] = mapped_column(String())
    
    courses: Mapped[List["Courses"]] = relationship(secondary=UserCourses, back_populates="users")


class Subject(Base):
    __tablename__ = "subject"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    
    courses : Mapped[List["Courses"]] = relationship(back_populates="subject")

class Courses(Base):
    __tablename__ = "course"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    age_group: Mapped[str] = mapped_column(String(10))
    
    lectures: Mapped[List["Lecture"]] = relationship()
    subject_id: Mapped[int] = mapped_column(ForeignKey("subject.id"))
    subject: Mapped["Subject"] = relationship(back_populates="courses")
    users: Mapped[List["User"]] = relationship(secondary=UserCourses, back_populates="courses")
    

Base.metadata.create_all(engine)



with Session(engine) as session:
    test_user = User(name="Joe", email="gibrish@gmail.com",password_hash="shdgh", courses=[Courses(name="python", age_group="teen", subject = Subject(name="cs")), Courses(name="html",  age_group="teen", subject = Subject(name="cs"))])
    session.add(test_user)
    session.commit()


    # 
    # 