import streamlit as st

from libs.bvcdatabase import (
    create_prompt,
    delete_prompt,
    read_prompt,
    read_use_model,
    update_prompt,
)


def page_prompt_manager(table: str):
    prompts = read_prompt(table, st.session_state.user)
    prompt_dict = st.selectbox(
        label="**提示词**",
        options=prompts,
        format_func=lambda x: f"{x["memo"]} == {x['model']} == {x['creator']}",
        key=f"{table}_prompt_dict",
    )
    tab_markdown, tab_text_area = st.tabs(["查看", "编辑"])
    with tab_text_area:
        prompt = st.text_area(
            "**提示词**",
            value=prompt_dict["prompt"],
            height=400,
            label_visibility="collapsed",
            key=f"{table}",
        )
    with tab_markdown:
        with st.container(height=402):
            st.markdown(prompt)

    col_memo, col_public, col_model, col_creator = st.columns(4)
    with col_memo:
        prompt_memo = st.text_input(
            "**备注**", value=prompt_dict["memo"], key=f"{table}_memo"
        )
    with col_public:
        prompt_public = st.selectbox(
            label="**公开**",
            options=[False, True],
            index=prompt_dict["public"],
            format_func=lambda x: "是" if x else "否",
            key=f"{table}_prompt_public",
        )
    with col_model:
        models = read_use_model()
        try:
            names = [model["name"] for model in models]
            index = names.index(prompt_dict["model"])
        except ValueError:
            st.toast("模型不在使用，请更新！")
            index = 0
        model_dict = st.selectbox(
            label="**模型**",
            options=models,
            index=index,
            format_func=lambda x: x["name"],
            key=f"{table}_model_dict",
        )
    with col_creator:
        prompt_creator = st.text_input(
            label="**作者**",
            value=prompt_dict["creator"],
            disabled=True,
            key=f"{table}_prompt_creator",
        )

    col_prompt_insert, col_prompt_update, col_prompt_delete = st.columns(3)
    with col_prompt_insert:
        if st.button(
            ":material/add: 添加",
            key=f"{table}_create_prompt",
            use_container_width=True,
        ):
            if st.session_state.user != "访客":
                create_prompt(
                    table=table,
                    prompt=prompt,
                    memo=prompt_memo,
                    model=model_dict["name"],
                    creator=st.session_state.user,
                    public=prompt_public,
                )
                st.rerun()
            else:
                st.toast("访客无法进行此项操作，请登录！")
    with col_prompt_update:
        if st.button(
            ":material/update: 更新",
            key=f"{table}_update_prompt",
            use_container_width=True,
        ):
            if st.session_state.user != "访客":
                if st.session_state.user == prompt_creator:
                    update_prompt(
                        table=table,
                        id=prompt_dict["id"],
                        prompt=prompt,
                        memo=prompt_memo,
                        model=model_dict["name"],
                        creator=st.session_state.user,
                        public=prompt_public,
                    )
                    st.rerun()
                else:
                    st.toast("无权限更新提示词")
            else:
                st.toast("访客无法进行此项操作，请登录！")
    with col_prompt_delete:
        if st.button(
            ":material/delete: 删除",
            key=f"{table}_delete_prompt",
            type="primary",
            use_container_width=True,
        ):
            if st.session_state.user != "访客":
                if st.session_state.user == prompt_creator:
                    delete_prompt(table=table, id=prompt_dict["id"])
                    st.rerun()
                else:
                    st.toast("无权限删除提示词")
            else:
                st.toast("访客无法进行此项操作，请登录！")
