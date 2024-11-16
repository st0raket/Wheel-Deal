from sqlalchemy import (
    Column, Integer, String, Float, Date, ForeignKey
)
from sqlalchemy.orm import relationship
from database1 import Base, engine

# Dimension Tables

class CarMake(Base):
    __tablename__ = "Car_make"

    ID = Column(Integer, primary_key=True, index=True)
    car_make = Column(String, unique=True, nullable=False)

    # Relationship to Model
    models = relationship("Model", back_populates="car_make")


class Model(Base):
    __tablename__ = "Model"

    ID = Column(Integer, primary_key=True, index=True)
    model = Column(String, unique=True, nullable=False)
    Car_make_id = Column(Integer, ForeignKey("Car_make.ID"), nullable=False)

    # Relationship back to CarMake
    car_make = relationship("CarMake", back_populates="models")


class FuelType(Base):
    __tablename__ = "Fuel_type"

    ID = Column(Integer, primary_key=True, index=True)
    fuel_type = Column(String, unique=True, nullable=False)


class Color(Base):
    __tablename__ = "Color"

    ID = Column(Integer, primary_key=True, index=True)
    color = Column(String, unique=True, nullable=False)


class BodyStyle(Base):
    __tablename__ = "Body_style"

    ID = Column(Integer, primary_key=True, index=True)
    body_style = Column(String, unique=True, nullable=False)


class Transmission(Base):
    __tablename__ = "Transmission"

    ID = Column(Integer, primary_key=True, index=True)
    transmission = Column(String, unique=True, nullable=False)


class Option(Base):
    __tablename__ = "Options"

    ID = Column(Integer, primary_key=True, index=True)
    option = Column(String, unique=True, nullable=False)


class Damage(Base):
    __tablename__ = "Damage"

    ID = Column(Integer, primary_key=True, index=True)
    damage = Column(String, unique=True, nullable=False)

# Fact Table

class Cars(Base):
    __tablename__ = "Cars"

    ID = Column(Integer, primary_key=True, index=True)
    Model_ID = Column(Integer, ForeignKey("Model.ID"), nullable=False)
    Fuel_type_ID = Column(Integer, ForeignKey("Fuel_type.ID"), nullable=False)
    Color_ID = Column(Integer, ForeignKey("Color.ID"), nullable=False)
    Body_style_ID = Column(Integer, ForeignKey("Body_style.ID"), nullable=False)
    Transmission_ID = Column(Integer, ForeignKey("Transmission.ID"), nullable=False)
    Options_ID = Column(Integer, ForeignKey("Options.ID"), nullable=False)
    Damage_ID = Column(Integer, ForeignKey("Damage.ID"), nullable=False)

    Year = Column(Integer, nullable=False)
    Mileage = Column(Float, nullable=False)
    Horsepower = Column(Float, nullable=False)
    Website_post_date = Column(Date, nullable=False)
    Sell_date = Column(Date, nullable=True)
    Num_of_prev_owners = Column(Integer, nullable=False)
    Estimated_price = Column(Float, nullable=False)

    # Relationships
    model = relationship("Model")
    fuel_type = relationship("FuelType")
    color = relationship("Color")
    body_style = relationship("BodyStyle")
    transmission = relationship("Transmission")
    options = relationship("Option")
    damage = relationship("Damage")

# Create all tables
Base.metadata.create_all(engine)
