from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer,
                primary_key=True,
                autoincrement=True
                )
    delete = Column(Integer,
                    default=1)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)

    def set_attrs(self, attrs):
        for k, v in attrs.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)


hero_constellations = Table('hero_constellations',
                            Base.metadata,
                            Column('hero_id',
                                   Integer,
                                   ForeignKey('hero.id')),
                            Column('constellation_id',
                                   Integer,
                                   ForeignKey('constellation.id')),
                            info={'bind_key': 'e7db'})

constellation_catalyst = Table('constellation_catalysts',
                               Base.metadata,
                               Column('constellation_id',
                                      Integer,
                                      ForeignKey('constellation.id')),
                               Column('catalyst_id',
                                      Integer,
                                      ForeignKey('catalyst.id')),
                               info={'bind_key': 'e7db'})

catalyst_shop = Table('catalyst_shops', Base.metadata,
                      Column('catalyst_id', Integer, ForeignKey('catalyst.id')),
                      Column('shop_id', Integer, ForeignKey('shop.id')),
                      info={'bind_key': 'e7db'})


class Nicename(BaseModel):
    __tablename__ = 'nicename'
    __bind_key__ = 'e7db'
    nicename = Column(String(64))
    hero_id = Column(Integer, ForeignKey('hero.id'))
    constellation = relationship('Hero',
                                 lazy='subquery',
                                 backref='nicenames'
                                 )

    def keys(self):
        return 'nicename'

    def __repr__(self):
        return f'{self.nicename}'


class Hero(BaseModel):
    __tablename__ = 'hero'
    __bind_key__ = 'e7db'
    heroname = Column(String(64))
    constellation = relationship('Constellation', secondary=hero_constellations, backref='heros')
    nicename = relationship('Nicename', backref='heros')

    def keys(self):
        return 'heroname'

    def __repr__(self):
        return f'{self.heroname}'


class Constellation(BaseModel):
    __bind_key__ = 'e7db'
    __tablename__ = 'constellation'
    constellation = Column(String(16))
    # 反查询英雄表
    hero = relationship('Hero',
                        lazy='subquery',
                        secondary=hero_constellations,
                        backref=backref('constellations', lazy=True)
                        )
    # 反查询 催化剂表
    catalyst = relationship('Catalyst',
                            lazy='subquery',
                            secondary=constellation_catalyst,
                            backref=backref('constellations', lazy=True)
                            )

    def __repr__(self):
        return f'{self.constellation}'


class Catalyst(BaseModel):
    __bind_key__ = 'e7db'
    __tablename__ = 'catalyst'
    catalyst = Column(String(16))
    # qb的图片地址
    qbaddr1 = Column(String(64))
    # web端的图片地址
    webaddr2 = Column(String(64))
    # 反查询星座表
    constellation = relationship('Constellation',
                                 lazy='subquery',
                                 secondary=constellation_catalyst,
                                 backref=backref('catalysts', lazy=True)
                                 )
    # 反查询 商店表
    shop = relationship('Shop',
                        lazy='subquery',
                        secondary=catalyst_shop,
                        backref=backref('catalysts', lazy=True)
                        )

    def __repr__(self):
        return f'{self.catalyst}'


class Shop(BaseModel):
    __bind_key__ = 'e7db'
    __tablename__ = 'shop'
    shop = Column(String(32))
    # 反查询 催化剂表
    catalyst = relationship('Catalyst',
                            lazy='subquery',
                            secondary=catalyst_shop,
                            backref=backref('shops', lazy=True)
                            )

    def __repr__(self):
        # 打印结果  商店
        return f'{self.shop}'
