import os
import sys
from typing import List

from sqlalchemy import create_engine, Enum as SaEnum, ForeignKey, Integer, String, Column
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from eralchemy2 import render_er

Base = declarative_base()

# Tabla de asociación
# estudiante_curso = Table('estudiante_curso', Base.metadata,
#     Column('estudiante_id', Integer, ForeignKey('estudiantes.id')),
#     Column('curso_id', Integer, ForeignKey('cursos.id'))
# )

#Tabla de asociación
followers= Table('followers', Base.metadata,
    Column('user_from_id', Integer, ForeignKey('users.id')),
    Column('user_to_id', Integer, ForeignKey('users.id')))


class Follower(Base):
    __tablename__ = 'followers'
    # id: Mapped[int] = mapped_column(primary_key=True) 
    # user_from_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)  # Seguidos por usuario
    # user_to_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)  # Seguidores a usuario
    user_from_id: Mapped["User"] = relationship("User", foreign_keys=[user_from_id], back_populates="followers_from")
    user_to_id: Mapped["User"] = relationship("User", foreign_keys=[user_to_id], back_populates="followers_to")


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)  # va a comment, a post y a follower
    username: Mapped[str] = mapped_column(nullable=False)
    firstname: Mapped[str] = mapped_column(nullable=False)
    lastname: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    followers: Mapped[List["Follower"]] = relationship("Follower", secondary=followers, back_populates='users') #Sobra lo de secondary????
    comments: Mapped[List["Comment"]] = relationship(back_populates="User")
    posts: Mapped[List["Post"]] = relationship(back_populates="User")

#1:N 1 usuario muchos comentarios
class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)  # Viene desde user
    users: Mapped["User"] = relationship(back_populates="comments")
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)  # viene desde post
    posts: Mapped["Post"] = relationship("Post", back_populates="comments")

#1:N 1 usuario muchos posts, 1 post muchos comentarios
class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True)  # Clave primaria
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    users: Mapped["User"] = relationship(back_populates="posts")
    multimedia: Mapped[List["Media"]] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="posts")


#1:N 1 post muchos media
class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[Enum] = mapped_column(Enum('image', 'video'), nullable=False)  # Especificar tipos
    url: Mapped[str] = mapped_column(nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'), nullable=False)
    posts: Mapped["Post"] = relationship(back_populates="multimedia")


    def to_dict(self):
        return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e
