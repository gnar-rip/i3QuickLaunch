# Custom Program Launcher for Arch Linux

This custom program launcher is designed for Arch Linux users who seek a lightweight, efficient, and highly customizable alternative to traditional application launchers. Integrated seamlessly with the i3 window manager, this launcher not only allows you to quickly find and launch your applications but also provides real-time insights into their resource usage, locations, and update status.

## Features

- **Program Launching**: Quickly search for and launch applications installed on your Arch Linux system.
- **Memory Usage Monitoring**: View real-time memory usage for running programs directly from the launcher interface.
- **Program Location**: Easily find out where applications are installed on your system.
- **Update Checks**: Check for available updates for your applications without leaving the launcher.
- **Search Functionality**: Use the built-in search bar to filter through your applications as you type.
- **Expandable Program Details**: Select programs to view detailed information, including memory usage, program location, and available updates.
- **i3 Window Manager Integration**: Designed to work flawlessly with the i3 window manager, providing a seamless user experience.

## Installation

To use this program launcher, ensure you have Python installed on your Arch Linux system. You will also need to install GTK+ for Python (PyGObject), `psutil`, and `i3ipc` libraries. 

1. **Install GTK+ for Python (PyGObject) and required libraries**:

    ```sh
    sudo pacman -S python-gobject gtk3
    pip install psutil i3ipc
    ```

2. **Clone the repository**:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

3. **Run the launcher**:

    ```sh
    python launcher.py
    ```

## Usage

- **Launching an Application**: Click on the application name in the list to launch it.
- **Viewing Program Details**: Select a program to view its details, including memory usage, installation path, and available updates.
- **Searching for Programs**: Type in the search bar at the top to filter the list of applications based on your input.

## Customization

This launcher is designed to be highly customizable. You can modify the source code to add new features, change the UI layout, and adjust the color themes to suit your preferences. The launcher uses GTK+, allowing for extensive customization through CSS.

## Contributing

Contributions to this project are welcome! Whether it's adding new features, fixing bugs, or improving documentation, your help is appreciated. Please feel free to fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
