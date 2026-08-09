from packages.retrieval.loop import retrieve_and_evaluate
from sqlalchemy.orm import Session

def search_memory(args: dict, db: Session):
    query = args.get("query", "")
    return retrieve_and_evaluate(query, db=db)
