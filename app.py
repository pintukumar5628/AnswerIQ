import streamlit as st
import nltk
from nltk.corpus import words

# Download NLTK resources
nltk.download("words")

# Function to preprocess text
def preprocess_text(text):
    return str(text).lower().strip()

# Function to evaluate answers
def evaluate_answer(answer_text, keywords):
    # Preprocess the user's answer
    answer_text = preprocess_text(answer_text)
    keywords = preprocess_text(keywords).split(", ")

    # Count the number of keywords found in the answer
    matched_keywords = [kw for kw in keywords if kw in answer_text]
    score = len(matched_keywords)
    return score, matched_keywords

# Function to generate detailed analysis and feedback
def analyze_answer(answer_text):
    answer_text = preprocess_text(answer_text)

    # Analyze content relevance (e.g., number of English words)
    word_count = len(answer_text.split())
    valid_words = [word for word in answer_text.split() if word in words.words()]
    content_relevance = len(valid_words) / word_count if word_count > 0 else 0

    # Analyze grammar and spelling (simple check using valid words percentage)
    grammar_score = content_relevance * 100

    # Analyze coherence (word repetition as a measure of coherence)
    word_set = set(answer_text.split())
    coherence_score = len(word_set) / word_count if word_count > 0 else 0

    # Analyze length adequacy (e.g., based on an ideal length range)
    ideal_length = 50  # Define an arbitrary ideal word count
    length_adequacy = min(1.0, word_count / ideal_length)

    # Generate feedback
    feedback = []
    if content_relevance < 0.7:
        feedback.append("Improve content relevance by using more meaningful and accurate words.")
    if grammar_score < 80:
        feedback.append("Check grammar and spelling for errors.")
    if coherence_score < 0.8:
        feedback.append("Improve coherence by avoiding repetitive words or phrases.")
    if length_adequacy < 0.8:
        feedback.append(f"Expand your answer to meet the ideal length of {ideal_length} words.")

    # Return analysis
    analysis = {
        "Content Relevance": f"{content_relevance * 100:.2f}%",
        "Grammar and Spelling": f"{grammar_score:.2f}%",
        "Coherence": f"{coherence_score * 100:.2f}%",
        "Length Adequacy": f"{length_adequacy * 100:.2f}%",
    }
    feedback_text = " | ".join(feedback) if feedback else "Excellent answer!"
    return analysis, feedback_text

# Streamlit UI
st.title("Subjective Answer Evaluation System")
st.write("Evaluate your answers based on a given job description and keywords.")

# Text input for job description or question
job_description = st.text_area("Enter the Job Description or Question:", placeholder="Type the job description or question here.")

# Text input for predefined keywords
keywords = st.text_input("Enter Keywords (comma-separated):", placeholder="e.g., data analysis, machine learning, Python")

# Text input for user's answer
answer = st.text_area("Enter Your Answer:", placeholder="Type your answer here.")

if st.button("Evaluate Answer"):
    if job_description and keywords and answer:
        # Evaluate answers and generate detailed feedback
        score, matched_keywords = evaluate_answer(answer, keywords)
        analysis, feedback = analyze_answer(answer)

        # Display results
        st.subheader("Evaluation Results")
        st.write(f"**Score:** {score}")
        st.write(f"**Matched Keywords:** {matched_keywords}")
        st.write("### Detailed Analysis")
        st.json(analysis)
        st.write("### Feedback")
        st.write(feedback)
    else:
        st.error("Please fill in the Job Description, Keywords, and Answer fields to proceed.")
