from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean, create_engine
from sqlalchemy.orm import relationship,  declarative_base, sessionmaker

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


class Audition(Base):
    __tablename__ = 'auditions'

    id = Column(Integer(), primary_key=True)
    actor = Column(String)
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())
    role_id = Column(Integer(), ForeignKey('roles.id'))

    role = relationship('Role', back_populates='auditions')

    def __repr__(self):
        return f'(Actor: {self.actor}, Location: {self.location}, Phone: {self.phone})'

    def call_back(self):
        self.hired = True
        session.commit()
        return 'Done'


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    auditions = relationship('Audition', back_populates='role')

    def __repr__(self):
        return self.name

    @property
    def actors(self):
        return [audition.actor for audition in self.auditions]

    @property
    def locations(self):
        return [audition.location for audition in self.auditions]

    def lead(self):
        for audition in self.auditions:
            if (audition.hired == True):
                return audition
        return 'no actor has been hired for this role'

    def understudy(self):
        hired = []
        for audition in self.auditions:
            if (audition.hired == True):
                hired.append(audition)
        if (len(hired) >= 2):
            return hired[1]
        return 'no actor has been hired for understudy for this role'


engine = create_engine('sqlite:///theater.db')
Session = sessionmaker(bind=engine)
session = Session()


# audition1 = Audition(actor='John', location='Theater A',
#                      phone=1234567890, hired=True)
# audition2 = Audition(actor='Emily', location='Theater B',
#                      phone=9876543210, hired=False)
# audition3 = Audition(actor='Michael', location='Theater A',
#                      phone=5555555555, hired=True)

# role1 = Role(name='Hero')
# role2 = Role(name='Villain')

# session.add_all([audition1, audition2, audition3, role1, role2])
# session.commit()

# audition1.role_id = role1.id
# audition2.role_id = role2.id
# audition3.role_id = role1.id

e = session.query(Audition).filter_by(actor='Emily').first()
villain = session.query(Role).filter_by(name='Villain').first()


print(villain.understudy())
