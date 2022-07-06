from django_filters import Filter


class ListFilter(Filter):
    def filter(self, qs, value):
        if value not in (None, ""):
            integers = [int(v) for v in value.split(",")]
            return qs.filter(
                **{"%s__%s" % (self.field_name, self.lookup_expr): integers}
            )
        return qs
