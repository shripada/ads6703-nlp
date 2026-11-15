def test_health(client):
    assert client.get("/api/health").json() == {"ok": True}


def test_a_text_is_labelled_and_saved(client):
    r = client.post("/api/texts", json={"body": "My order is late"})
    assert r.status_code == 201
    assert r.json()["label"] == "complaint"
    assert [t["body"] for t in client.get("/api/texts").json()] == ["My order is late"]


def test_an_empty_text_is_refused(client):
    assert client.post("/api/texts", json={"body": ""}).status_code == 422


def test_the_same_question_calls_the_llm_once(client, fake_llm):
    first = client.post("/api/ask", json={"question": "What is UPI?"}).json()
    second = client.post("/api/ask", json={"question": "What is UPI?"}).json()
    assert first == {"answer": "answer to: What is UPI?", "saved": False}
    assert second["saved"] is True
    assert fake_llm.calls == 1
