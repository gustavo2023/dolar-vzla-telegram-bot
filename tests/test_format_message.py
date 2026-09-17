import main


def test_returns_error_message_when_no_data():
    assert main.format_message(None) == "Error: Could not retrieve exchange rates."
    assert main.format_message([]) == "Error: Could not retrieve exchange rates."


def test_full_payload_contains_both_rates(rates_payload):
    message = main.format_message(rates_payload)
    assert "Reporte del Dólar" in message
    assert "BCV (Oficial):* Bs. 36.5" in message
    assert "Paralelo:* Bs. 39.75" in message
    assert "16/09 09:00 AM" in message
    assert "Datos obtenidos de DolarAPI" in message


def test_payload_missing_paralelo_only_shows_bcv(rates_payload):
    message = main.format_message([rates_payload[0]])
    assert "BCV (Oficial)" in message
    assert "Paralelo" not in message


def test_payload_without_recognized_fuentes():
    message = main.format_message([{"fuente": "promedio", "promedio": 50.0}])
    assert "Reporte del Dólar" in message
    assert "BCV (Oficial)" not in message
    assert "Paralelo" not in message