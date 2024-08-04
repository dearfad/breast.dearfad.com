import streamlit as st
from datetime import datetime
from utils import chat, set_page_header, User, save_data
import pickle

set_page_header()

# if "messages" not in st.session_state:
#     st.session_state.messages = [
#         {"role": "user", "content": "你好"},
#         {"role": "assistant", "content": "大夫，你好"},
#     ]


role = st.selectbox("**类别**", ("游客", "学生", "教师", "管理员"))

match role:
    case "游客":
        pass
        # chapter = st.selectbox(
        #     "**章节**",
        #     ("breast",),
        #     format_func=lambda x: CHAPTER[x],
        # )
        # st.info("请用**正常语气**与随机一名患者沟通", icon=":material/counter_1:")
        # st.info("问诊完毕后请输入 **我问完了**", icon=":material/counter_2:")
        # st.info("回答患者提出的**相关问题**", icon=":material/counter_3:")
        # st.info(
        #     "**重新开始**请按 **F5** 或 :material/refresh: 页面",
        #     icon=":material/counter_4:",
        # )
        # st.info("作为一名**游客**，您的过程不被统计", icon=":material/counter_5:")
        # if st.button("开始", use_container_width=True):
        #     st.session_state.user = User(
        #         role=role, chapter=chapter, name="游客", grade="", major="", mode=""
        #     )
        #     st.session_state.user.create_chatlog()
        #     st.session_state.page = "inquiry"
        #     st.rerun()
    case "学生":
        pass
        # chapter = st.selectbox(
        #     "**章节**",
        #     ("breast",),
        #     format_func=lambda x: CHAPTER[x],
        # )
        # name = st.text_input("**姓名**", "学生")
        # grade = st.selectbox("**年级**", (range(2016, 2030, 1)))
        # major = st.selectbox("**专业**", ("临床医学", "放射", "口腔", "其他"))
        # mode = st.selectbox("模式", ("课堂练习", "自学测试", "出科考试"))

        # if st.button("开始", use_container_width=True):
        #     st.session_state.user = User(role, chapter, name, grade, major, mode)
        #     st.session_state.user.create_chatlog()
        #     st.session_state.page = "inquiry"

        #     st.rerun()
    case "教师":
        password = st.text_input("**密码**")
        if st.button("登录", use_container_width=True):
            if password == st.secrets['teacher_key']:
                st.switch_page("pages/teacher.py")
            else:
                st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")

    case "管理员":
        password = st.text_input("**密码**")
        if st.button("登录", use_container_width=True):
            if password == st.secrets['admin_key']:
                st.switch_page("pages/admin.py")
            else:
                st.warning(":material/key: **密码错误**，请咨询**管理员**相关信息")


def show_chat():
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("医"):
                st.write(message["content"])
        if message["role"] == "assistant":
            with st.chat_message("患"):
                st.markdown(f"**{message['content']}**")


def show_inquiries():
    user = st.session_state.user
    character_id = user.chatlog.loc[user.index, "id"]
    st.markdown(f"**就诊编号: {user.index +
                1} / {len(user.chatlog)}**")
    st.markdown(f"**:date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**")
    st.markdown(":page_facing_up: **谈话记录**")

    # col_left, col_center, col_right = st.columns([1, 3, 1])
    # with col_center:
    #     st.caption(
    #         f"患者编号：**{user.index+1} / {len(user.chatlog)}**")
    #     st.image(
    #         "https://cdn.seovx.com/d/?mom=302",
    #         caption=st.session_state.faker.name(),
    #         use_column_width=True,
    #     )

    show_chat()

    # 如果再次询问，不重新记录开始时间
    if user.chatlog.loc[user.index, "start_time"] == "":
        user.chatlog.loc[user.index, "start_time"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    if prompt := st.chat_input(""):
        if prompt != "我问完了":
            with st.chat_message("医"):
                st.write(prompt)
                st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("患"):
                response = chat(
                    role_server="xingchen",
                    character_id=character_id,
                    messages=st.session_state.messages,
                )
                st.markdown(f"**{response}**")
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
        else:
            user.chatlog.loc[user.index, "conversation_end_time"] = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            st.session_state.messages.append({"role": "user", "content": prompt})
            user.chatlog.loc[user.index, "messages"] = str(st.session_state.messages)
            st.session_state.page = "explain"
            st.rerun()


def show_question():
    user = st.session_state.user
    st.markdown(f"**就诊编号: {user.index +
                1} / {len(user.chatlog)}**")
    with st.container(border=True):
        st.markdown(":page_facing_up: **对话记录**")
        show_chat()

    case_question = user.chatlog.loc[user.index, "questions"]
    for index, question in enumerate(case_question):
        key = "a" + str(index)

        st.radio(
            f"**Q{index+1}: {question['question']}**", question["answer_list"], key=key
        )

    if st.button("再问一下", use_container_width=True):
        st.session_state.page = "inquiry"
        user.chatlog.loc[user.index, "inquiry_count"] += 1
        st.rerun()

    if st.button("提交答案", use_container_width=True):
        user.chatlog.loc[user.index, "end_time"] = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        for a in range(len(case_question)):
            k = "a" + str(a)
            case_question[a]["user_answer"] = st.session_state[k]

        user.index += 1
        if user.index == len(user.chatlog):
            save_data()
            st.session_state.page = "result"
        else:
            st.session_state.page = "inquiry"
            del st.session_state.messages
        st.rerun()


def show_result():
    user = st.session_state.user
    with st.container(border=True):
        col_name, col_grade, col_major = st.columns(3)
        with col_name:
            st.markdown(f"**姓名: {user.name}**")
        with col_grade:
            st.markdown(f"年级: {user.grade}")
        with col_major:
            st.markdown(f"专业: {user.major}")

        user_start_time = datetime.strptime(
            user.chatlog.loc[0, "start_time"], "%Y-%m-%d %H:%M:%S"
        )
        user_end_time = datetime.strptime(
            user.chatlog.loc[len(user.chatlog["questions"]) - 1, "end_time"],
            "%Y-%m-%d %H:%M:%S",
        )
        st.markdown(f":date: {user.chatlog.loc[0, 'start_time']}")
        st.markdown(f":stopwatch: {user_end_time-user_start_time}")

    score = 0
    total_questions_count = 0
    normal_inquiry_count = len(user.chatlog["questions"])
    total_inquiry_count = 0

    for i, question in enumerate(user.chatlog["questions"]):
        st.divider()
        start_time = datetime.strptime(
            user.chatlog.loc[i, "start_time"], "%Y-%m-%d %H:%M:%S"
        )
        conversation_end_time = datetime.strptime(
            user.chatlog.loc[i, "conversation_end_time"], "%Y-%m-%d %H:%M:%S"
        )
        end_time = datetime.strptime(
            user.chatlog.loc[i, "end_time"], "%Y-%m-%d %H:%M:%S"
        )
        col_question_left, col_question_right = st.columns(2)
        with col_question_left:
            st.markdown(f"**:ok_woman: {i+1}/{len(user.chatlog['questions'])}**")
        with col_question_right:
            st.markdown(
                f"**:stopwatch: {end_time-start_time} = {conversation_end_time-start_time} + {end_time-conversation_end_time}**"
            )
        with st.container(border=True):
            st.markdown("**对话记录**")
            st.markdown(f"**:repeat: {user.chatlog.loc[i, 'inquiry_count']}**")
            total_inquiry_count += user.chatlog.loc[i, "inquiry_count"]
            st.session_state.messages = eval(user.chatlog.loc[i, "messages"])
            show_chat()
        for q in question:
            total_questions_count += 1
            st.markdown(f"**Q{total_questions_count}: {q['question']}**")
            st.markdown(f"答案选项: 🔹{' 🔹'.join(q['answer_list'])}")
            st.markdown(f"正确答案: :white_check_mark:**{q['correct_answer']}**")
            if q["correct_answer"] == q["user_answer"]:
                score += 1
                st.markdown(f"用户回答: :white_check_mark:**{q['user_answer']}**")
            else:
                st.markdown(f"用户回答: :x:**:red[{q['user_answer']}]**")
    st.divider()
    question_score = round(score / total_questions_count * 100)
    inquiry_score = (total_inquiry_count - normal_inquiry_count) * 2
    st.markdown(f"**问题得分: {score} :material/pen_size_2: {
                total_questions_count} :material/close:100 :material/equal: {question_score}**")
    st.markdown(f"**复问扣分: ( {total_inquiry_count} - {
                normal_inquiry_count} ) :material/close:2 :material/equal: {inquiry_score}**")
    st.markdown(f"**最后得分: :small_orange_diamond: :red[{
                question_score - inquiry_score}] :small_orange_diamond:**")

    if st.button("返回首页", use_container_width=True):
        reset()
        st.rerun()





def show_teacher():
    with open("users.pkl", "rb") as file:
        users = pickle.load(file)

    st.selectbox(
        "**用户**",
        users,
        format_func=lambda x: user_select_option(x),
        key="user",
    )
    show_result()


# match st.session_state.page:
#     case "login":
#         show_login()
#     case 'teacher':
#         show_teacher()
#     case "admin":
#         st.switch_page("pages/admin.py")
#     case "inquiry":
#         show_inquiries()
#     case "explain":
#         show_question()
#     case "result":
#         show_result()
