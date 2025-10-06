# Humanoid Robot – System Design

Welkom! Dit is de documentatie voor mijn OOP_PCOM7E-assignment.

- **Project README** → [README](README.md)
- **Summative Report (500w rationale incl.)** → [REPORT](REPORT.md)
- **Design Rationale (uitgebreid)** → [DESIGN_RATIONALE](DESIGN_RATIONALE.md)
- **Changelog** → [CHANGELOG](CHANGELOG.md)

## UML Artefacts
- Class → ![Class Diagram](assets/img/class_diagram.png)
- Sequence → ![Sequence Diagram](assets/img/sequence_diagram.png)
- Activity (navigate/pick/errors) → ![Nav](assets/img/activity_navigate.png), ![Pick](assets/img/activity_pick.png), ![Errors](assets/img/activity_errors.png)
- State → ![State](assets/img/state_diagram.png)
- Component → ![Component](assets/img/component_diagram.png)
- Deployment → ![Deployment](assets/img/deployment_diagram.png)
- State Pattern → ![State](assets/img/state-pattern.png)

## Run & Validate
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
flake8
pytest -q --cov=robot --cov-report=term-missing
python -m robot
