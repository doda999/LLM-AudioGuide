import streamlit as st
import cv2
import numpy as np

from img_understanding import *
from text_generation import *

st.title("Audio Guide Maker")

file_path = st.file_uploader('Choose a file', type=['png', 'jpg', 'jpeg'])
if file_path:
    # バイト列を読み込む
    image_bytes = file_path.read()
    # バイト列からデコード
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    # 画像表示
    st.image(img, channels="BGR")
    
    # 作品名と画家名を取得
    title, painter = get_image_info(img)
    # 情報不明の場合、画像から説明文生成
    if title == "" or painter == "":
        caption = get_caption_from_img(img)
    # 情報が取得できた場合、作品名と画家名から説明文生成
    else:
        caption = get_caption_from_info(title, painter)
    
    st.write(caption)
    