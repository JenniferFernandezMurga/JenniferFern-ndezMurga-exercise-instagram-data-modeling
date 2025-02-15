 
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship, declarative_base, Mapped
from eralchemy2 import render_er
from typing import List

Base = declarative_base()

# Tabla de asociación para seguidores
followers = Table('followers', Base.metadata,
    Column('user_from_id', Integer, ForeignKey('users.id')),
    Column('user_to_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = Column(Integer, primary_key=True)  
    username: Mapped[str] = Column(String, nullable=False)
    firstname: Mapped[str] = Column(String, nullable=False)
    lastname: Mapped[str] = Column(String, nullable=False)
    email: Mapped[str] = Column(String, nullable=False, unique=True)
    
    followers_from: Mapped[List["Follower"]] = relationship("Follower", 
        foreign_keys=[followers.c.user_from_id], back_populates='user_from')
    followers_to: Mapped[List["Follower"]] = relationship("Follower", 
        foreign_keys=[followers.c.user_to_id], back_populates='user_to')
    
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="user")

# class Follower(Base):
#     __tablename__ = 'follower'
    
#     user_from_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     user_to_id: Mapped[int] = Column(Integer, ForeignKey('users.id'), primary_key=True)
    
#     user_from: Mapped[User] = relationship("User", foreign_keys=[user_from_id], back_populates="followers_from")
#     user_to: Mapped[User] = relationship("User", foreign_keys=[user_to_id], back_populates="followers_to")

class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = Column(Integer, primary_key=True)
    comment_text: Mapped[str] = Column(String, nullable=False)
    author_id: Mapped[int] = Column(ForeignKey('users.id'), nullable=False)
    
    user: Mapped[User] = relationship(back_populates="comments")
    post_id: Mapped[int] = Column(ForeignKey('posts.id'), nullable=False)
    post: Mapped["Post"] = relationship("Post", back_populates="comments")

class Post(Base):
    __tablename__ = 'posts'
    id: Mapped[int] = Column(Integer, primary_key=True)
    user_id: Mapped[int] = Column(ForeignKey('users.id'), nullable=False)
    user: Mapped[User] = relationship(back_populates="posts")
    
    multimedia: Mapped[List["Media"]] = relationship("Media", back_populates="post")
    comments: Mapped[List[Comment]] = relationship("Comment", back_populates="post")

class Media(Base):
    __tablename__ = 'media'
    id: Mapped[int] = Column(Integer, primary_key=True)
    type: Mapped[str] = Column(Enum('image', 'video'), nullable=False)
    url: Mapped[str] = Column(String, nullable=False)
    post_id: Mapped[int] = Column(ForeignKey('posts.id'), nullable=False)
    post: Mapped[Post] = relationship(back_populates="multimedia")

    def to_dict(self):
        return {
            # 'id': self.id,
            # 'type': self.type,
            # 'url': self.url,
            # 'post_id': self.post_id
        }

# Generar el diagrama
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem generating the diagram")
    raise e