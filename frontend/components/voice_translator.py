import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import streamlit as st

class VoiceTranslator:
    def __init__(self):
        """Initialize the voice translator"""
        self.recognizer = sr.Recognizer()
        self.temp_dir = tempfile.gettempdir()
    
    def listen(self, timeout=5, phrase_time_limit=5):
        """Listen for speech and convert to text"""
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
                # Convert speech to text
                text = self.recognizer.recognize_google(audio)
                return text
        except sr.WaitTimeoutError:
            st.warning("No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            st.warning("Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results; {e}")
            return None
        except Exception as e:
            st.error(f"Error: {str(e)}")
            return None
    
    def text_to_speech(self, text, lang='en'):
        """Convert text to speech and return the audio file path"""
        try:
            # Create a temporary file for the audio
            temp_file = os.path.join(self.temp_dir, "tts_output.mp3")
            
            # Generate speech
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(temp_file)
            
            return temp_file
        except Exception as e:
            st.error(f"Error generating speech: {str(e)}")
            return None
    
    def get_audio_bytes(self, text, lang='en'):
        """Convert text to speech and return the audio bytes"""
        # Return empty bytes if no text is provided (instead of None)
        if not text or len(text.strip()) == 0:
            st.warning("No text provided for audio generation")
            return b""  # Return empty bytes instead of None
            
        try:
            # Sanitize text for TTS (remove special characters that might cause issues)
            sanitized_text = ''.join(c for c in text if c.isprintable())
            
            # Ensure we have at least some text to convert
            if not sanitized_text or len(sanitized_text.strip()) == 0:
                st.warning("Text contains no valid characters for audio generation")
                return b""  # Return empty bytes instead of None
            
            # Create a temporary file for the audio
            temp_file = os.path.join(self.temp_dir, f"tts_output_{os.urandom(4).hex()}.mp3")
            
            # Generate speech directly
            tts = gTTS(text=sanitized_text, lang=lang, slow=False)
            tts.save(temp_file)
            
            if os.path.exists(temp_file):
                # Read the audio file
                with open(temp_file, "rb") as f:
                    audio_bytes = f.read()
                
                # Clean up the temporary file
                try:
                    os.remove(temp_file)
                except Exception:
                    pass  # Ignore cleanup errors
                
                # Ensure we have valid audio bytes
                if audio_bytes and len(audio_bytes) > 0:
                    return audio_bytes
                else:
                    st.warning("Generated audio file was empty")
                    return b""  # Return empty bytes instead of None
            else:
                st.warning("Failed to create audio file")
                return b""  # Return empty bytes instead of None
        except Exception as e:
            st.error(f"Error getting audio bytes: {str(e)}")
            return b""  # Return empty bytes instead of None