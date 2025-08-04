import streamlit as st
import math

st.set_page_config(page_title="Calculator", page_icon="🧮", layout="centered")

st.markdown(
    "<h1 style='text-align: center; color: #265E56;'>Web Calculator</h1>",
    unsafe_allow_html=True
)

# Styling
st.markdown("""
<style>
div.stButton > button {
    background-color: #FFCCCC;
    color: black;
    font-size: 22px;
    border-radius: 10px;
    height: 60px;
    width: 100%;
    margin-bottom: 5px;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "expression" not in st.session_state:
    st.session_state.expression = ""

# Button layout
buttons = [
    ["C", "x²", "√x", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    [".", "0", "=", "←"]
]

# Display field
st.text_input("Expression", value=st.session_state.expression, key="display", label_visibility="collapsed")

# Button click handler
def click(label):
    if label == "C":
        st.session_state.expression = ""
    elif label == "=":
        try:
            st.session_state.expression = str(eval(st.session_state.expression))
        except:
            st.session_state.expression = "Error"
    elif label == "x²":
        try:
            st.session_state.expression = str(eval(f"({st.session_state.expression})**2"))
        except:
            st.session_state.expression = "Error"
    elif label == "√x":
        try:
            st.session_state.expression = str(math.sqrt(float(eval(st.session_state.expression))))
        except:
            st.session_state.expression = "Error"
    elif label == "←":
        st.session_state.expression = st.session_state.expression[:-1]
    else:
        st.session_state.expression += label

# Render buttons
for row in buttons:
    cols = st.columns(4)
    for i, label in enumerate(row):
        cols[i].button(label, key=f"btn_{label}", on_click=click, args=(label,))
