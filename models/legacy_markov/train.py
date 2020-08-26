import fire
from models.markov.markov_model import MarkovModel
from models.utils.postgres import PostgresStorage


def train(
        model_order: int,
        host: str,
        port=5432,
        user='postgres',
        password='password',
        dbname='habr'
):
    storage = PostgresStorage.connect(
        host=host, port=port, user=user, password=password, dbname=dbname)
    texts_list = storage.get_posts_texts()
    print('Loaded texts: ', len(texts_list))
    markov_model = MarkovModel(order=model_order)
    markov_model.train(texts_list)
    print('Marcov self length: ', len(markov_model.model))
    markov_model.save()


if __name__ == '__main__':
    fire.Fire(train)
