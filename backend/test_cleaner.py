from parsers.text_cleaner import clean_text


sample_text = """
    John Doe


    Python     SQL        Git


    Machine Learning
"""

result = clean_text(sample_text)

print("CLEANED TEXT:")
print("----------------")
print(result)