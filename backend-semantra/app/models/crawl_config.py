from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class CrawlConfig(Base):
    __tablename__ = "crawl_configs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    
    # Paramètres de performance
    max_urls = Column(Integer, default=1000000)
    crawl_speed = Column(String, default="medium")  # slow, medium, fast
    delay_between_requests = Column(Integer, default=1000)  # ms
    retry_attempts = Column(Integer, default=3)
    timeout = Column(Integer, default=30)  # seconds
    
    # Configuration anti-blocage
    user_agent = Column(String, default="Semantra Bot 1.0")
    user_agents_rotation = Column(JSON, default=[])
    proxy_enabled = Column(Boolean, default=False)
    proxy_list = Column(JSON, default=[])
    
    # Configuration adaptative
    adaptive_speed = Column(Boolean, default=True)
    adaptive_user_agent = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    user = relationship("User", back_populates="crawl_configs")
    url_filters = relationship("UrlFilter", back_populates="crawl_config")
    
    def __repr__(self):
        return f"<CrawlConfig(id={self.id}, name={self.name})>" 