# Custom Program Launcher for Arch Linux & i3WM

This custom program launcher, tailored for Arch Linux users and seamlessly integrated with the i3 window manager, offers a lightweight, efficient, and customizable solution for managing and launching applications. With enhanced features focusing on usability and system insights, this launcher elevates your desktop experience by providing detailed information about your applications at a glance.

## Features

- **Program Launching**: Instantly search for and launch applications installed on your Arch Linux system with support for double-click or Enter key activations.
- **Memory Usage Monitoring**: Access real-time memory usage data for running programs directly within the launcher interface.
- **Program Location & Update Checks**: Identify where applications are installed on your system and check for available updates effortlessly.
- **Search Functionality**: Utilize the dynamic search bar to swiftly filter through your applications as you type.
- **Expandable Program Details**: Click on a program to unveil additional details, such as memory usage, installation path, and update availability.
- **Favorites Priority**: Frequently used applications are prioritized and listed at the top, making them easily accessible for a faster workflow.
- **i3 Window Manager Integration**: Crafted to integrate flawlessly with the i3 window manager, ensuring a seamless user experience.

## Installation

To install this program launcher, ensure Python and GTK+ for Python (PyGObject) are installed on your system. You will also need the `psutil` and `i3ipc` libraries for full functionality. 

1. **Install Required Packages**:

   ```
   sudo pacman -S python-gobject gtk3
   pip install psutil i3ipc
   ```

2. **Clone the Repository** (replace `<repository-url>` with the actual URL of the repository):

   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

3. **Install the Launcher**:

   Using the `setup.py` file, you can easily install the launcher with:

   ```
   python setup.py install
   ```

   Alternatively, for a development setup or to run directly without installing:

   ```
   python launcher.py
   ```

## Usage

- **Launching an Application**: Double-click on an application name or select it and press Enter to launch.
- **Viewing Program Details**: Highlight a program to view its detailed information, including memory usage, installation path, and update status.
- **Searching for Programs**: Begin typing in the search bar at the top to filter applications based on your input. Only favorites are shown by default, with others appearing as they match the search criteria.

## Customization

The launcher is designed for high customizability. Feel free to modify the source code to add new features, alter the UI layout, or customize the color themes to match your aesthetic preferences. Leveraging GTK+, the launcher supports extensive customization possibilities through CSS.

## Contributing

Contributions are warmly welcomed! If you're interested in adding new features, fixing bugs, or enhancing the documentation, please fork the repository, make your changes, and submit a pull request.

## License

This project is distributed under the MIT License - see the LICENSE file for details.


