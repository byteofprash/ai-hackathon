from fastapi import FastAPI, WebSocket
import random
import pandas
import os
import pandas as pd

os.environ["OPENAI_API_KEY"] = "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"
df = pd.read_csv('./notebook/prash.csv', encoding="utf-8")

from langchain.agents import create_pandas_dataframe_agent
from langchain.schema.agent import AgentAction
from langchain.llms import OpenAI

app = FastAPI()


pd_agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=True, 
prefix="""acceptReferrals means referral is accepted. 
rejectReferrals means referral is rejected. 
acceptCoupon means coupon is accepted. 
rejectCoupon means coupon is rejected.
Group the sessions whenever working with effect_type, is_first_session, session_revenue. 
setDiscount gives discount. 
setDiscountPerItem gives discount. 
addLoyaltyPoints adds loyalty points. 
Give the numbers in human readable separated by commas and truncate decimal to 2. 
When working with session use session_created_date. 
Whenever asked about discount value always use the discount_value field. 
Use the discount_value with session_revenue when asked about discount percentage.
Also display the intermediate steps in as part of the final answer
""", return_intermediate_steps=True)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            text = await websocket.receive_text()
            # Send message to the client
            answer = pd_agent({"input": text})
            logs = []
            for step in answer["intermediate_steps"]:
                if type(step[0]) == AgentAction:
                    logs.append(step[0].log)
            # resp = {'value': random.uniform(0,1)}
            resp = {'answer': answer["output"], "steps": logs}
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')
