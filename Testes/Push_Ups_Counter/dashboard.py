import streamlit as st
import pandas as pd
from personal_ai import *
import time

st.set_page_config(layout="wide")

personalAI = PersonalAI("landmark_test.mp4")
personalAI.run()

placeholder = st.empty()

status = "relaxed"
count = 0
direction = "down"

frame_count = 0

while True:
    if not personalAI.image_q.empty(): #pra se certificar de que há algo na fila
        frame, results, ts = personalAI.image_q.get()
        frame_count += 1

        if ts == "done":
            break
        
        if len(results.pose_landmarks) > 0:
            elbow_angle = personalAI.find_angle(results, 12, 14, 16)
            hip_angle = personalAI.find_angle(results, 11, 23, 25)
            #Lógica da flexão
            if elbow_angle > 150 and hip_angle > 170:
                status = "ready"
                direction = "down" #direção possível de seguir
            
            if status == "ready":
                if direction == "down" and elbow_angle < 90:
                    direction = "up"
                    count += 0.5
                    
                elif direction == "up" and elbow_angle  > 90:
                    direction = "down"
                    count += 0.5 
                    

    with placeholder.container():
        col1, col2 = st.columns([0.4, 0.6])  #40% para o vídeo e 60% para o restante
        
        col1.image(frame, caption = f"Frame {frame_count}")
        col2.markdown(f"##**Status:** {status}")
        col2.markdown(f"##**Contador:**{int(count)}")

time.sleep(0.1)