import streamlit as st
import io
import base64
from datetime import datetime

def render_summary_tools(content, voice_translator=None):
    """Render tools for exporting summaries as PDF or audio"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Copy to clipboard button
        st.button("📋 Copy Text", on_click=set_clipboard_data, args=(content,), help="Copy summary to clipboard")
    
    with col2:
        # Export as PDF button
        pdf_bytes = generate_pdf(content)
        # Ensure we never pass None to download_button
        if pdf_bytes is None:
            pdf_bytes = b""
            
        st.download_button(
            label="📄 Export as PDF",
            data=pdf_bytes,
            file_name=f"financial_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            help="Download summary as PDF"
        )
    
    with col3:
        # Export as audio button
        if voice_translator:
            # Limit text length for audio generation to avoid issues
            text_for_audio = content[:300] if len(content) > 300 else content
            
            # Check if we should generate audio or show the audio player
            audio_generated = False
            audio_bytes = None
            
            # Try to generate audio
            try:
                with st.spinner("Generating audio..."):
                    audio_bytes = voice_translator.get_audio_bytes(text_for_audio)
                    # Ensure we never have None bytes
                    if audio_bytes is None:
                        audio_bytes = b""
                    
                    if audio_bytes and len(audio_bytes) > 0:
                        audio_generated = True
            except Exception as e:
                st.warning("Could not generate audio for this content.")
            
            # If audio was generated successfully, show the player and download button
            if audio_generated:
                # Show audio player
                st.audio(audio_bytes, format="audio/mp3")
                
                # Add download button for audio
                st.download_button(
                    label="🔊 Export as Audio",
                    data=audio_bytes,
                    file_name=f"summary_audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3",
                    mime="audio/mp3",
                    help="Download summary as audio file"
                )
            else:
                # Show disabled button if audio generation failed
                st.download_button(
                    label="🔊 Export as Audio",
                    data=b"",  # Empty bytes instead of None
                    file_name="summary_audio.mp3",
                    mime="audio/mp3",
                    disabled=True,
                    help="Audio generation failed"
                )
        else:
            # If no voice translator is available, show disabled button
            st.download_button(
                label="🔊 Export as Audio",
                data=b"",  # Empty bytes instead of None
                file_name="summary_audio.mp3",
                mime="audio/mp3",
                disabled=True,
                help="Audio export not available"
            )

def set_clipboard_data(text):
    """Set text to clipboard using JavaScript"""
    # Create a JavaScript function to copy text to clipboard
    js_code = f"""
    <script>
    function copyToClipboard() {{
        const text = `{text}`;
        navigator.clipboard.writeText(text).then(() => {{
            // Show a success message
            const div = document.createElement('div');
            div.textContent = 'Copied to clipboard!';
            div.style.position = 'fixed';
            div.style.top = '10px';
            div.style.right = '10px';
            div.style.padding = '10px';
            div.style.background = 'rgba(0, 200, 0, 0.8)';
            div.style.color = 'white';
            div.style.borderRadius = '5px';
            div.style.zIndex = '9999';
            document.body.appendChild(div);
            
            // Remove the message after 2 seconds
            setTimeout(() => {{
                document.body.removeChild(div);
            }}, 2000);
        }}).catch(err => {{
            console.error('Failed to copy text: ', err);
        }});
    }}
    
    // Call the function
    copyToClipboard();
    </script>
    """
    
    # Display the JavaScript code
    st.components.v1.html(js_code, height=0)

def generate_pdf(content):
    """Generate a PDF from the content"""
    try:
        # In a real implementation, we would use ReportLab to generate a PDF
        # For now, we'll create a simple PDF with placeholder content
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        
        # Create a buffer for the PDF
        buffer = io.BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Create custom styles
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontSize=16,
            alignment=TA_CENTER,
            spaceAfter=20
        )
        
        normal_style = ParagraphStyle(
            'Normal',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_LEFT,
            spaceAfter=10
        )
        
        # Create the content
        elements = []
        
        # Add title
        elements.append(Paragraph("Financial Summary", title_style))
        elements.append(Spacer(1, 20))
        
        # Add date
        date_text = f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        elements.append(Paragraph(date_text, normal_style))
        elements.append(Spacer(1, 20))
        
        # Add content
        # Split content by lines and create paragraphs
        for line in content.split('\n'):
            if line.strip():
                elements.append(Paragraph(line, normal_style))
        
        # Build the PDF
        doc.build(elements)
        
        # Get the PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        st.error(f"Error generating PDF: {str(e)}")
        # Return an empty PDF as fallback
        empty_buffer = io.BytesIO()
        return empty_buffer.getvalue() or b""  # Ensure we never return None