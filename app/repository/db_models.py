from datetime import datetime, UTC

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.repository.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str]= mapped_column(nullable=False)
    password: Mapped[str]= mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(
        nullable=False,
        default=lambda: datetime.now(UTC).isoformat()
    )
    jti: Mapped[str] = mapped_column(nullable=True)


class Tags(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False
    )

    name: Mapped[str]= mapped_column(nullable=False)

    user: Mapped["User"] = relationship(
    )

    Transactions: Mapped[list["Transactions"]] = relationship(
        secondary="transaction_tags",
        back_populates="Tags",
    )

class Budget(Base):
    __tablename__ = "budget"


    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)

    limit: Mapped[float] = mapped_column(nullable=False)

    @property
    def current_sum(self):
        return sum(
            transaction.sum
            for transaction in self.transactions
        )

    colour:Mapped[str] = mapped_column(nullable=True)

    Transactions:Mapped[list["Transactions"]] = relationship()


class Transactions(Base):
    __tablename__ = "transaction"


    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)

    sum: Mapped[float] = mapped_column(nullable=False)

    description:Mapped[str] = mapped_column(nullable=False)

    categoryId: Mapped[int] = mapped_column(
        ForeignKey("budget.id", ondelete="CASCADE"),
        nullable=True
    )

    Tags: Mapped[list["Tags"]] = relationship(
        secondary="transaction_tags",
        back_populates="Transactions",
    )

class Goals(Base):
    __tablename__ = "goals"


    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    nullable=False,
    )
    name: Mapped[str] = mapped_column(nullable=False)

    dueDate: Mapped[str] = mapped_column(nullable=True)

    targetSum: Mapped[float] = mapped_column(nullable=False)

    currentSum: Mapped[float] = mapped_column(nullable=True)
    # @property
    # def current_sum(self):
    #     return sum(
    #         transaction.sum
    #         for transaction in self.transactions
    #     )
    colour: Mapped[str] = mapped_column(nullable=True)
    description:Mapped[str] = mapped_column(nullable=False)

    # Transactions:Mapped[list["Transactions"]] = relationship()


class TransactionTags(Base):
    __tablename__ = "transaction_tags"

    transaction_id: Mapped[int] = mapped_column(
        ForeignKey("transaction.id", ondelete="CASCADE"),
    nullable=False,
    primary_key=True
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
    nullable=False,
    primary_key=True
    )



