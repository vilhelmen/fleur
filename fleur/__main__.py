#!/usr/bin/env python3

from . import symbols

import logging, logging.handlers

rootLogger = logging.getLogger('')
rootLogger.setLevel(logging.DEBUG)
socketHandler = logging.handlers.SocketHandler('localhost',
                    logging.handlers.DEFAULT_TCP_LOGGING_PORT)
# don't bother with a formatter, since a socket handler sends the event as
# an unformatted pickle
rootLogger.addHandler(socketHandler)

logger = rootLogger


import npyscreen


class myEmployeeForm(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.myName = self.add(npyscreen.TitleText, name='Name')
        self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department',
                                     values=['Department 1', 'Department 2', 'Department 3'])
        self.myDate = self.add(npyscreen.TitleDateCombo, name='Date Employed')



class GridObject:
    _template = symbols.flower_stages

    show_bold = False  # set by grid because... editing cell???
    highlight = False  # set by grid on display to show highlight status
    grid_current_value_index = (0, 0)  # set by grid to indicate grid position(??) (row, col)

    def __str__(self):
        return self._template[2]






class FlowerGrid(npyscreen.SimpleGrid):
    _contained_widgets = npyscreen.Pager
    def make_contained_widgets(self):
        super(FlowerGrid, self).make_contained_widgets()
        for x in self._my_widgets:
            for y in x:
                y.autowrap = True

    def custom_print_cell(self, actual_cell, cell_display_value):
        logger.debug('Displaying cell')
        actual_cell.values = [str(cell_display_value)]


class PlayArea(npyscreen.Form):
    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        self.grid = self.add(FlowerGrid, columns=4, column_width=10, row_height=5, always_show_cursor=True)
        self.grid.set_grid_values_from_flat_list([GridObject()]*20, max_cols=4)
        #self.myDepartment = self.add(npyscreen.TitleSelectOne, scroll_exit=True, max_height=3, name='Department',
        #                             values=['Department 1', 'Department 2', 'Department 3'])
        #self.myDate = self.add(npyscreen.TitleDateCombo, name='Date Employed')


class MyApplication(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', PlayArea, name='PLAYAREA')
        # A real application might define more forms here.......


if __name__ == '__main__':
    TestApp = MyApplication().run()