from django.db import models
from django.utils.encoding import smart_unicode
from django.utils import formats
from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.util import lookup_field
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape
from django.db.models.fields.related import ManyToManyRel

from django.contrib.admin import util as admin_util

def djmoney_contents(self):
    from django.contrib.admin.templatetags.admin_list import _boolean_icon
    from django.contrib.admin.views.main import EMPTY_CHANGELIST_VALUE
    field, obj, model_admin = self.field['field'], self.form.instance, self.model_admin

    try:
        f, attr, value = lookup_field(field, obj, model_admin)
    except (AttributeError, ValueError, ObjectDoesNotExist):
        result_repr = EMPTY_CHANGELIST_VALUE
    else:
        if f is None:
            boolean = getattr(attr, "boolean", False)
            if boolean:
                result_repr = _boolean_icon(value)
            else:
                result_repr = smart_unicode(value)
                if getattr(attr, "allow_tags", False):
                    result_repr = mark_safe(result_repr)
        else:
            if value is None:
                result_repr = EMPTY_CHANGELIST_VALUE
            elif isinstance(f.rel, ManyToManyRel):
                result_repr = ", ".join(map(unicode, value.all()))
            else:
                result_repr = smart_unicode(value)
    return conditional_escape(result_repr)

from django.contrib.admin.helpers import AdminReadonlyField
AdminReadonlyField.contents = djmoney_contents
