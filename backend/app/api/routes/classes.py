from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import pandas as pd
import os

router = APIRouter()

@router.get("/")
async def get_class():
    try:
        df = pd.read_csv("./classes.csv")
        
        # Tạo mảng các object với quantity mặc định là 0
        result = [
            {
                "className": class_name,
                "quantity": 0
            }
            for class_name in df["Class_Name"]
        ]
        
        response = {
            "message": "Read classes.csv successfully",
            "result": result
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

