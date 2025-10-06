import hashlib
import os

# jola_testenvironment\.venv\Lib\site-packages\allure_behave\utils.py

def scenario_history_id(scenario, extra: str = None) -> str:
    """
    Erzeugt eine History-ID für ein Scenario.
    - Immer basierend auf Feature-Name, Scenario-Name und evtl. Tabellenzeilen.
    - Zusätzlich kann ein optionaler Faktor (extra) angegeben werden,
      der in die Berechnung mit einfließt.
    """
    parts = [scenario.feature.name, scenario.name]

    # Falls Scenario aus einer Tabelle (Outline) stammt
    if hasattr(scenario, "_row") and scenario._row:
        row = scenario._row
        parts.extend([f"{name}={value}" for name, value in zip(row.headings, row.cells)])

    # Optionaler zusätzlicher Faktor (Parameter oder Umgebungsvariable)
    extra_factor = extra or os.getenv("TEST_HISTORY_FACTOR")
    if extra_factor:
        parts.append(f"extra={extra_factor}")

    # Hash erzeugen
    text = "|".join(parts).encode("utf-8")
    return hashlib.md5(text).hexdigest()