"""Source category."""

from __future__ import annotations

from typing import Dict, List, Union
from service.ext.testing import faker

from ..common_types import (
    BreadCrumbs,
    VisibleType,
    SizedSourceMarketImage,
    builtins,
)


class SourceCategory(builtins.TypeSource):
    """Source category."""

    id: int
    name: str
    parent: Union[int, None]

    is_actual: bool
    visible_type: VisibleType

    slug: str
    old_slug: Union[str, None]

    breadcrumbs: Union[List[BreadCrumbs], str, None]

    cover: SizedSourceMarketImage
    preview: SizedSourceMarketImage

    updated: str
    created: str

    __i18n__ = ['name']

    @classmethod
    def example(
        cls,
        pk: int,
        name: str,
        slug: str,
        is_actual: bool = True,
        parent_pk: int = None,
        visible_type: VisibleType = VisibleType.simple,
    ) -> SourceCategory:
        """From values."""

        return SourceCategory(
            id=pk,
            name=name,
            slug=slug,
            parent=parent_pk,
            old_slug=f'{slug}_old',
            is_actual=is_actual,
            visible_type=visible_type,
            breadcrumbs=[{'title': name, 'slug': slug}],
            cover=SizedSourceMarketImage.example(),
            preview=SizedSourceMarketImage.example(),
            updated=str(faker.any_dt_day_ago()),
            created=str(faker.any_dt_day_ago()),
        )

    def clean(self) -> Dict:
        """Overrides."""

        _context = {
            'name': self.name,
            'slug': self.slug,
            'parent_pk': self.parent,
            'old_slug': self.old_slug,
            'is_actual': self.is_actual,
            'visible_type': self.visible_type,
            'breadcrumbs': self.breadcrumbs,
        }

        _cover = self.cover.to_sized_image().dict()
        _preview = self.preview.to_sized_image().dict()

        _context['media'] = {'cover': _cover, 'preview': _preview}

        return _context
