# backend/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import SessionLocal, init_db, Mail
from schemas import MailIn, MailOut
from ml_model import predict

app = FastAPI(title="Phishing Detector Backend")

# CORS (allow Streamlit during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB tables
init_db()

# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/send_mail", response_model=MailOut)
def send_mail(mail: MailIn, db: Session = Depends(get_db)):
    new = Mail(
        sender=mail.sender,
        receiver=mail.receiver,
        subject=mail.subject,
        body=mail.body,
        prediction="Not Scanned"
    )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new

@app.get("/inbox", response_model=list[MailOut])
def get_inbox(db: Session = Depends(get_db)):
    mails = db.query(Mail).order_by(Mail.id.desc()).all()
    return mails

@app.post("/scan/{mail_id}")
def scan_mail(mail_id: int, db: Session = Depends(get_db)):
    mail = db.query(Mail).filter(Mail.id == mail_id).first()
    if not mail:
        raise HTTPException(status_code=404, detail="Mail not found")
    label, score = predict(mail.body)
    mail.prediction = f"{label}" + (f" ({score:.2f})" if score is not None else "")
    db.commit()
    return {"id": mail_id, "prediction": mail.prediction}

@app.post("/scan_all")
def scan_all(db: Session = Depends(get_db)):
    mails = db.query(Mail).all()
    for m in mails:
        label, score = predict(m.body)
        m.prediction = f"{label}" + (f" ({score:.2f})" if score is not None else "")
    db.commit()
    return {"status": "scanned", "count": len(mails)}

@app.delete("/mail/{mail_id}")
def delete_mail(mail_id: int, db: Session = Depends(get_db)):
    mail = db.query(Mail).filter(Mail.id == mail_id).first()
    if not mail:
        raise HTTPException(status_code=404, detail="Mail not found")

    db.delete(mail)
    db.commit()
    return {"status": "deleted", "id": mail_id}

