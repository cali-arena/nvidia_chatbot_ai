"""
Final Assessment Frontend Server
Gradio interface mounted on FastAPI
"""

import gradio as gr
import os
from fastapi import FastAPI
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

route = os.environ.get("APP_ROOT_PATH")

#####################################################################
## Final App Deployment

from frontend_block import get_demo

demo = get_demo()
demo.queue()

logger.warning("Starting FastAPI app")
app = FastAPI()
app = gr.mount_gradio_app(app, demo, '/', root_path=route)

@app.get("/health")
async def health():
    return {"success": True}, 200

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Frontend Server on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
