import io
import json
import os
import sys
from contextlib import redirect_stdout

import streamlit as st
from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

from app import run_react_agent  # noqa: E402
from mcp_server import MCPAcademicServer  # noqa: E402
from providers import get_llm_provider  # noqa: E402


load_dotenv()


def get_final_answer(trace_logs):
    for event in reversed(trace_logs):
        if event.get("action_type") == "FINAL_ANSWER":
            return event.get("output", "")
    return "Chưa có Final Answer."


def render_trace(trace_logs):
    for event in trace_logs:
        step = event.get("step", "?")
        st.markdown(f"### Step {step}")

        thought = event.get("thought")
        if thought:
            st.markdown("**Thought**")
            st.write(thought)

        if event.get("action_type") == "TOOL_EXECUTION":
            st.markdown("**Action**")
            st.code(event.get("tool_name", ""), language="text")

            st.markdown("**Arguments**")
            st.json(event.get("arguments", {}))

            st.markdown("**Observation**")
            st.json(event.get("observation", {}))

        if event.get("action_type") == "FINAL_ANSWER":
            st.markdown("**Final Answer**")
            st.write(event.get("output", ""))


def main():
    st.set_page_config(page_title="VinUni Academic ReAct Agent", page_icon="🎓")
    st.title("VinUni Academic ReAct Agent")

    provider = get_llm_provider()
    mcp_server = MCPAcademicServer()

    provider_name = provider.__class__.__name__
    model_name = getattr(provider, "model_name", os.getenv("LLM_MODEL", "N/A"))
    st.caption(f"Provider: {provider_name} | Model: {model_name}")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_trace" not in st.session_state:
        st.session_state.last_trace = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    user_query = st.chat_input("Nhập câu hỏi học vụ hoặc yêu cầu đặt lịch...")

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        with st.chat_message("assistant"):
            with st.spinner("ReAct Agent đang xử lý..."):
                captured_stdout = io.StringIO()
                with redirect_stdout(captured_stdout):
                    trace_logs = run_react_agent(user_query, provider, mcp_server)

                final_answer = get_final_answer(trace_logs)
                st.write(final_answer)

        st.session_state.messages.append({"role": "assistant", "content": final_answer})
        st.session_state.last_trace = trace_logs

    with st.expander("View ReAct Trace", expanded=False):
        if st.session_state.last_trace:
            render_trace(st.session_state.last_trace)
        else:
            st.info("Chưa có trace. Hãy gửi một câu hỏi để chạy ReAct Agent.")


if __name__ == "__main__":
    main()
