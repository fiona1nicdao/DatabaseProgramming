class Base(DeclarativeBase):
    pass
association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("left_table.id"),primary_key=True),
    Column("right_id", ForeignKey("right_table.id"),primary_key = True),
)

class Parent(Base):
    __tablename__ = "left_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[List[Child]] = relationship(
        secondary=association_table, back_populates="parents"
    )

class Child(Base):
    __tablename__ = "right_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    parents: Mapped[List[Parent]] = relationship(
        secondary=association_table, back_populates="children"
    )