from sqlalchemy.orm import Query

def paginate_query(query: Query, page: int, per_page: int):
    """
    Paginate a given SQLAlchemy query.

    Parameters:
    - query: The SQLAlchemy query object to paginate.
    - page: Current page number.
    - per_page: Number of items per page.

    Returns:
    - A tuple containing the paginated results and pagination details.
    """
    total_items = query.count()
    total_pages = (total_items // per_page) + (1 if total_items % per_page else 0)
    items = query.limit(per_page).offset((page - 1) * per_page).all()

    pagination_details = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'total_items': total_items
    }

    return items, pagination_details
