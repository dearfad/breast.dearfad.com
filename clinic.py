import streamlit as st

from libs.bvcclasses import Role, User
from libs.bvcdatabase import check_user_exist, user_login
from libs.bvcpage import set_page_header, show_role_info
from libs.bvcutils import reset_session_state, validate_register

set_page_header()

reset_session_state()

role = st.selectbox("**类别**", Role)

show_role_info(role)

match role:
    case Role.VISITOR:
        if st.button("**开始**", use_container_width=True):
            st.session_state.doctor = User()
            st.switch_page("pages/inquiry.py")

    case Role.STUDENT:
        mode = st.selectbox("**模式**", ("课堂学习", "自学测试", "出科考试"))
        name = st.text_input("**姓名**", "学生")
        grade = st.selectbox("**年级**", (range(2015, 2030, 1)))
        major = st.selectbox(
            "**专业**", ("临床医学 5+3 一体化", "临床医学 5 年制", "放射医学", "其他")
        )
        if st.button("**开始**", use_container_width=True):
            st.session_state.doctor = User(
                role=role, mode=mode, name=name, grade=grade, major=major
            )
            st.switch_page("pages/inquiry.py")

    case Role.TEACHER:
        username = st.text_input("**用户名**")
        password = st.text_input("**密码**", type="password")        
        st.session_state.user_exist = True if check_user_exist(username) else False
        col_register, col_login = st.columns(2)
        with col_register:
            if st.button("**注册**", use_container_width=True, type="primary", disabled=st.session_state.user_exist):
                if password:
                    validate_register(username, password)
                else:
                    st.warning("**请输入密码**")
        with col_login:
            if st.button("**登录**", use_container_width=True, disabled=not st.session_state.user_exist):
                if user_login(username, password):
                    st.session_state.user = User(role=role, name=username)
                    st.switch_page("pages/teacher.py")
                else:
                    st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")

    case Role.ADMIN:
        password = st.text_input("**密码**", type="password")
        if st.button("**登录**", use_container_width=True):
            st.session_state.doctor = User(role=role)
            if password == st.secrets["admin_key"]:
                st.switch_page("pages/admin.py")
            else:
                st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")