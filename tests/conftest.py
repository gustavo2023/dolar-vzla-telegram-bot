import pytest


@pytest.fixture
def rates_payload():
    """Realistic DolarAPI /v1/dolares response entries."""
    return [
        {
            "fuente": "oficial",
            "promedio": 36.5,
            "fechaActualizacion": "2026-09-16T09:00:00.000Z",
        },
        {
            "fuente": "paralelo",
            "promedio": 39.75,
            "fechaActualizacion": "2026-09-16T08:55:00.000Z",
        },
    ]