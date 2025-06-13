from fastapi import APIRouter, HTTPException, Depends
from app.models.base import SessionLocal
from app.models.order import Order, OrderStatus
from sqlalchemy.orm import Session
import uuid
import threading
import time
import requests
import os
import logging

router = APIRouter(prefix="/ai-call", tags=["ai-call"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-call")

task_status = {}

# 你需要在.env或环境变量中配置以下信息
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "your-elevenlabs-api-key")
ELEVENLABS_AGENT_ID = os.getenv("ELEVENLABS_AGENT_ID", "wyCA1CqE6chkD28n2JpT")
ELEVENLABS_PHONE_NUMBER_ID = os.getenv("ELEVENLABS_PHONE_NUMBER_ID", "+18057492501")

# 调用ElevenLabs batch calling API

def call_elevenlabs_batch(phone_number, call_name="ai-call-task"):
    url = "https://api.elevenlabs.io/v1/convai/batch-calling/submit"
    payload = {
        "call_name": call_name,
        "agent_id": ELEVENLABS_AGENT_ID,
        "agent_phone_number_id": ELEVENLABS_PHONE_NUMBER_ID,
        "recipients": [
            {"phone_number": phone_number}
        ]
    }
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    logger.info(f"[AI-CALL] ElevenLabs batch call payload: {payload}")
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    logger.info(f"[AI-CALL] ElevenLabs batch call response: {response.status_code}, {response.text}")
    response.raise_for_status()
    return response.json()

def update_agent_prompt(agent_id, api_key, first_message, system_prompt):
    url = f"https://api.elevenlabs.io/v1/convai/agents/{agent_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "conversation_config": {
            "agent": {
                "first_message": first_message,
                "prompt": system_prompt
            }
        }
    }
    response = requests.patch(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()

def ai_call_task(task_id, order_id, first_message, system_prompt):
    logger.info(f"[AI-CALL] 任务启动: task_id={task_id}, order_id={order_id}")
    db: Session = SessionLocal()
    order = None
    try:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            logger.error(f"[AI-CALL] 未找到订单: order_id={order_id}")
            task_status[task_id] = "fail"
            return
        logger.info(f"[AI-CALL] 更新Agent prompt: order_id={order_id}")
        update_agent_prompt(ELEVENLABS_AGENT_ID, ELEVENLABS_API_KEY, first_message, system_prompt)
        logger.info(f"[AI-CALL] 开始外呼: order_id={order_id}, phone={order.phone}")
        result = call_elevenlabs_batch(order.phone, call_name=f"order_{order_id}")
        logger.info(f"[AI-CALL] 外呼成功: order_id={order_id}, result={result}")
        order.status = OrderStatus.success
        db.commit()
        task_status[task_id] = "success"
    except Exception as e:
        logger.error(f"[AI-CALL] 外呼失败: order_id={order_id}, error={e}")
        if order:
            order.status = OrderStatus.fail
            db.commit()
        task_status[task_id] = f"fail: {str(e)}"
    finally:
        db.close()
        logger.info(f"[AI-CALL] 任务结束: task_id={task_id}, order_id={order_id}")

@router.post("/start")
def start_ai_call(order_id: int, first_message: str, system_prompt: str):
    task_id = str(uuid.uuid4())
    logger.info(f"[AI-CALL] 新建任务: task_id={task_id}, order_id={order_id}")
    task_status[task_id] = "pending"
    thread = threading.Thread(target=ai_call_task, args=(task_id, order_id, first_message, system_prompt))
    thread.start()
    return {"task_id": task_id}

@router.get("/status/{task_id}")
def get_task_status(task_id: str):
    status = task_status.get(task_id, "not_found")
    logger.info(f"[AI-CALL] 查询任务: task_id={task_id}, status={status}")
    return {"task_id": task_id, "status": status} 