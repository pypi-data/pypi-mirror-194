from collections import namedtuple

from django.db.models.sql import query
from django.db.models.sql import subqueries

from clickhouse_backend import compat

ExplainInfo = namedtuple("ExplainInfo", ("format", "type", "options"))


class Query(query.Query):
    def __init__(self, model, where=query.WhereNode, alias_cols=True):
        if compat.dj_ge4:
            super().__init__(model, alias_cols)
        else:
            super().__init__(model, where, alias_cols)
        self.setting_info = {}

    def clone(self):
        obj = super().clone()
        obj.setting_info = self.setting_info.copy()
        return obj

    def explain(self, using, format=None, type=None, **settings):
        q = self.clone()
        q.explain_info = ExplainInfo(format, type, settings)
        compiler = q.get_compiler(using=using)
        return "\n".join(compiler.explain_query())


def clone_decorator(cls):
    old_clone = cls.clone

    def clone(self):
        obj = old_clone(self)
        if hasattr(obj, "setting_info"):
            obj.setting_info = self.setting_info.copy()
        return obj

    cls.clone = clone
    return cls


clone_decorator(subqueries.UpdateQuery)
clone_decorator(subqueries.DeleteQuery)
