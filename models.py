from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime
from random_words import RandomNicknames
from random import randint, choices
from math import floor
from util import roll

rn = RandomNicknames()

Base = declarative_base()

class Fighter(Base):
    __tablename__ = 'fighter'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    stre = Column(Integer)
    con = Column(Integer)
    dex = Column(Integer)
    int = Column(Integer)
    wis = Column(Integer)
    cha = Column(Integer)

    def __init__(self):
        self.first_name = rn.random_nick()
        self.last_name = rn.random_nick()
        self.stre = roll('3d6')
        self.con = roll('3d6')
        self.dex = roll('3d6')
        self.int = roll('3d6')
        self.wis = roll('3d6')
        self.cha = roll('3d6')
    
    def mod(self, num):
        return floor(num/2.0) - 5

    def perform(self):
        effort = []
        effort.append(roll('1d20') + self.mod(self.stre))
        effort.append(roll('1d20') + self.mod(self.con))
        effort.append(roll('1d20') + self.mod(self.dex))
        effort.append(roll('1d20') + self.mod(self.int))
        effort.append(roll('1d20') + self.mod(self.wis))
        effort.append(roll('1d20') + self.mod(self.cha))
        return effort

    def all_bouts(self):
        return self.bouts_a + self.bouts_d

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def __repr__(self):
        return "%s %s %d/%d/%d/%d/%d/%d" % (self.first_name, self.last_name, self.stre, self.con, self.dex, self.int, self.wis, self.cha)

class Bout(Base):
    __tablename__ = 'bout'
    id = Column(Integer, primary_key=True)
    fighter1_id = Column(Integer, ForeignKey('fighter.id'))
    fighter1 = relationship(Fighter, foreign_keys=[fighter1_id], backref='bouts_a')
    fighter2_id = Column(Integer, ForeignKey('fighter.id'))
    fighter2 = relationship(Fighter, foreign_keys=[fighter2_id], backref='bouts_d')
    announced_at = Column(DateTime)
    held_at = Column(DateTime)
    score = Column(Integer)
    def __init__(self, fighter1, fighter2):
        self.fighter1 = fighter1
        self.fighter2 = fighter2
        self.announced_at = datetime.now()
        self.held_at = None
        # Positive for fighter1 win, negative for fighter1 loss
        self.score = None

    def hold_bout(self):
        self.score = 0
        self.held_at = datetime.now()
        print("%s vs. %s! Begin!" % (self.fighter1, self.fighter2))
        f1 = self.fighter1.perform()
        f2 = self.fighter2.perform()

        for round in range(0,6):
            if f1[round] > f2[round]:
                self.score += 1
            elif f2[round] > f1[round]:
                self.score -= 1
        return self.score

    def announce_winner(self):
        if self.score is None:
            return "The bout has not begun."
        elif self.score > 0:
            return "Fighter 1, %s, is the victor!" % self.fighter1
        elif self.score < 0:
            return "Fighter 2, %s, is the victor!" % self.fighter2
        else:
            return "It was a tie!"