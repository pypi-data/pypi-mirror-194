# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
Unreleased template stuff

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed
### Security
-->

## [Unreleased]
### Added
### Changed
### Deprecated
### Removed
### Fixed

## [0.4.1]

### Fixed

 - Fixed the import in the Xilinx ArtyS7 and Atlys board files where they were using the improper import in `toolchain_program` for `required_tool`.
## [0.4.0]

### Added

- Added [Code of Conduct](https://github.com/shrine-maiden-heavy-industries/torii-boards/blob/main/CODE_OF_CONDUCT.md)
- Added [flake8](https://flake8.pycqa.org/en/latest/) configuration file.
- Added [mypy](http://mypy-lang.org/) configuration file.
- Added a `noxfile.py` for use with [nox](https://nox.thea.codes/en/stable/).
- Added `MEGA65` board definitions file [#1](https://github.com/shrine-maiden-heavy-industries/torii-boards/pull/1)

### Changed

- Renamed from `amaranth_boards` to `torii_boards`
- Updated the CI scripts.
- Moved Intel based platforms into `torii_boards.intel`.
- Moved Xilinx based platforms into `torii_boards.xilinx`.
- Moved Lattice based platforms into `torii_boards.lattice`.
- Moved Quicklogic based platforms into `torii_boards.quicklogic`.
- Moved the `torii_boards.extensions` into `torii_boards.resources.extensions`.

### Removed

- Removed the `nMigen` compatibility layer.
- Removed the `torii_boards.resources` and migrated that to [`torii.platform.resources`](https://github.com/shrine-maiden-heavy-industries/torii-hdl/tree/main/torii/platform/resources)

### Fixed

- Fixed the package name.
- Fixed the package authors.
- Fixed the package trove classifiers.
- Fixed all flake8 warnings on the entire codebase.
- Fixed indentation.

## [0.1.0] - [0.3.0]

No changelog is provided for these versions as they are all older untagged releases of [Amaranth Boards](https://github.com/amaranth-lang/amaranth-boards) from before the fork.


[unreleased]: https://github.com/shrine-maiden-heavy-industries/torii-hdl/compare/v0.4.1...main
[0.4.1]: https://github.com/shrine-maiden-heavy-industries/torii-hdl/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/shrine-maiden-heavy-industries/torii-hdl/compare/amaranth-fork...v0.4.0
[0.3.0]: https://github.com/shrine-maiden-heavy-industries/torii-hdl/compare/amaranth-fork...main
[0.1.0]: https://github.com/shrine-maiden-heavy-industries/torii-hdl/compare/amaranth-fork...main
