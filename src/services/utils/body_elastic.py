from typing import Optional


def get_body_search(
        size: int,
        sort_by: str,
        offset: int,
        sort_order: str,
        genre: Optional[str] = None,
        actor: Optional[str] = None,
        director: Optional[str] = None,
        writer: Optional[str] = None,
):
    """Функция формирует тело запроса к ElasticSearch."""

    if not any([genre, actor, director, writer]):
        return {
            "sort": [
                {
                    sort_by: {
                        "order": sort_order,
                    }
                }
            ],
            "from": offset,
            "size": size,
        }
    fields = []

    if genre is not None:
        fields.append(
            {
                'field': 'genres',
                'id': genre,
            }
        )

    if actor is not None:
        fields.append(
            {
                'field': 'actors',
                'id': actor,
            }
        )

    if writer is not None:
        fields.append(
            {
                'field': 'writers',
                'id': writer,
            }
        )

    if director is not None:
        fields.append(
            {
                'field': 'directors',
                'id': director,
            }
        )

    query = _get_query(fields)

    return {
        "query": query,
        "sort": [
            {
                sort_by: {
                    "order": sort_order,
                }
            }
        ],
        "from": offset,
        "size": size,
    }


def _get_query(
        fields: list
) -> dict:
    query = {
            "bool": {
                "must": [
                ]
            }
    }
    for item in fields:
        query['bool']['must'].append(
            _get_nested(
                item.get('field'),
                item.get('id'),
            )
        )

    return query


def _get_nested(
        path: str,
        field: str
) -> dict:
    return {
        "nested": {
            "path": path,
            "query": {
                "bool": {
                    "must": [
                        {"match": {f"{path}.id": field}}
                    ]
                }
            }
        }
    }
