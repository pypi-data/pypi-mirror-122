# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from outflow.core.db import Model


class Configuration(Model):
    """
    Stores a run configuration
    """

    id = Column(Integer, primary_key=True)
    config = Column(JSONB, nullable=False)
    settings = Column(JSONB, nullable=False)
    # TODO add cli args
    hash = Column(String(64), nullable=False, unique=True)
    runs = relationship("Run", back_populates="configuration")
