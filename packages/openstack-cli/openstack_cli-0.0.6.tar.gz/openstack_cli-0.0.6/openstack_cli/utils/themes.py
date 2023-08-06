from inquirer.themes import Default
from blessed import Terminal

term = Terminal()


class BlueComposure(Default):
    def __init__(self):
        super().__init__()
        self.Question.brackets_color = term.dodgerblue
        self.Question.default_color = term.deepskyblue2
        self.Checkbox.selection_icon = "❯"
        self.Checkbox.selection_color = term.normal
        self.Checkbox.selected_icon = "◉"
        self.Checkbox.selected_color = term.cyan3
        self.Checkbox.unselected_icon = "◯"
        self.List.selection_color = term.normal
        self.List.selection_cursor = "❯"
