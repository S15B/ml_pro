def test_predict_smoke(client, good_row):
    r = client.post("/v1/predict", json=good_row)
    assert r.status_code == 200
    body = r.json()
    assert 0.0 <= body["price"] <= 100_000_000
    assert isinstance(body["price"], float)
    assert body["latency_ms"] >= 0
    assert body["model_version"]


def test_predict_handles_missing_mortgage_rate(client, good_row):
    r = client.post("/v1/predict", json={**good_row, "mortgage_rate": None})
    assert r.status_code == 200

def test_predict_handles_missing_usd_rate(client, good_row):
    r = client.post("/v1/predict", json={**good_row, "usd_rate": None})
    assert r.status_code == 200


def test_batch_and_single_agree(client, good_row):
    s1 = client.post("/v1/predict", json=good_row).json()["price"]
    s2 = client.post("/v1/predict", json=good_row).json()["price"]
    assert abs(s1 - s2) < 1e-12
