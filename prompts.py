COT_GEN_PROMPT = """JOB DESCRIPTION: <<JD>>
NOTES: <<NOTES>>
RESUME: <<ENTRY>>"""
COMPARE_RESUME = """User Information:
<<FS>>
Use the above examples and the user information to suggest improvements. Explain your rationale before the final content.
<<USER_INFO>>
Education: <<USER_EDU>>
Entry:
"""