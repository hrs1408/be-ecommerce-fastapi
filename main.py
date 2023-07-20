from fastapi import FastAPI
from fastapi_responseschema import wrap_app_responses
from passlib.context import CryptContext
from sqlalchemy.orm import sessionmaker
from starlette.staticfiles import StaticFiles

import models
from database.database import engine
from routes.auth_route import auth
from routes.category_route import category
from routes.media_route import media
from routes.product_route import product
from routes.user_route import user
from schemas.schema import Route

models.Base.metadata.create_all(bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI(
    title="Ecommerce API",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="2.5.0",
)
wrap_app_responses(app, Route)


@app.on_event("startup")
def start_up_event():
    db = SessionLocal()
    root_user = db.query(models.User).filter(models.User.email == "admin@gmail.com").first()
    if not root_user:
        admin = models.User(email="admin@gmail.com", hashed_password=pwd_context.hash("Admin@123"),
                            user_role=models.UserRole.SUPPER_ADMIN, is_active=True)
        db.add(admin)
        db.commit()
        db.refresh(admin)


app.include_router(prefix="/api", router=auth)
app.include_router(prefix="/api", router=user)
app.include_router(prefix="/api", router=category)
app.include_router(prefix="/api", router=product)
app.include_router(prefix="/api", router=media)
app.mount("/medias", StaticFiles(directory="medias"), name="medias")
