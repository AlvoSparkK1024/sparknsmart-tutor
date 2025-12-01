import streamlit as st
import asyncio
import nest_asyncio
nest_asyncio.apply()
import os
import json
from dotenv import load_dotenv
load_dotenv()
from src.orchestration.orchestrator import Orchestrator

st.set_page_config(page_title="SPARKnSMART Energy Tutor", layout="wide")

st.title("SPARKnSMART Energy Tutor Agent")
st.markdown("Powered by **Google ADK (Gemini)** and **NotebookLM**")

# Sidebar for configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GEMINI_API_KEY", ""))
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    
    st.divider()
    st.info("Upload appliance data to start analysis.")

# Main area
col1, col2 = st.columns([1, 1])

import pypdf
from io import BytesIO

# ... imports ...

# Main area
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Input Material")
    
    input_type = st.radio("Input Type", ["PDF Document", "Raw Notes"])
    
    document_text = ""
    
    if input_type == "PDF Document":
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        if uploaded_file:
            try:
                # Extract text
                reader = pypdf.PdfReader(uploaded_file)
                for page in reader.pages:
                    document_text += page.extract_text() + "\n"
                
                # Extract images from PDF
                import fitz  # PyMuPDF
                pdf_images = []
                
                # Save uploaded file temporarily
                temp_pdf_path = "temp_uploaded.pdf"
                with open(temp_pdf_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                # Open with PyMuPDF to extract images
                pdf_document = fitz.open(temp_pdf_path)
                os.makedirs("outputs/pdf_images", exist_ok=True)
                
                for page_num in range(len(pdf_document)):
                    page = pdf_document[page_num]
                    image_list = page.get_images()
                    
                    for img_index, img in enumerate(image_list):
                        xref = img[0]
                        base_image = pdf_document.extract_image(xref)
                        image_bytes = base_image["image"]
                        
                        # Save image
                        image_path = f"outputs/pdf_images/page{page_num + 1}_img{img_index + 1}.png"
                        with open(image_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        pdf_images.append(image_path)
                
                pdf_document.close()
                
                st.success(f"✅ Extracted {len(document_text)} characters and {len(pdf_images)} images from PDF.")
                
                # Store in session state
                st.session_state["document_text"] = document_text
                st.session_state["pdf_images"] = pdf_images
                
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
    else:
        document_text = st.text_area("Paste your notes here", height=200)
        if document_text:
            st.session_state["document_text"] = document_text
    
    # Show question input only if document is loaded
    if "document_text" in st.session_state and st.session_state["document_text"]:
        st.markdown("---")
        st.markdown("### 💬 Ask Your Question")
        user_question = st.text_area(
            "What would you like to learn about this document?",
            placeholder="e.g., Explain the main concepts in simple terms...",
            height=100,
            key="user_question_input"
        )
        
        # Submit button
        if st.button("🎬 Generate Explanation & Visuals", type="primary", use_container_width=True):
            if user_question:
                st.session_state["generating"] = True
                st.session_state["current_question"] = user_question
                st.rerun()
            else:
                st.warning("Please enter a question first!")

with col2:
    st.subheader("📺 Explanation & Visuals")
    
    # Check if generation is in progress
    if st.session_state.get("generating"):
        document_text = st.session_state.get("document_text", "")
        question = st.session_state.get("current_question", "")
        
        progress_container = st.container()
        with progress_container:
            st.info(f"**Question:** {question}")
            
            overall_progress = st.progress(0)
            status_text = st.empty()
            
            # Step 1: Generate explanation using Gemini directly
            status_text.text("📝 Generating explanation...")
            overall_progress.progress(0.5)
            
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Create prompt
            prompt = f"""
You are an expert educator. Based on the following document, answer the user's question in a clear and engaging way.

Document Content:
{document_text[:8000]}

User Question:
{question}

Provide:
1. A detailed explanation (2-3 paragraphs) that directly answers the question
2. Suggest 2-3 visual aids that would help understand this concept (describe what each visual should show)

Format your response as:
EXPLANATION:
[Your detailed explanation here]

VISUAL 1: [Description of first visual aid]
VISUAL 2: [Description of second visual aid]
VISUAL 3: [Description of third visual aid (if applicable)]
"""
            
            try:
                response = model.generate_content(prompt)
                response_text = response.text
                
                # Parse response
                explanation = ""
                visual_prompts = []
                
                lines = response_text.split('\n')
                in_explanation = False
                
                for line in lines:
                    if 'EXPLANATION:' in line:
                        in_explanation = True
                        continue
                    elif line.startswith('VISUAL'):
                        in_explanation = False
                        # Extract visual description
                        visual_desc = line.split(':', 1)[1].strip() if ':' in line else line.strip()
                        if visual_desc:
                            visual_prompts.append(visual_desc)
                    elif in_explanation and line.strip():
                        explanation += line + "\n"
                
                status_text.text("✅ Complete!")
                overall_progress.progress(1.0)
                
                # Store results
                st.session_state["explanation"] = explanation.strip() if explanation.strip() else response_text
                st.session_state["visual_descriptions"] = visual_prompts
                st.session_state["generating"] = False
                st.rerun()
                
            except Exception as e:
                st.error(f"Error generating explanation: {e}")
                st.session_state["generating"] = False
    
    # Display results if available
    elif "explanation" in st.session_state and st.session_state["explanation"]:
        st.success("✅ Generation Complete!")
        st.info(f"**Your Question:** {st.session_state.get('current_question', '')}")
        
        st.markdown("---")
        st.markdown("### 📖 Explanation")
        st.markdown(st.session_state["explanation"])
        
        # Display extracted PDF images
        if st.session_state.get("pdf_images"):
            st.markdown("---")
            st.markdown("### 🖼️ Images from Your Document")
            
            pdf_images = st.session_state["pdf_images"]
            
            # Display in columns for better layout
            cols_per_row = 2
            for i in range(0, len(pdf_images), cols_per_row):
                cols = st.columns(cols_per_row)
                for j in range(cols_per_row):
                    if i + j < len(pdf_images):
                        with cols[j]:
                            st.image(pdf_images[i + j], caption=f"Image {i + j + 1}", use_container_width=True)
        
        # Display visual descriptions
        if st.session_state.get("visual_descriptions"):
            st.markdown("---")
            st.markdown("### 💡 Suggested Visual Concepts")
            st.caption("Additional visual aids that would help illustrate this topic:")
            
            for idx, visual_desc in enumerate(st.session_state["visual_descriptions"]):
                with st.expander(f"Visual Concept {idx + 1}", expanded=False):
                    st.write(visual_desc)
        
        # Clear button
        st.markdown("---")
        if st.button("🔄 Ask Another Question", use_container_width=True):
            st.session_state.pop("explanation", None)
            st.session_state.pop("visual_descriptions", None)
            st.session_state.pop("current_question", None)
            # Keep pdf_images as they're from the document
            st.rerun()
    
    else:
        st.info("📤 Upload a document and ask a question to get started!")
