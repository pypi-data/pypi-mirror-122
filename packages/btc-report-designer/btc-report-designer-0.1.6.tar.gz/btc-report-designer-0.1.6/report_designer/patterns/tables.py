from report_designer.core.tables import (
    AbstractTable,
    CellTypeCenter,
    CellTypeDateTime,
)


class PatternTable(AbstractTable):
    """
    Таблица списка шаблонов
    """

    def create_header(self, header):
        level_0 = [
            header('Наименование'),
            header('Основная таблица'),
            header('Группы'),
            header('Автор'),
            header('Дата и время обновления'),
        ]
        return [level_0]

    def create_cells(self, obj):
        cell = self.cell_class
        url = obj.get_detail_url()
        return [
            cell(obj.name, cell_type=CellTypeCenter, url=url),
            cell(obj.root, cell_type=CellTypeCenter, url=url),
            cell(obj.get_groups_names, cell_type=CellTypeCenter, url=url),
            cell(obj.author, cell_type=CellTypeCenter, url=url),
            cell(obj.updated, cell_type=CellTypeDateTime, url=url),
        ]
