import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ProgramRow(Gtk.ListBoxRow):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box_outer)

        # Program name label
        self.label = Gtk.Label(label=name, xalign=0)
        self.box_outer.pack_start(self.label, True, True, 0)

        # Placeholder for program details, hidden by default
        self.details = Gtk.Label(label="Program details here...", xalign=0)
        self.details.set_no_show_all(True)
        self.box_outer.pack_start(self.details, True, True, 0)

    def show_details(self, show):
        if show:
            self.details.show()
        else:
            self.details.hide()

class LauncherWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Program Launcher")
        self.set_border_width(10)
        self.set_default_size(400, 400)

        # Vertical box to hold the search bar and the list box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Search bar
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search programs...")
        self.search_entry.connect("changed", self.on_search_changed)
        vbox.pack_start(self.search_entry, False, False, 0)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)
        vbox.pack_start(self.listbox, True, True, 0)

        self.listbox.connect("row-selected", self.on_row_selected)

        # Example programs
        self.program_names = ["Firefox", "Terminal", "Text Editor", "Settings"]
        for name in self.program_names:
            self.listbox.add(ProgramRow(name))

        self.listbox.show_all()

    def on_row_selected(self, listbox, row):
        for _row in listbox.get_children():
            if isinstance(_row, ProgramRow):
                _row.show_details(False)
        if row is not None:
            row.show_details(True)

    def on_search_changed(self, entry):
        search_text = entry.get_text().lower()
        for row in self.listbox.get_children():
            if search_text in row.name.lower():
                row.show()
            else:
                row.hide()

def main():
    win = LauncherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()