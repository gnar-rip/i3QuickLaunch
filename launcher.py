import gi
import os
import subprocess
from configparser import RawConfigParser, NoSectionError
import json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

usage_file_path = "usage.json"

def load_usage_counts():
    try:
        with open(usage_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def update_usage_count(program_name):
    usage_counts = load_usage_counts()
    usage_counts[program_name] = usage_counts.get(program_name, 0) + 1
    with open(usage_file_path, 'w') as file:
        json.dump(usage_counts, file, indent=4)

class ProgramRow(Gtk.ListBoxRow):
    def __init__(self, name, command, usage_count=0):
        super().__init__()
        self.name = name
        self.command = command
        self.usage_count = usage_count
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(self.box_outer)
        self.label = Gtk.Label(label=name, xalign=0)
        self.box_outer.pack_start(self.label, True, True, 0)
        self.details = Gtk.Label(label=f"Details for {name}", xalign=0)
        self.details.set_visible(False)
        self.box_outer.pack_start(self.details, True, True, 0)

    def show_details(self, show):
        self.details.set_visible(show)

    def launch_program(self):
        update_usage_count(self.name)
        subprocess.Popen(self.command.split(), start_new_session=True)

class LauncherWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Program Launcher")
        self.set_border_width(10)
        self.set_default_size(400, 600)
        self.usage_counts = load_usage_counts()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search programs...")
        self.search_entry.connect("changed", self.on_search_changed)
        vbox.pack_start(self.search_entry, False, False, 0)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled_window, True, True, 0)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)
        scrolled_window.add(self.listbox)
        self.listbox.connect("row-selected", self.on_row_selected)
        self.populate_programs()

        # Connect to the 'realize' signal to hide details after the window is fully initialized
        self.connect("realize", lambda _: self.hide_all_details())

    def populate_programs(self):
        desktop_files_dir = '/usr/share/applications'
        for item in os.listdir(desktop_files_dir):
            if item.endswith('.desktop'):
                config = RawConfigParser()
                config.read(os.path.join(desktop_files_dir, item))
                try:
                    name = config.get('Desktop Entry', 'Name')
                    exec_cmd = config.get('Desktop Entry', 'Exec').split()[0]
                    exec_cmd = exec_cmd.partition('%')[0].strip()
                    usage_count = self.usage_counts.get(name, 0)
                    program_row = ProgramRow(name, exec_cmd, usage_count)
                    self.listbox.add(program_row)
                except NoSectionError:
                    continue

    def hide_all_details(self):
        for row in self.listbox.get_children():
            row.show_details(False)

    def on_row_selected(self, listbox, row):
        self.hide_all_details()
        if row is not None:
            row.show_details(True)

    def on_search_changed(self, entry):
        search_text = entry.get_text().lower()
        for row in self.listbox.get_children():
            row.set_visible(search_text in row.name.lower())

def main():
    win = LauncherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
