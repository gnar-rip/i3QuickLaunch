# CHANGELOG

All notable changes to this project will be documented in this file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2024-02-28

### Added
- Logic to retrieve and display memory usage for running applications, enhancing the launcher's functionality with real-time system resource monitoring.
- A progress bar UI component for each application in the launcher to visually represent its memory usage.
- Theme support enabling users to customize the appearance of the launcher interface.

### Changed
- Improved the accuracy of matching running processes to applications listed in the launcher for more reliable memory usage tracking.
- Updated UI behavior to dynamically display memory usage details only when an application is highlighted, maintaining a clean interface.
- Refined the program listing process to only show "favorite" programs initially, with the capability to dynamically update the list based on search input.
- Enhanced the user interface and interaction feedback, such as highlighting and detail visibility, to be more responsive and intuitive.
- Adjusted `usage.json` storage logic to comply with XDG standards, ensuring user data is stored in a standardized and expected location across different Linux environments.

### Fixed
- Resolved issues where program details were incorrectly shown or hidden due to event handling conflicts.
- Addressed a bug where the launcher would not correctly differentiate between keyboard and mouse actions, leading to unintended program launches.
- Fixed an error related to variable scope in the `on_search_changed` method, ensuring the launcher dynamically updates the program list without crashing.
- Corrected the handling of `usage.json` to dynamically determine its path, addressing potential issues with file access across various user environments.

### Known Issues
- Lack of differentiation between input methods for program activation.
- Memory Usage bar not being displayed, nor showing correct memory usage information.
- Checkforupdates still broken. Default displays "Up to date" but this may not be accurate.

## [0.1.0] - 2024-02-24

### Added
- Initial release of the launcher with basic functionality to list installed applications and launch them via a graphical interface.
- Simple search functionality to filter the list of applications in real-time.


