import streamlit as st
from libs.bvcpage import set_page_header
from libs.bvcutils import set_current_user
from libs.bvcdatabase import select_all_model, update_all_model, add_model

set_page_header(layout="wide")

with st.expander("模型设定", icon="🚨", expanded=True):
    models = select_all_model()
    modified_models = st.data_editor(
        models,
        num_rows="fixed",
        use_container_width=True,
        hide_index=True,
        disabled=("id",),
        column_config={
            "use": st.column_config.CheckboxColumn(
                "使用",
            ),
            "free": st.column_config.CheckboxColumn(
                "免费",
            ),
            "price_input": st.column_config.ProgressColumn(
                "输入价格/千tokens",
                format="%f",
                min_value=0,
                max_value=0.1,
            ),
            "price_output": st.column_config.ProgressColumn(
                "输出价格/千tokens",
                format="%f",
                min_value=0,
                max_value=0.1,
            ),
        },
        height=600,
    )
    col_add, col_update, col_delete = st.columns(3)
    with col_add:
        if st.button(
            ":material/add: **添加**",
            use_container_width=True,
            ):
            add_model()            
    with col_update:
        if st.button(
            ":material/update: **更新**",
            disabled=modified_models.equals(models),
            use_container_width=True,
            type="primary",
        ):
            update_all_model(modified_models)
            st.rerun()
    with col_delete:
        if st.button(
            ":material/delete: **删除**",
            use_container_width=True,
            ):
            pass

if st.button("退出登录", use_container_width=True, type="primary"):
    set_current_user(st.session_state.cookie_controller, name="游客")
    st.switch_page("clinic.py")

if st.button("返回首页", use_container_width=True):
    st.switch_page("clinic.py")
