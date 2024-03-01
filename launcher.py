#!/usr/bin/python
import gi
import json
import os
import subprocess
from configparser import RawConfigParser, NoSectionError
import psutil
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Gio

def get_theme_files(directory):
        path = os.path.join(os.path.dirname(__file__), directory)
        return [f for f in os.listdir(path) if f.endswith('.css')]

def get_usage_file_path():
    app_name = "i3QuickLaunch"
    default_data_home = os.path.join(os.path.expanduser("~"), ".local", "share")
    data_home = os.getenv("XDG_DATA_HOME", default_data_home)
    usage_file_path = os.path.join(data_home, app_name, "usage.json")
    os.makedirs(os.path.dirname(usage_file_path), exist_ok=True)
    return usage_file_path

def load_or_initialize_usage_data():
    usage_file_path = get_usage_file_path()
    if not os.path.exists(usage_file_path):
        return {}
    with open(usage_file_path, 'r') as file:
        return json.load(file)

usage_data = load_or_initialize_usage_data()

def load_usage_counts():
    usage_file_path = get_usage_file_path()
    if not os.path.exists(usage_file_path):
        return {}
    with open(usage_file_path, 'r') as file:
        return json.load(file)

def update_usage_count(program_name):
    usage_file_path = get_usage_file_path()
    usage_counts = load_usage_counts()
    usage_counts[program_name] = usage_counts.get(program_name, 0) + 1
    with open(usage_file_path, 'w') as file:
        json.dump(usage_counts, file, indent=4)
        
def check_for_updates(package_name):
    if not package_name:
        return False  # No update information available
    try:
        result = subprocess.check_output("checkupdates", shell=True, universal_newlines=True)
        updates = result.split('\n')
        for update in updates:
            if package_name in update:
                return True  # Update is available for this package
        return False  # No updates found for this package
    except subprocess.CalledProcessError as e:
        print(f"Error checking updates for {package_name}: {e}")
        return None  # Indicate an error occurreds

class ProgramRow(Gtk.ListBoxRow):
    def __init__(self, name, command, usage_count=0, install_path=None, package_name=None, icon=None):
        super().__init__()
        self.name = name
        self.command = command
        self.usage_count = usage_count
        self.install_path = install_path
        self.package_name = package_name
        self.has_memory_data = False 
        
        self.box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(self.box_outer)
        
        # Create a horizontal box to contain the icon and the label
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.box_outer.pack_start(hbox, True, True, 0)
        
        # Load and set the icon
        self.icon_image = Gtk.Image()
        self.set_icon(icon)
        hbox.pack_start(self.icon_image, False, False, 0)
        
        # Create and pack the label into the hbox
        self.label = Gtk.Label(label=name, xalign=0)
        hbox.pack_start(self.label, True, True, 0)
        #self.box_outer.pack_start(self.label, True, True, 0)
        
        # Initialize the memory usage progress bar
        self.memory_usage_bar = Gtk.ProgressBar()
        self.memory_usage_bar.set_visible(False)
        self.box_outer.pack_start(self.memory_usage_bar, expand=True, fill=True, padding=0)
        
        self.details = Gtk.Label(label=f"Details for {name}", xalign=0)
        self.details.set_visible(False)
        self.box_outer.pack_start(self.details, True, True, 0)
        
    def set_icon(self, icon_name):
        if icon_name:
            icon_theme = Gtk.IconTheme.get_default()
            try:
                pixbuf = icon_theme.load_icon(icon_name, 18, 0)
                scaled_pixbuf = pixbuf.scale_simple(18, 18, GdkPixbuf.InterpType.BILINEAR)
                self.icon_image.set_from_pixbuf(scaled_pixbuf)
            except Exception as e:
                print(f"Failed to load icon {icon_name}: {e}")
                # Handle missing icon (optional)
        
    def set_memory_usage(self, memory_usage):
        self.memory_usage_bar.set_fraction(memory_usage)
        #self.has_memory_data = True
        self.memory_usage_bar.set_visible(True)
    
    def show_details(self, show):
        if show:
            has_update = check_for_updates(self.package_name)
            if has_update is None:
                update_text = "No Data"  # no update/couldnt check for update
            else:
                update_text = "Update available" if has_update else "Up to date"
            update_text = "Update available" if has_update else "Up to date"
            self.details.set_text(f"Usage Count: {self.usage_count}\nInstall Path: {self.install_path}\n{update_text}")
        self.details.set_visible(show)
        self.memory_usage_bar.set_visible(show and self.has_memory_data)

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
        self.set_default_size(400, 400)
        self.usage_counts = load_usage_counts()
        # Vertical Box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(vbox)
        # Horizont Search + Theme Button
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        vbox.pack_start(hbox, False, False, 0)
        self.search_entry = Gtk.Entry()
        self.search_entry.set_placeholder_text("Search programs...")
        self.search_entry.connect("changed", self.on_search_changed)
        self.search_entry.set_size_request(375, -1)
        hbox.pack_start(self.search_entry, False, False, 0)
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled_window, True, True, 0)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.BROWSE)
        scrolled_window.add(self.listbox)
        self.connect("show", self.on_show_window)
        self.listbox.connect("row-selected", self.on_row_selected)
        self.populate_programs()
        
        # Theme dropdown - Broken. Fix asap
        self.theme_dropdown = Gtk.MenuButton.new()
        hbox.pack_start(self.theme_dropdown, False, False, 0)
        self.apply_theme('default.css')
        print("Connecting clicked signal...")
        self.theme_popover = Gtk.Popover()
        self.theme_dropdown.set_popover(self.theme_popover)
        theme_menu = self.populate_theme_selector()
        if theme_menu.get_parent():  # Check if the menu is already attached to another widget
            theme_menu.get_parent().remove(theme_menu)  # Remove it from its existing container
        self.theme_popover.add(theme_menu)  # Add the menu to the popover
        print("Theme Menu added to popover:", theme_menu)  
        self.theme_dropdown.connect("clicked", self.on_theme_changed)
 
        # Connect to the 'realize' signal to hide details after the window is fully initialized
        self.connect("realize", lambda _: self.hide_all_details())
        
        # Connect the list.box click so we can workaround the single click issue
        self.listbox.connect("button-press-event", self.on_listbox_click)
        
        # Allow "enter" to launch programs. Fixed double click override.
        self.listbox.connect("row-activated", self.on_row_activated)

    def populate_theme_selector(self):
        print("Populating theme selector...")
        theme_menu = Gtk.Menu()
        theme_files = get_theme_files('themes')
        print("Theme Files:", theme_files)
        for theme_file in theme_files:
            menu_label = os.path.splitext(os.path.basename(theme_file))[0]
            print("Menu Label:", menu_label)
            menu_item = Gtk.MenuItem.new_with_label(menu_label)
            menu_item.connect("activate", self.on_theme_selected, theme_file)  # Connect a signal
            theme_menu.append(menu_item)  # Add the menu item to the passed menu
        theme_menu.show_all()  # Show all menu items
        print("Theme Menu created:", theme_menu)
        return theme_menu
            
    def on_theme_changed(self, button):
        print('Theme button clicked')
        # Retrieve the popover associated with the button
        popover = button.get_popover()
        print("Popover:", popover)
        if popover is None:
            print("No popover associated with the button")
            return
        # Retrieve the menu model from the popover
        menu = self.theme_popover.get_child()
        
        # Find the active menu item and apply the corresponding theme
        for menu_item in menu.get_children():
            if menu_item.get_active():
                theme_name = menu_item.get_label()
                self.apply_theme(theme_name + '.css')
                print("Theme applied:", theme_name)
                return

        if menu is None:
            print("No menu found in the popover")
            return

    # Find the active menu item and apply the corresponding theme
        for menu_item in menu.get_children():
            if menu_item.get_active():
                theme_name = menu_item.get_label()
                self.apply_theme(theme_name + '.css')
                return

        print("No active menu item found")
           
    def on_theme_selected(self, menu_item, theme_file):
        print("Theme Selected:", theme_file)
        # Apply the selected theme directly
        self.apply_theme(theme_file)

        # Loop through all menu items to deactivate any previously active item
        for item in menu_item.get_parent().get_children():
            item.set_active(False)
        # Set the selected menu item as active
        menu_item.set_active(True)

 
    def populate_programs(self):
        desktop_files_dir = '/usr/share/applications'
        program_usage = load_usage_counts()  # Load the usage counts

        programs = []
        # Load all programs
        for item in os.listdir(desktop_files_dir):
            if item.endswith('.desktop'):
                config = RawConfigParser()
                config.read(os.path.join(desktop_files_dir, item))
            try:
                name = config.get('Desktop Entry', 'Name')
                exec_cmd = config.get('Desktop Entry', 'Exec').split()[0]
                exec_cmd = exec_cmd.partition('%')[0].strip()
                usage_count = program_usage.get(name, 0)  # Use 0 as default if not found
                install_path = os.path.join(desktop_files_dir, item)
                package_name = name.lower().replace(" ", "-")  # This is a placeholder and may not be accurate
                icon = config.get('Desktop Entry', 'Icon', fallback=None)  # Fetch icon for each program
                programs.append((name, exec_cmd, usage_count, install_path, package_name, icon))
            except NoSectionError:
                continue
        # Separate top 5 programs based on usage
        top_programs = sorted(programs, key=lambda x: (-x[2], x[0]))[:5]
        # Sort the rest alphabetically, excluding the top 5
        other_programs = sorted([p for p in programs if p not in top_programs], key=lambda x: x[0])
        # Clear the listbox before populating
        self.listbox.foreach(lambda widget: self.listbox.remove(widget))
        #Add top programs
        for program in top_programs:
            program_row = ProgramRow(*program)
            self.listbox.add(program_row)
        # Add a divider
        divider = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.listbox.add(divider)
        # Add the rest of the programs
        for program in other_programs:
            program_row = ProgramRow(*program)
            self.listbox.add(program_row)
        self.listbox.show_all()
        self.hide_all_details()

    def hide_all_details(self):
        for child in self.listbox.get_children():
            if isinstance(child, ProgramRow):
                child.show_details(False)

    def on_row_selected(self, listbox, row):
        self.hide_all_details()
        if row is not None:
            row.show_details(True)
            app_name = row.name
            memory_usage = self.get_memory_usage_for_application(app_name)
            row.set_memory_usage(memory_usage)

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
                        icon = config.get('Desktop Entry', 'Icon', fallback=None)
                        program_row = ProgramRow(name, exec_cmd, usage_count, icon=icon)
                        self.listbox.add(program_row)
                except NoSectionError:
                    continue

        self.listbox.show_all()
        # self.filter_programs(search_text)
        # Explicitly call hide_all_details to ensure all program details are hidden after repopulation
        self.hide_all_details()
        
    def on_listbox_click(self, widget, event):
        self.last_action_type = 'mouse'    
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

    def on_show_window(self, *args):
        #self.update_memory_usage_for_all_rows()
        pass
        
    def update_memory_usage_for_row(self, row):
        if isinstance(row, ProgramRow):
            memory_usage = self.get_memory_usage_for_application(row.name)
            row.set_memory_usage(memory_usage)
            
    def get_memory_usage_for_application(self, app_name):
        total_memory_usage = 0.0
        for proc in psutil.process_iter(attrs=['name', 'memory_percent']):
            try:
                # Simplify app_name and process name to improve matching accuracy
                proc_name = proc.info['name'].lower()
                simplified_app_name = app_name.lower().replace(" ", "")
                simplified_proc_name = proc_name.replace(" ", "")
        
                if simplified_app_name in simplified_proc_name:
                    # Debugging output to verify matching and memory usage
                    print(f"Matching process: {proc.info['name']} with memory usage: {proc.info['memory_percent']}%")
                    total_memory_usage += proc.info['memory_percent']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        memory_usage_fraction = total_memory_usage / 100.0  # Convert percentage to a fraction
        # Debugging output to verify total memory usage calculation
        print(f"Total memory usage for {app_name}: {memory_usage_fraction*100:.2f}%")
        return memory_usage_fraction
    
    def apply_theme(self, theme_file):
        css_theme_path = os.path.join(os.path.dirname(__file__), 'themes', theme_file)
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(css_theme_path)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)
     
    def update_memory_usage_for_all_rows(self):
        for row in self.listbox.get_children():
            if isinstance(row, ProgramRow):
                memory_usage = self.get_memory_usage_for_application(row.name)
                row.set_memory_usage(memory_usage)

def main():
    win = LauncherWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()