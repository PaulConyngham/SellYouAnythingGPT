#Hello world

import openai
import re
import streamlit as st


#weaviate_api_key = st.secrets["API_KEYS"]["weaviate"]
#openai.api_key = st.secrets["API_KEYS"]["openai"]

paulconyngham_url = "https://www.linkedin.com/in/paustevenlconyngham/"
coreintelligence_url ="https://www.coreintelligence.com.au/"
awapac2023_url = "https://advertisingweek.com/event/awapac-2023/"

st.set_page_config(page_title="MarketAnythingGPT", page_icon="✌️", layout="wide")
st.title("MarketAnythingGPT - Market Anything with GPT ✌️\n")
st.markdown("---")
st.header("a demo by [Core Intelligence](%s) for AWAPAC2023" %coreintelligence_url)
st.markdown("---")
#st.header("Under Construction, please check back later 🏗️👷")



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
    st.session_state.counter = 1
    st.session_state.current_func_dict = category_func_dict
    st.session_state.messages = []  # initialize messages



# Functions for each case for the dictionary mapping further down below in the script

def generate_conversation(model, messages):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages
    )
    assistant_msg = response['choices'][0]['message']['content']
    return assistant_msg

# Utility function to parse the assistant's message into separate categories
def parse_categories(message):
    # Remove any leading/trailing whitespace and split into lines
    lines = message.strip().split('\n')

    # Prepare a regex pattern to match numerical list items
    pattern = re.compile(r'^\d+\.\s*')

    # Remove numerical prefixes from each line and return the result
    return [pattern.sub('', line) for line in lines]

def initiate_categorization(product_name, feedback=None):
    conversation = [
        {"role": "system", "content": "You are an assistant that helps clarify user product inputs. Your task is to provide a list of possible product categories for a given product, not to assume one."},
        {"role": "user", "content": f"I have a product named {product_name}. Can you suggest the possible categories for it?"},
    ]
    if feedback:
        conversation.append({"role": "user", "content": feedback})

    assistant_msg = generate_conversation(st.session_state["openai_model"], conversation)

    # Parse the message into categories
    suggested_categories = parse_categories(assistant_msg)

    # Add 'other' option
    suggested_categories.append('other')

    # Show categories to the user
    return suggested_categories

def handle_category_choice(user_choice, suggested_categories):
    if suggested_categories[user_choice - 1] == 'other':
        return "Please type your category:"
    else:
        return f"You have chosen the category '{suggested_categories[user_choice - 1]}'. Is this correct? (yes/no)"

def confirm_category(user_confirmation):
    if user_confirmation.lower() in ["yes", "y"]:
        return True
    else:
        return "Please provide feedback to help identify the correct category."

def initiate_product_info_generation(product_name, category, feedback=None):
    conversation = [
        {"role": "system", "content": "You are an assistant that provides detailed information about a specific product in a given category. Provide information in a general sense, do not provide specific numbers on items. Finally provide your information in a list format"},
        {"role": "user", "content": f"I am selling a {product_name} in the {category} category. Can you provide more details about this product?"},
    ]
    if feedback:
        conversation.append({"role": "user", "content": feedback})

    assistant_msg = generate_conversation(st.session_state["openai_model"], conversation)
    product_details = assistant_msg.strip()

    return f"Detailed Information for {product_name}:\n{product_details}\nIs the above product information correct? (yes/no)"

def confirm_product_info(user_confirmation):
    if user_confirmation.lower() in ["yes", "y"]:
        return True
    else:
        return "Please specify what is wrong with the product details."


st.text("What product or service would you like to market?")

#"Send a message"


# After the functions are defined, initialize session state variables
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "counter" not in st.session_state:
    st.session_state["counter"] = 1
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Define the function dictionaries here, after the functions are defined
category_func_dict = {
    1: initiate_categorization,
    2: handle_category_choice,
    3: confirm_category,
}

product_info_func_dict = {
    1: initiate_product_info_generation,
    2: confirm_product_info,
}

# Now we can assign the function dictionary to the session state variable
st.session_state["current_func_dict"] = category_func_dict

def handle_chat():

    # React to user input
    if prompt := st.chat_input("What product or service would you like to market?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})

        # Get the function using the dictionary mapping
        func = st.session_state["current_func_dict"].get(st.session_state["counter"], lambda x: "Invalid choice")
        response = func(prompt)

        print(response)

        # Remove any empty strings from the list
        response = [sentence for sentence in response if sentence]

        # Join the list into a single string, with each sentence on a new line
        response = '\n'.join(response)

        # If the response is True, it means the user has confirmed something
        if response is True:
            if st.session_state["current_func_dict"] is category_func_dict:
                st.session_state["current_func_dict"] = product_info_func_dict  # Switch to the product info flow
            else:
                st.session_state["current_func_dict"] = category_func_dict  # Switch back to the category flow cf
            st.session_state["counter"] = 1  # Reset the counter
        else:
            if "no" in prompt.lower():
                st.session_state["counter"] -= 1  # Go back to the previous state
            else:
                st.session_state["counter"] += 1  # Go to the next state

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state["messages"].append({"role": "assistant", "content": response})

handle_chat()



