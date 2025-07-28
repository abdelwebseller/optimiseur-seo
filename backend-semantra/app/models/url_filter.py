from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class UrlFilter(Base):
    __tablename__ = "url_filters"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    crawl_config_id = Column(String, ForeignKey("crawl_configs.id"), nullable=False)
    
    # Type de filtre
    filter_type = Column(String, nullable=False)  # pattern, regex, subdomain, folder
    
    # Valeur du filtre
    filter_value = Column(Text, nullable=False)
    
    # S'il s'agit d'un filtre d'exclusion
    is_exclude = Column(Boolean, default=False)
    
    # Ordre d'application
    priority = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    crawl_config = relationship("CrawlConfig", back_populates="url_filters")
    
    def __repr__(self):
        return f"<UrlFilter(id={self.id}, type={self.filter_type}, value={self.filter_value})>" 