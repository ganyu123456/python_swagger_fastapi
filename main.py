import uvicorn
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

# 定义验证 Token 的依赖函数
def verify_token(token: str):
    if token != "valid-token":
        raise HTTPException(status_code=400, detail="Invalid token")
    return token

# 定义获取当前用户的依赖
def get_current_user(token: str = Depends(verify_token)):
    return {"username": "user"}

# 定义计算器 API 路由
@app.get("/calculate/{a}/{b}", summary="Perform basic arithmetic operations")
async def calculate(a: int, b: int, current_user: dict = Depends(get_current_user)):
    """
    计算两数的加、减、乘、除。

    - **a**: 第一个整数
    - **b**: 第二个整数
    - **current_user**: 当前请求的用户
    """
    return {
        "user": current_user["username"],
        "add": a + b,
        "subtract": a - b,
        "multiply": a * b,
        "divide": a / b if b != 0 else "undefined"
    }

# 定义一个简单的根路径
@app.get("/", summary="Root endpoint")
async def root():
    """
    这是根路径，用于测试应用是否正常运行。
    """
    return {"message": "Welcome to the FastAPI Calculator!"}

# 提交测试3
# 定义启动方法
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
