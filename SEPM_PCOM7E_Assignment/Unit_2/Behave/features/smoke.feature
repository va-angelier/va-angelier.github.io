Feature: Smoke test
  Scenario Outline: Echo toont uppcase tekst
  Given I have the text "<input>"
  When I uppercase the text
  Then I see "<expected>"

  Examples:
    | input | expected |
    | hoi   | HI |
    | hej   | HEJ |
    | Hallo   | hoi |
    | hI   | HI |
    | bye   | BYE |
