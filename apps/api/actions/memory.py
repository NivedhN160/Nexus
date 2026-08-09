from packages.retrieval.loop import retrieve_and_evaluate

def search_memory(args: dict):
    query = args.get("query", "")
    return retrieve_and_evaluate(query)
