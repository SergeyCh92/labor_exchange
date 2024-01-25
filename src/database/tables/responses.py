import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database.engine import Base


class Response(Base):
    __tablename__ = "responses"
    # задаем ограничение, чтобы кандидат не мог дважды откликнуться на одну и ту же вакансию
    __table_args__ = (sa.UniqueConstraint("user_id", "job_id", name="response_unique_key"),)

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="Идентификатор отклика")
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), comment="Идентификатор пользователя", nullable=False
    )
    job_id = sa.Column(
        sa.Integer, sa.ForeignKey("jobs.id", ondelete="CASCADE"), comment="Идентификатор вакансии", nullable=False
    )
    message = sa.Column(sa.String(500), comment="Сопроводительное письмо")

    user = relationship("User", back_populates="responses")
    job = relationship("Job", back_populates="responses")
