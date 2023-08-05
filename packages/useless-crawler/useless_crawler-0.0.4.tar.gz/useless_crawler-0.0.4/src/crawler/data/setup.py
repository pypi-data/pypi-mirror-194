from .models import metadata
from .database import get_engine

def setup():
    engine = get_engine()
    metadata.create_all(bind=engine)