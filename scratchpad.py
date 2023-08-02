 def handle_chat():

    # React to user input
    if prompt := st.chat_input("What product or service would you like to market?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state["messages"].append({"role": "user", "content": prompt})

        # Define the arguments dictionary here before calling the function
        args = {
            'product_name': st.session_state.get('product_name'),
            'user_choice': st.session_state.get('user_choice'),
            'user_confirmation': st.session_state.get('user_confirmation'),
            'category': st.session_state.get('category'),
            'feedback': st.session_state.get('feedback'),
            'suggested_categories': st.session_state.get('suggested_categories')  # Using get method in case suggested_categories is not present
        }

        if 'suggested_categories' not in st.session_state:
            initiate_categorization(args)
        else:
            func = st.session_state["current_func_dict"].get(st.session_state["counter"], lambda x: "Invalid choice")
            response = func(args)

        # Get the function using the dictionary mapping
        func = st.session_state["current_func_dict"].get(st.session_state["counter"], lambda x: "Invalid choice")
        response = func(args)

        # If the response is True, it means the user has confirmed something
        if response is True:
            if st.session_state["current_func_dict"] is category_func_dict:
                st.session_state["current_func_dict"] = product_info_func_dict  # Switch to the product info flow
            else:
                st.session_state["current_func_dict"] = category_func_dict  # Switch back to the category flow
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



############

# working (ish) code  

# need to refactor all of the OpenAI functions

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Setting up functions to handle the different text input flows
counter = 0

def case_select_LLMs(counter, prompt):
    if counter == 1:
        return categorize_product(prompt)
    elif counter == 2:
        return "You chose B"
    elif counter == 3:
        return "You chose C"
    else:
        return "Invalid choice"

# React to user input
if prompt := st.chat_input("What product or service would you like to market?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    counter += 1

    print(prompt)

    response = case_select_LLMs(counter, prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

#########################

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#output
with st.chat_message("user"):
    st.write("Hello 👋")

with st.chat_message("assistant"):
    st.write("Hello human")

#input
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

##################################






# Step 2: Create text input for product name
product_name = st.text_input("Enter the product name:")

# Step 3: Call the function with the entered product name
if product_name:
    product_category = categorize_product(product_name)

    # Step 4: Store the product category in the session state
    st.session_state["product_category"] = product_category

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to market?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})




    #############

import streamlit as st

st.title("Echo Bot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])




####


def clear_text():
    st.session_state["input"] = ""

# We will get the user's input by calling the get_text function
def get_text():
    input_text = st.text_input("What product or service would you like to advertise?", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = categorize_product(user_input)

    # store the output 
    st.session_state.past.append(user_input)
    #st.session_state.generated.append(output)