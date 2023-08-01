#Hello world

import openai
import streamlit as st


#weaviate_api_key = st.secrets["API_KEYS"]["weaviate"]
#openai.api_key = st.secrets["API_KEYS"]["openai"]

paulconyngham_url = "https://www.linkedin.com/in/paustevenlconyngham/"
coreintelligence_url ="https://www.coreintelligence.com.au/"
awapac2023_url = "https://advertisingweek.com/event/awapac-2023/"

st.set_page_config(page_title="MarketAnythingGPT", page_icon="💦", layout="wide")
st.title("MarketAnythingGPT - Market Anything with GPT 💦\n")
st.markdown("---")
st.header("a demo by [Core Intelligence](%s) for AWAPAC2023" %coreintelligence_url)



with st.sidebar:
    st.markdown("# About 🙌")
    st.markdown(
        "MarketAnyThingGPT - input a product you would like \n"
        "to market or sell. Sit back, relax & let GPT do the rest \n"
        "\n"
        )
    st.markdown("---")
    st.markdown("A side project by [Paul Conyngham](%s)" %paulconyngham_url)
    st.markdown("of [Core Intelligence](%s)" %coreintelligence_url)
    st.markdown("a demo for [AWAPAC2023](%s)" %awapac2023_url)




openai.api_key = st.secrets["OPENAI_API_KEY"]


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"



def categorize_product(product_name):
    confirmation = False
    product_category = ""
    feedback = ""

    while not confirmation:
        conversation = [
            {"role": "system", "content": "You are an assistant that helps clarify user product inputs. Your task is to provide a list of possible product categories for a given product, not to assume one."},
            {"role": "user", "content": f"I have a product named {product_name}. Can you suggest the possible categories for it?"},
        ]
        if feedback:
            conversation.append({"role": "user", "content": feedback})

        # Use the LLM to generate product categories
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"] ,
            messages=conversation
        )

        # Extract the assistant message from the response
        assistant_msg = response['choices'][0]['message']['content']

        # Parse the message into categories
        suggested_categories = parse_categories(assistant_msg)

        # Add 'other' option
        suggested_categories.append('other')

        # Show categories to the user
        for i, category in enumerate(suggested_categories):
            print(f"{i + 1}. {category}")

        # Ask user to select a category
        user_choice = int(input("Please select a category by typing the corresponding number:\n"))

        # Check if user chose 'other'
        if suggested_categories[user_choice - 1] == 'other':
            product_category = input("Please type your category:\n")
        else:
            product_category = suggested_categories[user_choice - 1]

        # Confirm category with user
        user_confirmation = input(f"You have chosen the category '{product_category}'. Is this correct? (yes/no)\n")
        if user_confirmation.lower() in ["yes", "y"]:
            confirmation = True
        else:
            print("Please provide feedback to help identify the correct category.")
            feedback = input()

    return product_category


if "messages" not in st.session_state:
    st.session_state.messages = []

def clear_text():
    st.session_state["input"] = ""

# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("What product or service would you like to advertise", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = categorize_product(user_input)

    # store the output 
    st.session_state.past.append(user_input)
    #st.session_state.generated.append(output)




