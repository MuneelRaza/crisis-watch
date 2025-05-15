from prefect import flow, task
from data_ingestion.reliefweb_fetcher import get_relief_web_data
from data_ingestion.gnews_fetcher import get_gnews_data
from data_transformation.ner_script import run_ner_on_texts



# Optional: save_json can be a helper to store results

@task
def fetch_reliefweb():
    print("Fetching articles from ReliefWeb...")
    return get_relief_web_data()

@task
def fetch_gnews():
    print("Fetching articles from GNews...")
    return get_gnews_data()

@task
def apply_ner(articles):
    print("Applying NER on articles...")
    return run_ner_on_texts(articles)


@flow(name="CrisisWatch Pipeline")
def crisiswatch_flow():
    fetch_reliefweb()
    fetch_gnews()
    


if __name__ == "__main__":
    crisiswatch_flow()
