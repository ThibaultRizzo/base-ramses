from sqlalchemy import create_engine
url= f"postgresql://test:test@localhost:5434/ramses"
engine= create_engine(url)
request = "select id from instrument"

with engine.connect() as conn:
    result= conn.execute(request)
    print(result.all())