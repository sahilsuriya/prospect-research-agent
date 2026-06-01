from fastapi import FastAPI
from pydantic import BaseModel

from database import engine, SessionLocal
from models import Base, Company
from scraper import enrich_company
from fastapi.middleware.cors import CORSMiddleware
import json

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

@app.post("/enrich")
def enrich(data: URLRequest):

    result = enrich_company(data.url)

    db = SessionLocal()

    row = Company(
        website_name=result["website_name"],
        company_name=result["company_name"],
        address=result["address"],
        mobile_number=result["mobile_number"],
        mail=json.dumps(result["mail"]),
        core_service=result["core_service"],
        target_customer=result["target_customer"],
        probable_pain_point=result["probable_pain_point"],
        outreach_opener=result["outreach_opener"]
    )

    db.add(row)
    db.commit()
    db.close()

    return result


@app.get("/results")
def get_results():

    db = SessionLocal()

    companies = db.query(Company).all()

    response = []

    for c in companies:
        response.append({
            "website_name": c.website_name,
            "company_name": c.company_name,
            "address": c.address,
            "mobile_number": c.mobile_number,
            "mail": json.loads(c.mail),
            "core_service": c.core_service,
            "target_customer": c.target_customer,
            "probable_pain_point": c.probable_pain_point,
            "outreach_opener": c.outreach_opener
        })

    db.close()

    return response