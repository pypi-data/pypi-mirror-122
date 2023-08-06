from unittest import mock

import django

from django.core.paginator import Paginator
from django.contrib.admin.views.main import ChangeList

DJANGO_2X = django.VERSION[0] == 2
DJANGO_3X = django.VERSION[0] == 3


def get_elided_page_range(self, number=1, *, on_each_side=3, on_ends=2):

    if self.num_pages <= (on_each_side + on_ends) * 2:
        yield from range(1, self.num_pages + 1)
        return

    if number > (1 + on_each_side + on_ends) + 1:
        yield from range(1, on_ends + 1)
        yield Paginator.ELLIPSIS
        yield from range(number - on_each_side, number + 1)
    else:
        yield from range(1, number + 1)

    if number < (self.num_pages - on_each_side - on_ends) - 1:
        yield from range(number + 1, number + on_each_side + 1)
        yield Paginator.ELLIPSIS
        yield from range(self.num_pages - on_ends + 1, self.num_pages + 1)
    else:
        yield from range(number + 1, self.num_pages + 1)


class DfesChangeList(ChangeList):
    """
    Extended Django ChangeList to be able show data from external sources.
    """

    def get_queryset(self, request):
        if DJANGO_3X:
            (self.filter_specs, self.has_filters, _, _, _) = self.get_filters(request)
        else:
            (self.filter_specs, self.has_filters, _, _) = self.get_filters(request)
        return self.root_queryset

    def get_results(self, request):
        # qs = self.queryset
        # if self.show_all:
        #     qs = self.queryset
        # else:
        #     qs = self.get_queryset_slice()

        offset = (self.page_num - 1) * self.list_per_page
        limit = self.list_per_page

        result = self.model_admin.get_list(request, offset, limit)
        total = result.get("total") or 0

        # result = qs.execute_query(request, offset, limit)

        paginator = mock.MagicMock()
        paginator.count = total
        paginator.num_pages = int(total / self.list_per_page)
        paginator.get_elided_page_range = lambda *args, **kwargs: get_elided_page_range(paginator, *args, **kwargs)

        # self.result_count = paginator.count
        self.result_count = paginator.count
        self.show_full_result_count = False
        self.show_admin_actions = True
        self.full_result_count = paginator.count
        self.result_list = result.get("items") or []
        self.can_show_all = False
        self.multi_page = True
        self.paginator = paginator


class DfesAdminModelMixin(object):
    def get_changelist(self, request, **kwargs):
        return DfesChangeList

    def get_list(self, request, offset, limit):
        raise NotImplementedError("{}.get_list must be implemented".format(self.__class__.__name__))
