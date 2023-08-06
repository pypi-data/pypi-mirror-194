"""Example view."""

from typing import List

from ..views import TypeCategoryView


def raw_category_view() -> List[TypeCategoryView]:
    """Raw category view."""

    return [
        TypeCategoryView(
            pk=1,
            slug='box',
            parent_pk=None,
            lookup_category_pk=[1],
            lookup_category_slugs=['box'],
        ),
        TypeCategoryView(
            pk=56,
            slug='classical',
            parent_pk=[10],
            lookup_category_pk=[10, 56],
            lookup_category_slugs=['classical', 'music'],
        ),
    ]
