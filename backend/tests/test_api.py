import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import Base, engine, SessionLocal
from app.database.seed_data import seed_database

@pytest.fixture(scope="session", autouse=True)
def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

def test_health():
    with TestClient(app) as client:
        res = client.get("/api/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

def test_districts():
    with TestClient(app) as client:
        res = client.get("/api/districts")
        assert res.status_code == 200
        districts = res.json()
        assert len(districts) >= 30
        erode = next((d for d in districts if d["name_en"] == "Erode"), None)
        assert erode is not None
        
        # Test taluks for Erode
        taluks_res = client.get(f"/api/taluks/{erode['id']}")
        assert taluks_res.status_code == 200
        taluks = taluks_res.json()
        assert len(taluks) >= 4
        bhavani = next((t for t in taluks if t["name_en"] == "Bhavani"), None)
        assert bhavani is not None

def test_crops():
    with TestClient(app) as client:
        res = client.get("/api/crops")
        assert res.status_code == 200
        crops = res.json()
        assert len(crops) >= 30
        paddy = next((c for c in crops if c["name_en"] == "Paddy"), None)
        assert paddy is not None

def test_pattams():
    with TestClient(app) as client:
        res = client.get("/api/pattams")
        assert res.status_code == 200
        pattams = res.json()
        assert len(pattams) >= 5

def test_signup_login_flow():
    with TestClient(app) as client:
        phone = "9876543210"
        signup_payload = {
            "full_name": "Murugan Farmer",
            "mobile_number": phone,
            "email": "murugan.farmer@agri-ai.com",
            "password": "strongPassword123",
            "preferred_language": "ta"
        }
        res = client.post("/api/auth/signup", json=signup_payload)
        if res.status_code == 400:
            # Already exists
            login_res = client.post("/api/auth/login", json={"username": phone, "password": "strongPassword123"})
            assert login_res.status_code == 200
            token = login_res.json()["access_token"]
        else:
            assert res.status_code == 200
            token = res.json()["access_token"]

        # Test me
        me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        assert me_res.json()["full_name"] == "Murugan Farmer"

def test_prediction_and_recommendation_flow():
    with TestClient(app) as client:
        login_res = client.post("/api/auth/login", json={"username": "9876543210", "password": "strongPassword123"})
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Get Erode and Paddy
        districts = client.get("/api/districts").json()
        erode = next(d for d in districts if d["name_en"] == "Erode")
        taluks = client.get(f"/api/taluks/{erode['id']}").json()
        bhavani = taluks[0]
        crops = client.get("/api/crops").json()
        paddy = next(c for c in crops if c["name_en"] == "Paddy")

        pred_payload = {
            "district_id": erode["id"],
            "taluk_id": bhavani["id"],
            "crop_id": paddy["id"],
            "pattam": "Aadi Pattam (Monsoon Sowing)",
            "land_area_acres": 3.0,
            "soil_type": "Clay Loam",
            "irrigation_type": "Canal Irrigation",
            "soil_ph": 6.8,
            "soil_n": 260.0,
            "soil_p": 19.0,
            "soil_k": 220.0
        }

        pred_res = client.post("/api/predict", json=pred_payload, headers=headers)
        assert pred_res.status_code == 200
        pred_data = pred_res.json()
        assert pred_data["predicted_yield_per_acre"] > 1000.0
        assert pred_data["total_production_kg"] == round(pred_data["predicted_yield_per_acre"] * 3.0, 1)
        assert len(pred_data["factors"]) > 0

        pred_id = pred_data["id"]

        # Test recommendations
        rec_res = client.get(f"/api/recommendations/{pred_id}", headers=headers)
        assert rec_res.status_code == 200
        rec_data = rec_res.json()
        assert len(rec_data["timeline_stages"]) >= 5
        assert "what_should_i_do_now" in rec_data

        # Test prediction chatbot
        chat_res = client.post("/api/chat/prediction", json={
            "prediction_id": pred_id,
            "message": "How can I increase my yield in this paddy farm?"
        }, headers=headers)
        assert chat_res.status_code == 200
        assert len(chat_res.json()["message"]) > 20

def test_chatbot_guardrail():
    with TestClient(app) as client:
        login_res = client.post("/api/auth/login", json={"username": "9876543210", "password": "strongPassword123"})
        token = login_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Off-topic question
        off_topic = client.post("/api/chat/general", json={"message": "Who won the cricket world cup?"}, headers=headers)
        assert off_topic.status_code == 200
        assert off_topic.json()["is_refusal"] == True
