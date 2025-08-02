import streamlit as st
import requests
import json
from datetime import datetime
from components.summary_tools import render_summary_tools, generate_pdf
from components.voice_translator import VoiceTranslator

def render_chat_interface(api_url):
    """Render the chat interface component"""
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    
    # Check if we need to generate automatic advice based on profile
    if st.session_state.profile and len(st.session_state.messages) == 0:
        with st.spinner("Generating personalized advice based on your profile..."):
            try:
                # Send an initial message to get advice based on profile
                response = requests.post(
                    f"{api_url}/chat",
                    json={
                        "user_id": st.session_state.user_id,
                        "message": "Please provide me with financial advice based on my profile.",
                        "voice_input": False,
                        "chat_history": []
                    }
                )
                
                if response.status_code == 200:
                    chat_response = response.json()
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": chat_response["response"],
                        "summary_available": chat_response["summary_available"],
                        "audio_available": chat_response["audio_available"],
                        "tax_info": chat_response.get("tax_info")
                    })
            except Exception as e:
                st.error(f"Error generating automatic advice: {str(e)}")
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # If this is an assistant message, show appropriate tools
            if message["role"] == "assistant":
                # Create columns for tools
                tool_cols = st.columns([1, 1, 1])
                
                # Add PDF download button for all assistant messages
                with tool_cols[0]:
                    # Generate PDF from message content
                    pdf_content = f"""# Financial Assistant Response

{message["content"]}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                    pdf_bytes = generate_pdf(pdf_content)
                    
                    # Add download button for PDF
                    st.download_button(
                        "📄 Download as PDF",
                        data=pdf_bytes,
                        file_name=f"chat_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        help="Download this message as PDF"
                    )
                
                # If summary is available, show summary tools
                if message.get("summary_available", False):
                    render_summary_tools(message["content"], st.session_state.voice_translator)
                
                # If audio is available, show audio player and download button
                elif message.get("audio_available", False):
                    with tool_cols[1]:
                        with st.spinner("Generating audio..."):
                            try:
                                # Generate audio from text response - limit to first 300 characters to avoid issues
                                text_for_audio = message["content"][:300] if len(message["content"]) > 300 else message["content"]
                                audio_bytes = st.session_state.voice_translator.get_audio_bytes(text_for_audio)
                                
                                # Ensure we never have None bytes
                                if audio_bytes is None:
                                    audio_bytes = b""
                                
                                if audio_bytes and len(audio_bytes) > 0:
                                    # Show audio player
                                    st.audio(audio_bytes, format="audio/mp3")
                                    
                                    # Add download button for audio
                                    st.download_button(
                                        "🔊 Download Audio",
                                        data=audio_bytes,
                                        file_name=f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                        mime="audio/mp3"
                                    )
                            except Exception as e:
                                st.warning("Audio generation failed. Please try again.")
                # If neither summary nor audio is available, add audio generation option
                else:
                    with tool_cols[1]:
                        if st.button("🔊 Generate Audio", key=f"gen_audio_{hash(message['content'])}"):
                            with st.spinner("Generating audio..."):
                                try:
                                    # Generate audio from text response - limit to first 300 characters to avoid issues
                                    text_for_audio = message["content"][:300] if len(message["content"]) > 300 else message["content"]
                                    audio_bytes = st.session_state.voice_translator.get_audio_bytes(text_for_audio)
                                    
                                    # Ensure we never have None bytes
                                    if audio_bytes is None:
                                        audio_bytes = b""
                                    
                                    if audio_bytes and len(audio_bytes) > 0:
                                        # Show audio player
                                        st.audio(audio_bytes, format="audio/mp3")
                                        
                                        # Add download button for audio
                                        st.download_button(
                                            "🔊 Download Audio",
                                            data=audio_bytes,
                                            file_name=f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                            mime="audio/mp3"
                                        )
                                    else:
                                        st.warning("Audio generation failed. Please try again.")
                                except Exception as e:
                                    st.warning("Audio generation failed. Please try again.")
    
    # Chat input area with voice option
    col1, col2 = st.columns([6, 1])
    
    with col1:
        user_input = st.chat_input("Ask me about your finances...")
    
    with col2:
        voice_input = st.button("🎤", help="Click to speak")
    
    # Handle voice input
    if voice_input:
        st.info("Listening... Speak now.")
        voice_text = st.session_state.voice_translator.listen()
        
        if voice_text:
            user_input = voice_text
            st.info(f"Recognized: {voice_text}")
        else:
            st.error("Sorry, I couldn't understand that. Please try again.")
    
    # Process user input
    if user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(user_input)
        
        # Send message to backend
        with st.spinner("Thinking..."):
            try:
                # Prepare chat history for the API request
                chat_history = []
                for msg in st.session_state.messages:
                    if msg["role"] in ["user", "assistant"]:
                        chat_history.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                
                response = requests.post(
                    f"{api_url}/chat",
                    json={
                        "user_id": st.session_state.user_id,
                        "message": user_input,
                        "voice_input": voice_input,
                        "chat_history": chat_history
                    }
                )
                
                if response.status_code == 200:
                    chat_response = response.json()
                    
                    # Add assistant message to chat history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": chat_response["response"],
                        "summary_available": chat_response["summary_available"],
                        "audio_available": chat_response["audio_available"],
                        "tax_info": chat_response.get("tax_info")
                    })
                    
                    # Display assistant message
                    with st.chat_message("assistant"):
                        st.markdown(chat_response["response"])
                        
                        # Create columns for tools
                        tool_cols = st.columns([1, 1, 1])
                        
                        # Add PDF download button for all assistant messages
                        with tool_cols[0]:
                            # Generate PDF from message content
                            pdf_content = f"""# Financial Assistant Response

{chat_response["response"]}

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                            pdf_bytes = generate_pdf(pdf_content)
                            
                            # Add download button for PDF
                            st.download_button(
                                "📄 Download as PDF",
                                data=pdf_bytes,
                                file_name=f"chat_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                help="Download this message as PDF"
                            )
                        
                        # If summary is available, show summary tools
                        if chat_response["summary_available"]:
                            render_summary_tools(chat_response["response"], st.session_state.voice_translator)
                        
                        # If audio is available, generate and show audio player
                        if chat_response["audio_available"]:
                            with tool_cols[1]:
                                with st.spinner("Generating audio..."): 
                                    try:
                                        # Generate audio from text response - limit to first 300 characters to avoid issues
                                        text_for_audio = chat_response["response"][:300] if len(chat_response["response"]) > 300 else chat_response["response"]
                                        audio_bytes = st.session_state.voice_translator.get_audio_bytes(text_for_audio)
                                        
                                        # Ensure we never have None bytes
                                        if audio_bytes is None:
                                            audio_bytes = b""
                                        
                                        if audio_bytes and len(audio_bytes) > 0:
                                            # Show audio player
                                            st.audio(audio_bytes, format="audio/mp3")
                                            
                                            # Add download button for audio
                                            st.download_button(
                                                "🔊 Download Audio",
                                                data=audio_bytes,
                                                file_name=f"response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                                                mime="audio/mp3"
                                            )
                                        else:
                                            st.warning("Audio generation failed. Please try again.")
                                    except Exception as e:
                                        st.warning("Audio generation failed. Please try again.")
                        
                        
                        # If tax info is available, show a notification
                        if chat_response.get("tax_info"):
                            st.info("Tax information is available. Check the Tax Calculator tab for more details.")
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error communicating with backend: {str(e)}")
    
    # Clear chat button
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)