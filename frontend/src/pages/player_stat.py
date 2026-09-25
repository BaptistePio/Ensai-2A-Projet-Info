import streamlit as st
import requests
import logging

# Setup logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Player Statistics")

    # Get player ID from query parameters
    # st.query_params returns a dict-like object
    query_params = st.query_params
    player_id = query_params.get("id_player")

    if not player_id:
        st.error("No player ID provided. Please add '?id_player=X' to the URL.")
        return

    logger.info(f"Fetching details for player ID: {player_id}")

    # API Configuration (assuming backend is running on localhost:8000)
    # In a real scenario, this URL should be an environment variable
    API_URL = f"http://localhost:8000/player/{player_id}"

    try:
        response = requests.get(API_URL)
        
        # Check if the request was successful
        if response.status_code == 200:
            player_data = response.json()
            logger.info(f"Successfully retrieved data for player: {player_data.get('username')}")

            # Display Player Information
            st.subheader(f"👤 {player_data.get('username', 'Unknown User')}")

            col1, col2 = st.columns(2)

            with col1:
                # Display ELO using st.metric
                elo = player_data.get("elo", 0)
                st.metric(label="ELO Rating", value=elo)

            with col2:
                # Display Email
                email = player_data.get("email", "N/A")
                st.write(f"📧 **Email:** {email}")
                
                # Display Pokemon Fan status using st.checkbox
                # Note: st.checkbox is usually for input, but we can use it to display state
                is_pokemon_fan = player_data.get("is_pokemon_fan", False)
                st.checkbox("Pokémon Fan", value=is_pokemon_fan, disabled=True)

        elif response.status_code == 404:
            st.error("Player not found.")
            logger.warning(f"Player ID {player_id} not found (404).")
        else:
            st.error(f"Failed to fetch player data. Status code: {response.status_code}")
            logger.error(f"API Error: {response.status_code} - {response.text}")

    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Is it running?")
        logger.error("Connection error: Backend API is unreachable.")
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        logger.exception("An unexpected error occurred during player stats retrieval.")

if __name__ == "__main__":
    main()
