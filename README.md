# Data Extraction and Text Analysis

## Objective

This GitHub repository contains a Python project that focuses on data extraction and text analysis. The primary objective of this assignment was to extract textual data articles from the provided URLs and perform text analysis to compute various variables, as explained below.

## Problem Statement

The task involved in this assignment was to extract text data from articles given in the "Input.xlsx" file and save each article's content in a separate text file. The program needed to ensure that it extracts only the article title and text, excluding any website header, footer, or other unnecessary content.

## Solution and Approach

To tackle this problem, I created two Python files, "Text_Analysis.py" and "Scrapper.py." The "Scrapper.py" file contains the code responsible for extracting data from the given URLs using Python libraries like Beautiful Soup and requests. The extracted text was then saved in separate text files based on the URL_ID.

Next, in the "Text_Analysis.py" file, I implemented various text analysis functions. The analysis included calculating variables such as positive and negative scores, polarity score, subjectivity score, average sentence length, percentage of complex words, FOG index, average number of words per sentence, complex word count, word count, syllables per word, personal pronouns count, and average word length.

The analysis was performed on each extracted text, and the output was stored in an Excel file with the exact format specified in the "Output Data Structure.xlsx" file.

## Technologies Used

- Python programming language
- Libraries used: Beautiful Soup, requests, pandas, NLTK (natural language toolkit)

## License

This project is licensed under the MIT License.

## How to Run

To run this project, follow these steps:

1. Clone this repository to your local machine.
2. Ensure you have Python and the required libraries installed (mentioned in the code).
3. Execute the "Scrapper.py" file to extract data from the provided URLs and save the text files.
4. Next, run the "Text_Analysis.py" file to perform the text analysis and generate the output Excel file.
5. Make sure to provide the input data in the "Input.xlsx" file as per the format specified.

## Timeline

The project was completed in approximately 6 days, but it can be done sooner depending on the complexity of the data and processing speed.

## Submission

To submit your solution, follow the instructions in the submission form. The submission should include:

- The "Scrapper.py" and "Text_Analysis.py" files.
- Output data in CSV or Excel format as specified in the "Output Data Structure.xlsx" file.
- Detailed instructions on how to run the project.

Feel free to explore the code and use it for your text analysis tasks. If you encounter any issues or have suggestions for improvements, please don't hesitate to open an issue or pull request on this GitHub repository. Happy coding!

---
