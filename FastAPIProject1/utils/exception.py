import traceback
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette import status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

DEBUG_MODE= True

#http异常
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code":exc.status_code,
            "message": exc.detail,
            "data": None
        }
    )

#数据库异常
async def integrity_error_handler(request: Request, exc: IntegrityError):
            error_msg=str(exc.orig)
            if "username_UNIQUE" in error_msg or "Duplicate entry" in error_msg:
                detail="用户已存在"
            elif "FOREIGN KEY" in error_msg:
                detail="关联数据不存在"
            else:
                detail="数据约束错误，请检查输入"
            error_data=None
            if DEBUG_MODE:
                error_data={
                    "error_type":"IntegrityError",
                    "error_detail":error_msg,
                    "path":str(request.url)
                }
            return JSONResponse(
                content={
                    "code":"400",
                    "message": detail,
                    "data": error_data
                }
            )

#sqlalchemy异常
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    error_data=None
    if DEBUG_MODE:
        error_data={
            "error_type":type(exc).__name__,
            "error_detail":str(exc),
            "traceback":traceback.format_exc(),   #完整的错误堆栈
            "path":str(request.url)
        }
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code":"500",
            "message": "数据库操作失败，请稍后再试",
            "data": error_data
        }
    )
async def general_exception_handler(request: Request, exc: Exception):
    error_data=None
    if DEBUG_MODE:
        error_data={
            "error_type":type(exc).__name__,
            "error_detail":str(exc),
            "traceback":traceback.format_exc(),   #完整的错误堆栈
            "path":str(request.url)
        }
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code":"500",
                "message": "服务器内部错误",
                "data": error_data
            }
        )






