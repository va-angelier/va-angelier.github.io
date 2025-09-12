# Changelog
All notable changes to this project will be documented in this file.

The format is based on **Keep a Changelog** and this project adheres to **Semantic Versioning** (SemVer).

## [Unreleased]
### Added
- More tests, better logic and separations
### Changed
- Turned the project into a module
### Fixed
- Pickup objects, get hight test results (91%)
### Tests
- Test batterylevels and charging added
### Docs
- Documents are in /docs, UML are in /uml and 'graphics' are in assets/img

---

## [1.0.0] - 2025-09-12
### Added
- **Auto-docking & CHARGING state**: when battery drops below threshold *after* an action, the robot plans a route to the charger and enters a dedicated `CHARGING` state; charging progresses via `tick` until 100%.
- **Case-insensitive object lookup** for `pick <kind>` to reduce CLI user error.
- **.coveragerc** and **pytest.ini** for consistent coverage and discovery.

### Changed
- **CLI entrypoint moved** to `robot/__main__.py`; run via `python -m robot`. Core logic remains in `robot/robot_system.py`.
- **Environment.sense()** no longer moves objects onto obstacles (stable tests); still updates sensor readings and index.
- **Manipulator.pick()** made deterministic by default; tests that require failure use a stub.

### Fixed
- Import path stability in tests (package import `from robot.robot_system import ...`).
- Test flakiness caused by random grasp failures and object jitter causing unreachable targets.

### Tests
- Expanded suite to cover auto-docking → `CHARGING` → charge-to-100%, busy guards, no-path/timeout, invalid coords, and object-not-found.
- Coverage at **91%** on macOS/Python 3.12.7.

### Docs
- Updated **README.md** (run instructions, architecture overview, UML artefacts).
- Updated **REPORT.md** (assessment mapping, rationale, validation results).
- Added this **CHANGELOG.md**.

---

## [0.2.0] - 2025-09-11
### Added
- Full UML set: Class, Sequence, Activity (navigate/pick/errors), State, Component, Deployment, Use Case.
- Initial unit tests and coverage reporting.

### Changed
- README structure and repository housekeeping.

---

## [0.1.0] - 2025-08-23
### Added
- Initial repository scaffolding and baseline UML (“washing-machine” exploration).
- Core Python OOP skeleton (`Robot`, `Navigation`, `Manipulator`, `Communicator`, `Environment`, `MemoryStore`, `CLI`).

---

## Versioning
We use **Semantic Versioning**:
- **MAJOR**: incompatible API changes,
- **MINOR**: backwards-compatible functionality,
- **PATCH**: backwards-compatible bug fixes.

## Commit conventions
Recommended **Conventional Commits**:
- `feat(robot): add charging state with auto-docking`
- `fix(nav): prevent obstacles from blocking final target`
- `test(cli): add coverage for docking flow`
- `docs(readme): clarify run instructions`

© Victor Angelier – OOP_PCOM7E Assignment