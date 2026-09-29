import pytest
from hypothesis import given, strategies as st

from domain.index.distance import calculate

@pytest.mark.parametrize(
    "nome_rota, lat1, lon1, lat2, lon2, distancia_esperada_m",
    [
        # Caso 1: Cidades próximas (São Paulo -> Rio de Janeiro) ~ 357 km
        ("SP_to_RJ", -23.5505, -46.6333, -22.9068, -43.1729, 357690.0),

        # Caso 2: Transatlântico (Nova York -> Londres) ~ 5.570 km
        ("NY_to_London", 40.7128, -74.0060, 51.5074, -0.1278, 5570220.0),

        # Caso 3: Europa (Paris -> Berlim) ~ 877 km
        ("Paris_to_Berlin", 48.8566, 2.3522, 52.5200, 13.4050, 877460.0),

        # Caso 4: Extremos do globo (Linha do Equador -> Polo Norte) ~ 10.007 km
        ("Equator_to_NorthPole", 0.0, 0.0, 90.0, 0.0, 10007543.0),
    ]
)
def test_calculate_distance_real_cases(nome_rota, lat1, lon1, lat2, lon2, distancia_esperada_m):
    """Testa se a função retorna os valores esperados para rotas reais conhecidas."""
    distance = calculate(lat1, lon1, lat2, lon2)
    assert distance == pytest.approx(distancia_esperada_m, rel=0.01)

latitudes = st.floats(min_value=-90.0, max_value=90.0, allow_nan=False, allow_infinity=False)
longitudes = st.floats(min_value=-180.0, max_value=180.0, allow_nan=False, allow_infinity=False)

@given(lat1=latitudes, lon1=longitudes, lat2=latitudes, lon2=longitudes)
def test_calculate_distance_properties(lat1, lon1, lat2, lon2):
    """Testa propriedades gerais: simetria e resultados não-negativos."""
    distance = calculate(lat1, lon1, lat2, lon2)
    assert distance >= 0.0
    reverse_distance = calculate(lat2, lon2, lat1, lon1)
    assert distance == pytest.approx(reverse_distance, rel=1e-5, abs=1e-8)

@given(lat=latitudes, lon=longitudes)
def test_calculate_distance_identity(lat, lon):
    """Testa a propriedade de identidade: a distância de um ponto para ele mesmo é 0."""
    distance = calculate(lat, lon, lat, lon)
    assert distance == pytest.approx(0.0, abs=1e-8)