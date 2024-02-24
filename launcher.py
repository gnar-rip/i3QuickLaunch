import gi
import os
import subprocess
from configparser import RawConfigParser, NoSectionError
import json

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

def get_usage_file_path():
    app_name = "i3QuickLaunch"  # Example application name
    default_data_home = os.path.join(os.path.expanduser("~"), ".local", "share")
    data_home = os.getenv("XDG_DATA_HOME", default_data_home)

    usage_file_path = os.path.join(data_home, app_name, "usage.json")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(usage_file_path), exist_ok=True)
    
    return usage_file_path

def load_or_initialize_usage_data():
    usage_file_path = get_usage_file_path()
    
    if not os.path.exists(usage_file_path):
        return {}  # Initialize to an empty dict if the file doesn't exist

    with open(usage_file_path, 'r') as file:
        return json.load(file)

# Example usage within your launcher application
usage_data = load_or_initialize_usage_data()

def load_usage_counts():
    usage_file_path = get_usage_file_path()  # Call the function to get the path
    if not os.path.exists(usage_file_path):
        return {}  # Initialize to an empty dict if the file doesn't exist
    
    with open(usage_file_path, 'r') as file:
        return json.load(file)

def update_usage_count(program_name):
    usage_file_path = get_usage_file_path()  # Dynamically get the file path
    usage_counts = load_usage_counts()  # Load the current usage counts
    
    # Update the usage count for the specified program
    usage_counts[program_name] = usage_counts.get(program_name, 0) + 1
    
    # Write the updated usage counts back to the file
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
        # Initialize the flag to track the last action type ('keyboard' or 'mouse')
        self.last_action_type = None
        self.connect("key-press-event", self.on_key_press)
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
        
        # Connect the list.box click so we can workaround the single click issue
        self.listbox.connect("button-press-event", self.on_listbox_click)
        
        # Allow "enter" to launch programs. This may override double click functionality - DO NOT LOSE THIS LINE OF CODE AND FIX IMEDIATELY IF BROKEN YOU FUCKIN DUMBASS
        self.listbox.connect("row-activated", self.on_row_activated)


    def populate_programs(self):
        desktop_files_dir = '/usr/share/applications'
        program_usage = load_usage_counts()  # Load the usage counts

        programs = []

        for item in os.listdir(desktop_files_dir):
            if item.endswith('.desktop'):
                config = RawConfigParser()
                config.read(os.path.join(desktop_files_dir, item))
            try:
                name = config.get('Desktop Entry', 'Name')
                exec_cmd = config.get('Desktop Entry', 'Exec').split()[0]
                exec_cmd = exec_cmd.partition('%')[0].strip()
                usage_count = program_usage.get(name, 0)  # Use 0 as default if not found
                # Append all programs but later add conditionally to the listbox based on usage_count
                programs.append((name, exec_cmd, usage_count))
            except NoSectionError:
                continue

    # Sort programs by usage count in descending order, then by name
        programs.sort(key=lambda x: (-x[2], x[0]))

    # Populate the listbox with sorted programs, adding only if usage_count > 0
        for name, exec_cmd, usage_count in programs:
            if usage_count > 0:  # Add condition here
                program_row = ProgramRow(name, exec_cmd, usage_count)
                self.listbox.add(program_row)
    
        self.listbox.show_all()

    def hide_all_details(self):
        for row in self.listbox.get_children():
            row.show_details(False)

    def on_row_selected(self, listbox, row):
        self.hide_all_details()
        if row is not None:
            row.show_details(True)

    def on_search_changed(self, entry):
        search_text = entry.get_text().lower()
    # Clear the listbox before repopulating based on search
        self.listbox.foreach(lambda widget: self.listbox.remove(widget))

        desktop_files_dir = '/usr/share/applications'  # Ensure this is defined outside the loop
        program_usage = load_usage_counts()

        if search_text == "":
        # If the search field is cleared, repopulate with favorites
            self.populate_programs()
        else:
        # Dynamically add both favorites and matching non-favorites
            for item in os.listdir(desktop_files_dir):
                if item.endswith('.desktop'):
                    config = RawConfigParser()
                    config.read(os.path.join(desktop_files_dir, item))
                try:
                    name = config.get('Desktop Entry', 'Name').strip()
                    if search_text in name.lower():
                        exec_cmd = config.get('Desktop Entry', 'Exec').split()[0]
                        exec_cmd = exec_cmd.partition('%')[0].strip()
                        usage_count = program_usage.get(name, 0)
                        program_row = ProgramRow(name, exec_cmd, usage_count)
                        self.listbox.add(program_row)
                except NoSectionError:
                    continue

        self.listbox.show_all()
        # Explicitly call hide_all_details to ensure all program details are hidden after repopulation
        self.hide_all_details()
        
    def on_listbox_click(self, widget, event):
        self.last_action_type = 'mouse'
    # GDK_2BUTTON_PRESS is the constant for a double-click event.
        if event.type == Gdk.EventType.DOUBLE_BUTTON_PRESS:
            row = self.listbox.get_selected_row()
            if row:
                row.launch_program()
                
    def on_row_activated(self, listbox, row):
        if self.last_action_type == 'keyboard':
            if row is not None:
                row.launch_program()
        # Reset the flag after handling the activation
        self.last_action_type = None
                
    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Return:  # Check if the "Enter" key was pressed
            self.last_action_type = 'keyboard'


def main():
    win = LauncherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
