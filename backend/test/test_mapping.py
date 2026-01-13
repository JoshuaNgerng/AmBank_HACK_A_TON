from collections.abc import Mapping
from datetime import date, datetime
from decimal import Decimal
import json
from sqlalchemy import Numeric, Date, Integer, DateTime
from sqlalchemy.orm import class_mapper, Mapped, mapped_column, declarative_base

Base = declarative_base()

class TableBase(Base):
    """Base class for all database tables with common columns."""
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, onupdate=datetime.now, nullable=False)

    # Use this method to convert model instance to a dict (for API responses)
    def to_dict(self) -> dict:
        """Convert model to dictionary."""
        result = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime):
                result[column.name] = value.isoformat()
            else:
                result[column.name] = value
        return result  

class IncomeStatement(TableBase):
    __tablename__ = "income_statements"

    revenue: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    gross_profit: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    operating_expenses: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    operating_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    finance_costs: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    profit_before_tax: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    tax: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    net_income: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)

    eps: Mapped[Decimal] = mapped_column(Numeric(10, 4), nullable=False)

    period: Mapped[date] = mapped_column(Date, nullable=False)

def from_dict(model_class, data: dict):
    """
    Create a SQLAlchemy model instance from a dict.
    Uses __table__ and class_mapper instead of sqlalchemy.inspect.
    Supports nested relationships.
    """
    if data is None:
        return None

    obj = model_class()

    # ---- Columns ----
    column_names = {c.name for c in model_class.__table__.columns}

    for name in column_names:
        if name in data:
            setattr(obj, name, data[name])

    # ---- Relationships ----
    mapper = class_mapper(model_class)

    for rel in mapper.relationships:
        key = rel.key
        if key not in data:
            continue

        value = data[key]
        target = rel.mapper.class_

        # one-to-many / many-to-many
        if rel.uselist:
            if isinstance(value, list):
                children = [
                    from_dict(target, item)
                    for item in value
                    if isinstance(item, Mapping)
                ]
                setattr(obj, key, children)

        # many-to-one / one-to-one
        else:
            if isinstance(value, Mapping):
                setattr(obj, key, from_dict(target, value))

    return obj


# with open('fin-res.json', 'r') as f:
#     data = json.load(f)

# res = from_dict(IncomeStatement, data[0])
# print(res.to_dict())


test = IncomeStatement()
res = getattr(test, 'id')
print(res)
setattr(test, 'id', 123)
print(test.to_dict())
