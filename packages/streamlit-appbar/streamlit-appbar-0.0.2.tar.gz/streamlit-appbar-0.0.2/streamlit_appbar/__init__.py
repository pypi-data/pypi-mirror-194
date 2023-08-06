import os
import streamlit.components.v1 as components
import base64

_RELEASE = True

if not _RELEASE:
    _streamlit_appbar = components.declare_component(
        "streamlit-appbar",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _streamlit_appbar = components.declare_component("streamlit-appbar", path=build_dir)


def obj_to_image(obj: any):
    if type(obj) == str:
        ext = obj.split(".")[1]
        if ext == "svg":
            ext += "+xml"
        elif ext == "jpg":
            ext = "jpeg"
        with open(obj, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode()
            return f"data:image/{ext};base64, {encoded}"


def streamlit_appbar(title="", modes=[], logo="", bgColor="#F7F1E5", txtColor="#000000", height=90, default="", key=None):
    if logo != "":
        read_logo = obj_to_image(logo)
    else:
        read_logo = logo
    component_value = _streamlit_appbar(title=title, modes=modes, logo=read_logo, bgColor=bgColor, txtColor=txtColor, height=height, key=key, default=default)
    return component_value


if not _RELEASE:
    pass
    # import streamlit as st
    #
    # st.set_page_config(layout="wide")
    #
    # modes = [
    #     {"name": "Traduction",
    #      "icon": "Create"
    #      },
    #     {"name": "TLA",
    #      "icon": "TableView"
    #      },
    #     {"name": "Manuel",
    #      "icon": "MenuBook"
    #      },
    #     {"name": "Index",
    #      "icon": "List"
    #      },
    # ]
    #
    # mode = streamlit_appbar(title="PictOrtho", modes=modes, logo="icon.svg", bgColor="#FFFBF5", txtColor="#000000", height=90, key="mode")
    # st.write(st.session_state)
