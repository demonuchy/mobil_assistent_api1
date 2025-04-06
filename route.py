from datetime import timedelta, datetime
from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from fastapi.responses import RedirectResponse
from db_manager.shem import UserShem
from db_manager.query import get_user, add_user
from acces_token import create_access_token
from logger import logger
from speach_model import process_audio


public_router = APIRouter()

@public_router.get("/test")
async def test():
    return {"status" : 200}

@public_router.post("/register")
async def register(user : UserShem):
    user_entity = user.model_dump()
    print(user_entity)
    is_exists_user = await get_user(user_entity)
    if is_exists_user:
        raise HTTPException(
            status_code=400, 
            detail="Username already registered"
        )
    await add_user(user_entity)
    return RedirectResponse(url=f"/login?user={user}")


@public_router.post("/login")
async def login(user : UserShem):
    user_entity = user.model_dump()
    is_exists_user = await get_user(user_entity)
    if not is_exists_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email, "email" : user.email, "password" : user.password})
    return {"access_token": access_token}
    


private_router = APIRouter()

@private_router.post("/traslate")
async def traslate_audio(audio_file : UploadFile = File(...)):
    try:
        if not audio_file:
            pass
        file_data = await audio_file.read()
        dialog = await process_audio(file_data)
        return {"dialog" : dialog}
    except:
        pass

@private_router.post("/protected")
async def test(request : Request):
    print("ИДИ НАХУЙ")
   


