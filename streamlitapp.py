import streamlit as st
import time
from resumeobject import Resume

st.title("Resume Builder")
# Create placeholders for the text areas
job_description_placeholder = st.empty()
resume_experience_placeholder = st.empty()

# copy your text here for job description
job_description = job_description_placeholder.text_area("Job Description", height=200)
# copy your text here for resume experience section notes
resume_experience = resume_experience_placeholder.text_area("Resume Experience", height=200)

# if the user clicks the button generate resume object
if st.button("Generate Resume"):
    # Clear the text areas
    job_description_placeholder.empty()
    resume_experience_placeholder.empty()
    # create a resume object
    resume = None
    with st.spinner('Understanding Experiences'):
        resume = Resume(job_description, resume_experience)
    generating = False
    placeholder = st.empty()
    with st.spinner("Wait for it..."):
        # perform similarity search
        resume.perform_similarity_search()
        # generate resume
        resume.resume_generator(placeholder)
        # # display resume
        # st.write(resume.resume_updated)
        generating = True
        # remove the loading spinner
        st.balloons()

    if generating:
        # type success message
        st.success("Your resume is ready!")
        if st.button("Reset"):
            job_description_placeholder.empty()
            resume_experience_placeholder.empty()
            placeholder.empty()
            generating = False