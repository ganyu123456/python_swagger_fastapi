from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import numpy as np
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许所有来源的跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 或者设置为你前端的具体 URL
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

class CalculationResult(BaseModel):
    result: float


class CleanedDataResult(BaseModel):
    cleaned_data: List[float]


@app.get("/calculate", response_model=CalculationResult)
def calculate(
        num1: float = Query(..., description="第一个数字"),
        num2: float = Query(..., description="第二个数字"),
        operation: str = Query(..., description="选择操作：add, subtract, multiply, divide")
):
    """
    计算两个数的加减乘除。
    """
    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise ValueError("除数不能为零")
        result = num1 / num2
    else:
        raise ValueError("无效的操作类型")

    return CalculationResult(result=result)


def slope_cleaning(data: List[float], threshold: float) -> List[float]:
    """
    斜率清洗操作，清除掉异常点
    """
    cleaned_data = [data[0]]  # 保留第一个点
    for i in range(1, len(data) - 1):
        slope1 = data[i] - data[i - 1]
        slope2 = data[i + 1] - data[i]
        if abs(slope1 - slope2) < threshold:
            cleaned_data.append(data[i])  # 保留符合条件的点
    cleaned_data.append(data[-1])  # 保留最后一个点
    return cleaned_data


@app.post("/slope_cleaning", response_model=CleanedDataResult)
def clean_slope_data(data: List[float], threshold: float = Query(5.0, description="斜率变化阈值")):
    """
    对输入数据进行斜率清洗
    """
    cleaned_data = slope_cleaning(data, threshold)
    return CleanedDataResult(cleaned_data=cleaned_data)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
