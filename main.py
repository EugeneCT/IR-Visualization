import streamlit as st
import pandas as pd
import numpy as np
import json
import cv2
st.set_page_config(layout="wide")
st.title('IR visualization')
col1, col2 = st.columns(2)
col3, col4 = st.columns([2, 2])
uploaded_img = col1.file_uploader("Upload your image file here", type=[ 'jpg'] )
uploaded_json = col2.file_uploader("Upload your json file here",type=["json"])


if uploaded_img is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_img.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    
    scale_percent = 40 # percent of original size
    width = int(opencv_image.shape[1] * scale_percent / 100)
    height = int(opencv_image.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    # resize image
    resized = cv2.resize(opencv_image, dim, interpolation = cv2.INTER_AREA)
    imageLocation = col3.empty()

    imageLocation.image(resized, caption=uploaded_img.name)

# with open(bytes_data, 'r') as json_file:
if uploaded_json is not None:

    data = json.load(uploaded_json)
    class_dict={}
    for object in data["objects"]:
        try:
            class_dict[object["classTitle"]].append(object["points"]["exterior"])
        except:
            class_dict[object["classTitle"]]=[(object["points"]["exterior"])]

    radio_list=["All"]+list(class_dict.keys())

    genre = col4.radio(
        "Choose class Title",
        (radio_list))

    if genre!="All":
        for item in range(0,len(class_dict[genre])):
            x1=(class_dict[genre][item][0][0])* scale_percent / 100
            y1=(class_dict[genre][item][0][1])* scale_percent / 100
            x2=(class_dict[genre][item][1][0])* scale_percent / 100
            y2=(class_dict[genre][item][1][1])* scale_percent / 100
            color = (0, 255, 0)  # BGR color tuple (green in this case)
            thickness = 2
            cv2.rectangle(resized, (int(x1),int(y1)),(int(x2),int(y2)), color, thickness)
            imageLocation.image(resized, caption=uploaded_img.name)

    elif genre=="All":
        for keys in class_dict.keys():
            for item in range(0,len(class_dict[keys])):
                x1=(class_dict[keys][item][0][0])* scale_percent / 100
                y1=(class_dict[keys][item][0][1])* scale_percent / 100
                x2=(class_dict[keys][item][1][0])* scale_percent / 100
                y2=(class_dict[keys][item][1][1])* scale_percent / 100
                color = (0, 255, 0)  # BGR color tuple (green in this case)
                thickness = 2
                cv2.rectangle(resized, (int(x1),int(y1)),(int(x2),int(y2)), color, thickness)
                imageLocation.image(resized, caption=uploaded_img.name)

    # cv2.imshow('Image with Bounding Box', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
