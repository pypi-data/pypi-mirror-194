import copy
import os
import streamlit.components.v1 as components
from typing import Dict, List
import pandas as pd
import base64

_RELEASE = True

if not _RELEASE:
    _streamlit_freegrid = components.declare_component(
        "streamlit_freegrid",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _streamlit_freegrid = components.declare_component("streamlit_freegrid", path=build_dir)


def obj_to_image(obj: any):
    if type(obj) == str:
        with open(obj, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/jpeg;base64, {encoded}"


def streamlit_freegrid(df: pd.DataFrame,
                       labels: Dict[str, str] = {},
                       types: Dict[str, dict] = {},
                       hide: List[str] = [],
                       height: int = 400,
                       pageSize: int = 10,
                       key: str = None):
    temp_df = copy.deepcopy(df)
    for column in types:
        if types[column]["type"] == "image":
            temp_df[column] = temp_df[column].apply(lambda obj: obj_to_image(obj))
    component_value = _streamlit_freegrid(df=temp_df,
                                          labels=labels,
                                          types=types,
                                          hide=hide,
                                          height=height,
                                          pageSize=pageSize,
                                          key=key)
    return component_value


if not _RELEASE:
    pass
    # import streamlit as st
    # st.set_page_config(layout="wide")
    # df = pd.read_csv("table_v2.csv", sep="\t")
    # df["image"] = df["image"].apply(lambda path: "pictos/"+path)
    #
    # if "index_result" not in st.session_state:
    #     st.session_state["index_result"] = df.iloc[0:100]
    #
    # search_text = st.text_input("label", label_visibility="collapsed", key="search_text")
    # if search_text != "":
    #     st.session_state["index_result"] = df[df["word"].str.contains(search_text)]
    # st.write(st.session_state["index_result"])
    # streamlit_freegrid(
    #     df=st.session_state["index_result"],
    #     types={
    #         "image": {"type": "image"},
    #         "schematic": {"type": "bool"},
    #         "aac": {"type": "bool"},
    #         "aacColor": {"type": "bool"},
    #         "hair": {"type": "bool"},
    #         "skin": {"type": "bool"},
    #         "sex": {"type": "bool"},
    #         "violence": {"type": "bool"},
    #     },
    #     hide=["schematic", "aac", "aacColor", "hair", "skin", "sex", "violence", "downloads"],
    #     labels={
    #         "word": "Mots",
    #         "image": "Pictogramme",
    #         "_id": "Identifiant ARASAAC",
    #         "categories": "Catégories"
    #     },
    #     pageSize=30,
    #     key="index_sfg_result"
    # )
