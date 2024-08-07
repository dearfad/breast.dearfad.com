import streamlit as st
import random
import pandas as pd

import pickle
import os


CHAPTER = {
    "乳房疾病": "breast",
}


@st.cache_data
def read_cases(path):
    return pd.read_json(path, orient="records")


def reset_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]


def save_data():
    if not os.path.exists("data/users.pkl"):
        users = [st.session_state.user]

        with open("data/users.pkl", "wb") as file:
            pickle.dump(users, file)
    else:
        with open("data/users.pkl", "rb") as file:
            users = pickle.load(file)
        users.append(st.session_state.user)

        with open("data/users.pkl", "wb") as file:
            pickle.dump(users, file)


def load_data():
    with open("data/users.pkl", "rb") as file:
        users = pickle.load(file)
    return users


def user_info_formatter(user):
    match user.role:
        case "游客":
            return str(f"{user.name} - {user.chatlog.loc[0, "start_time"]}")

        case "学生":
            return str(
                f"{user.name} - {user.chatlog.loc[0, "start_time"]} - {user.grade}级 - {user.major}专业"
            )
