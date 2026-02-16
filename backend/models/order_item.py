import uuid
from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.db.base import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"))

    product_id = Column(UUID(as_uuid=True))
    product_name = Column(String)
    product_price = Column(Float)

    quantity = Column(Integer)
    subtotal = Column(Float)

    order = relationship("Order", back_populates="items")
