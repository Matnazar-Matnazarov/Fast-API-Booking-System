from fastapi import FastAPI, Request
import time
import asyncio
from typing import Optional, Dict
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from redis import asyncio as aioredis
from functools import wraps

app = FastAPI()

# Redis connection
redis = aioredis.from_url(
    "redis://localhost",
    encoding="utf-8",
    decode_responses=True
)

# In-memory cache alternative
CACHE: Dict[str, dict] = {}
CACHE_TTL = 300  # 5 minutes in seconds

def cache_decorator(ttl_seconds: int = CACHE_TTL):
    def wrapper(func):
        @wraps(func)
        async def wrapped(*args, **kwargs):
            # Cache key yaratish
            cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"
            
            try:
                # Redis dan cache ni tekshirish
                cached_data = await redis.get(cache_key)
                if cached_data:
                    return eval(cached_data)
                
                # Agar cache da bo'lmasa, funksiyani bajarish
                result = await func(*args, **kwargs)
                
                # Natijani cache ga saqlash
                await redis.set(cache_key, str(result), ex=ttl_seconds)
                print(result)
                return result
                
            except aioredis.ConnectionError as e:
                # Redis ishlamasa in-memory cache ishlatish
                current_time = datetime.now()
                print(e)
                if cache_key in CACHE:
                    cached_item = CACHE[cache_key]
                    if current_time < cached_item['expires']:
                        return cached_item['data']
                
                result = await func(*args, **kwargs)
                CACHE[cache_key] = {
                    'data': result,
                    'expires': current_time + timedelta(seconds=ttl_seconds)
                }
                return result
                
        return wrapped
    return wrapper

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    if process_time >= 1:
        formatted_time = f"{process_time:.2f} s"
    else:
        process_time_ms = round(process_time * 1000, 2)
        formatted_time = f"{process_time_ms} ms"
    
    response.headers["X-Process-Time"] = formatted_time
    return response

@app.get("/")
async def root():
    return {"message": "Hello World"}

async def process_name(input_name: str) -> str:
    if not isinstance(input_name, str):
        raise ValueError("Input must be a string")
    
    if not input_name:
        raise ValueError("Input cannot be empty")
        
    # Minimal kutish vaqti
    await asyncio.sleep(0.001)
    
    # O'zgaruvchilarni saqlash uchun list yaratish o'rniga,
    # to'g'ridan to'g'ri stringni qaytarish
    return input_name

@app.get("/hello/{name}")
@cache_decorator(ttl_seconds=300)  # 5 minutlik cache
async def say_hello(name: str):
    try:
        h = 0
        for i in range(100000):
            h+=1
        h = 0
        if len(name) > 100:
            return JSONResponse(
                status_code=400,
                content={
                    "message": "Name is too long. Maximum length is 100 characters",
                    "status": "error"
                }
            )
            
        processed_name = await process_name(name)
        return {
            "message": f"Hello {processed_name}",
            "status": "success"
        }
    except ValueError as ve:
        return JSONResponse(
            status_code=400,
            content={
                "message": str(ve),
                "status": "error"
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Internal server error occurred",
                "status": "error",
                "error": str(e)
            }
        )

# Cache ni tozalash uchun endpoint
@app.post("/clear-cache")
async def clear_cache():
    try:
        # Redis cache ni tozalash
        await redis.flushdb()
        # In-memory cache ni tozalash
        CACHE.clear()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error clearing cache",
                "error": str(e)
            }
        )