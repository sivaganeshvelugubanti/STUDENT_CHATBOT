# STUDENT_CHATBOT
AI powered chat for student assistance in personalized learning and question sloving

1) The Learning Path Generator is a Flask-based web application designed to help users create personalized learning paths for various topics. It leverages the Gemini AI model to generate structured learning modules, detailed explanations, and quizzes. The application also integrates with the YouTube Data API to fetch relevant educational videos for each subtopic .

2)# Prompt Classification & Output Formatting

The chatbot classifies a student's prompt as either a Topic or a Question using Natural Language Processing (NLP) and formats the output accordingly.

i) Prompt Classification

The chatbot first determines whether the user input is:

**Topic → A broad subject (e.g., "Data Science")

**Question → A specific inquiry (e.g., "What is Data Science?")

**This classification is done using NLP techniques, such as:

**Keyword Matching (Checking if the input is a subject or contains interrogative words like "What," "How," etc.)

**Machine Learning Models (Classifying text based on a trained dataset)
 Output Formatting Based on Classification

i) If the Prompt is a Topic:

  1)The topic is divided into five modules based on difficulty level, progressing from basic to advanced.

  2)Each module includes a YouTube video with the highest views related to that topic.

  3)A mini chatbot is available on every page for doubt clarifications.

  4)At the end of all modules, a quiz is conducted to assess understanding.

The quiz results are projected to evaluate the user's learning progress.

ii) If the Prompt is a Question:

   1)The chatbot answers the question step by step, breaking the solution into five clear steps according to the question's complexity.

   2)Each step is explained in detail to ensure better understanding.

  **Example Output:

   User Prompt: "What is supervised learning?"

   **Chatbot Response:

   1)Definition: Supervised learning is a type of Machine Learning where a model learns from labeled data.

   2)Examples: It includes classification and regression models.

   3)How It Works: The model is trained using input-output pairs.

   4)Use Cases: Used in spam detection, image recognition, etc.
