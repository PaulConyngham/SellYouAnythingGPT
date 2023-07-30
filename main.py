#Hello world

import openai
import streamlit as st


#weaviate_api_key = st.secrets["API_KEYS"]["weaviate"]
#openai.api_key = st.secrets["API_KEYS"]["openai"]

st.set_page_config(page_title="SellYouAnythingGPT", page_icon="💦", layout="wide")
st.header("Help GPT sell your mother in-law!💦\n")


COMPLETIONS_MODEL = "gpt-3.5-turbo"

paulconyngham_url = "https://www.linkedin.com/in/paustevenlconyngham/"
coreintelligence_url ="https://www.coreintelligence.com.au/"
awapac2023_url = "https://advertisingweek.com/event/awapac-2023/"

with st.sidebar:
    st.markdown("# About 🙌")
    st.markdown(
        "SellYouAnyThingGPT - input a product you would like \n"
        "to sell. Sit back, relax & let GPT do the rest \n"
        "\n"
        "Especially good at selling mothers in-law\n"
        )
    st.markdown("---")
    st.markdown("A side project by [Paul Conyngham](%s)" %paulconyngham_url)
    st.markdown("of [Core Intelligence](%s)" %coreintelligence_url)
    st.markdown("a demo for [AWAPAC2023](%s)" %awapac2023_url)


with st.chat_message("user"):
    st.write("Hello 👋")