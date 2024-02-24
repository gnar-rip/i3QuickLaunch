# CHANGELOG

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial creation of the launcher script with basic functionality to list and launch applications.
- Dynamic search functionality to filter through the listed applications based on user input.
- Implementation of `ProgramRow` class to encapsulate each program's display and actions within the launcher.
- Feature to prioritize frequently used programs based on usage counts, enhancing the user experience by listing favorite programs at the top.
- Functionality to hide and show details of each program dynamically, improving information management and UI cleanliness.
- Double-click and "Enter" key activation for launching programs, offering users multiple intuitive ways to interact with the launcher.
- Keyboard and mouse event differentiation, allowing for precise user interaction handling and preventing conflicts between input methods.

### Changed
- Refined the program listing process to only show "favorite" programs initially, with the capability to dynamically update the list based on search input.
- Enhanced the user interface and interaction feedback, such as highlighting and detail visibility, to be more responsive and intuitive.

### Fixed
- Resolved issues where program details were incorrectly shown or hidden due to event handling conflicts.
- Addressed a bug where the launcher would not correctly differentiate between keyboard and mouse actions, leading to unintended program launches.
- Fixed an error related to variable scope in the `on_search_changed` method, ensuring the launcher dynamically updates the program list without crashing.

## [0.1.0] - 2024-02-24

### Added
- Initial release of the launcher with basic functionality to list installed applications and launch them via a graphical interface.
- Simple search functionality to filter the list of applications in real-time.

### Known Issues
- Program details are not dynamically managed based on user interaction.
- Lack of differentiation between input methods for program activation.
