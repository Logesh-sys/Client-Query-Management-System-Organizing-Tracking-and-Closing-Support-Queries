from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    # Database connection URL
    Data_base_url = "postgresql://postgres:Logesh%401234@localhost:5432/Query_portal"
    engine = create_engine(Data_base_url)
    sessionLocal = sessionmaker(bind=engine) # This allows you to create session objects for transactions

    # Test connection
    with engine.connect() as conn:
        print("Database connected successfully")

except Exception as e:
    print("Database connection failed:",e) # Catch and print any exceptions during connection

