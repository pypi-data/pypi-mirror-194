from typing import Callable, Any, Optional, Set, Dict

from django import forms
from django.utils.safestring import mark_safe

import nh3


class Nh3Field(forms.CharField):
    """ nh3 form field """
    empty_values = [None, "", [], (), {}]

    def __init__(self, attributes: Dict[str, Set[str]] = dict(),
                 attribute_filter: Optional[Callable[[str, str, str], Optional[str]]] = None,
                 clean_content_tags: Set[str] = set(), link_rel: str = '',
                 strip_comments: bool = False, tags: Set[str] = set(), *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.nh3_options = {
            'attributes': attributes,
            'attribute_filter': attribute_filter,
            'clean_content_tags': clean_content_tags,
            'link_rel': link_rel,
            'strip_comments': strip_comments,
            'tags': tags
        }

    def to_python(self, value) -> Any:
        """
        Strips any dodgy HTML tags from the input if the input value contains HTML

        Mark the return value as template safe.
        """
        if value in self.empty_values:
            return self.empty_value
        if nh3.is_html(value):
            return mark_safe(nh3.clean(value, **self.nh3_options))
        else:
            return value
