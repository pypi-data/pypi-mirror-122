from django.urls import reverse_lazy

from report_designer.core.actions import ActionGroup, SimpleModalAction, DropdownActionGroup, UpdateDropdownModalAction


class PatternListActionGroup(ActionGroup):
    """
    Группа действий в списке шаблонов
    """

    create = SimpleModalAction(title='Добавить', url=reverse_lazy('report_designer:patterns:create'))


class PatternDropdownActionGroup(DropdownActionGroup):
    """
    Выпадающий список для претензионного дела
    """

    edit = UpdateDropdownModalAction(title='Редактировать основную информацию')
