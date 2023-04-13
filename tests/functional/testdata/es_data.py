import uuid


def get_es_data():
    return [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'genres': [
            {'id': '565', 'name': 'Sci-Fi'},
            {'id': '678', 'name': 'Action'}
        ],
        'title': 'The Star',
        'description': 'New World',
        'directors': [
            {'id': '123', 'name': 'Bib'},
            {'id': '112', 'name': 'Boba'},
        ],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],

    } for _ in range(60)]
