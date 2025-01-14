# -*- coding: utf-8 -*


instruction_template = """# GOAL #
Carefully analyze the HTML FILE CONTENT below, extract question-and-answer pairs from it. We will use the extracted Q&A data to fine-tune the language model later.
The granularity of the extracted question-and-answer pairs should not be too fine. Try to avoid extracting overly detailed question-and-answer pairs.
Extract one to two of the most concise and suitable questions from each HTML FILE.
Let's work this out in a step by step way to be sure we have the right answer.

# HTML FILE CONTENT #
{}

# RETURN AS A JSON #
{{"reasoning": "the reasoning process", "Q&A": [{{"Question": "A specific question extracted from the HTML FILE CONTENT above.", "Answer": "The answer to the Question."}}]}}"""

sys_message = "You are an trustworthy AI assistant that is very good at summarizing and organizing HTML file content."
