import os
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from config import DATABASE_URL

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    optimizations = relationship("Optimization", back_populates="user")

class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text)
    unit_cost = Column(Float, nullable=False)
    storage_cost = Column(Float, nullable=False)
    shortage_penalty = Column(Float, nullable=False)
    min_order_quantity = Column(Float, default=0)
    max_order_quantity = Column(Float)
    lead_time = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    historical_demands = relationship("HistoricalDemand", back_populates="material")
    optimizations = relationship("Optimization", back_populates="material")

class HistoricalDemand(Base):
    __tablename__ = 'historical_demand'

    id = Column(Integer, primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    date = Column(Date, nullable=False)
    demand_quantity = Column(Float, nullable=False)
    actual_cost = Column(Float)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    material = relationship("Material", back_populates="historical_demands")

class Optimization(Base):
    __tablename__ = 'optimizations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    material_id = Column(Integer, ForeignKey('materials.id'), nullable=False)
    name = Column(String(100), nullable=False)
    horizon = Column(Integer, nullable=False)
    initial_inventory = Column(Float, nullable=False)
    max_inventory = Column(Float, nullable=False)
    max_order = Column(Float, nullable=False)
    costs = Column(JSON, nullable=False)
    demand_params = Column(JSON, nullable=False)
    status = Column(String(20), default='pending')
    total_cost = Column(Float)
    solution_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="optimizations")
    material = relationship("Material", back_populates="optimizations")
    optimal_policies = relationship("OptimalPolicy", back_populates="optimization")
    results = relationship("OptimizationResult", back_populates="optimization")

class OptimalPolicy(Base):
    __tablename__ = 'optimal_policies'

    id = Column(Integer, primary_key=True)
    optimization_id = Column(Integer, ForeignKey('optimizations.id'), nullable=False)
    period = Column(Integer, nullable=False)
    reorder_point = Column(Float, nullable=False)
    order_up_to_level = Column(Float, nullable=False)
    expected_cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    optimization = relationship("Optimization", back_populates="optimal_policies")

class OptimizationResult(Base):
    __tablename__ = 'optimization_results'

    id = Column(Integer, primary_key=True)
    optimization_id = Column(Integer, ForeignKey('optimizations.id'), nullable=False)
    period = Column(Integer, nullable=False)
    inventory_level = Column(Float, nullable=False)
    optimal_order = Column(Float, nullable=False)
    expected_demand = Column(Float, nullable=False)
    expected_holding_cost = Column(Float, nullable=False)
    expected_shortage_cost = Column(Float, nullable=False)
    total_period_cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    optimization = relationship("Optimization", back_populates="results")


def init_db(db_url: str = None):
    """
    Inicializa la conexión a la base de datos y crea las tablas.
    """
    url = db_url or DATABASE_URL
    engine = create_engine(url)
    Base.metadata.create_all(engine)
    return engine


def get_session(engine=None):
    """
    Devuelve una sesión de SQLAlchemy ligada al engine.
    """
    if engine is None:
        engine = init_db()
    Session = sessionmaker(bind=engine)
    return Session()
