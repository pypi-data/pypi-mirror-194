# Changelog

## [Unreleased][]

[Unreleased]: https://github.com/chaostoolkit-incubator/chaostoolkit-spring/compare/0.3.2...HEAD

## [0.3.2][] - 2023-02-27

[0.3.2]: https://github.com/chaostoolkit-incubator/chaostoolkit-spring/compare/0.3.1...0.3.2

### Changed

- Updated build system
- Requires Python 3.7 as other packages


## [0.3.1][] - 2021-10-06

[0.3.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-spring/compare/0.3.0...0.3.1

### Fixed:

* `verify` parameter now passed as a `requests` parameter and not a query param

## [0.3.0][] - 2021-10-05

[0.3.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-spring/compare/0.2.0...0.3.0

### Changed:

* Switched to `black`, `flake8`, and `isort` for linting & formatting
* Ran `pyupgrade --py36-plus` across the codebase
* Switch to GitHub Actions instead of TravisCI
* Modified README to fall closer inline to more recently touched CTK packages

### Added:

* Makefile to abstract away common development tasks
* GitHub Actions workflows
* Added `verify_ssl` argument to probes and actions to allow for disabling SSL verification

## [0.2.0][] - 2018-11-20

[0.2.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-spring/compare/0.1.1...0.2.0

### Added

- fixed the bug on chaosmonkey_enabled probes when chaosmonkey not enabled.
- refactoring the code to remove duplicate requests calling

## [0.1.1][] - 2018-07-06

[0.1.1]: https://github.com/chaostoolkit-incubator/chaostoolkit-spring/compare/0.1.0...0.1.1

### Added

-   MANIFEST.in

## [0.1.0][] - 2018-07-06

[0.1.0]: https://github.com/chaostoolkit-incubator/chaostoolkit-spring/tree/0.1.0

### Added

-   Initial release
