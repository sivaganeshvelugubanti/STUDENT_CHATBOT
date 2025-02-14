# STUDENT_CHATBOT
AI powered chat for student assistance in personalized learning and question sloving

1) The Learning Path Generator is a Flask-based web application designed to help users create personalized learning paths for various topics. It leverages the Gemini AI model to generate structured learning modules, detailed explanations, and quizzes. The application also integrates with the YouTube Data API to fetch relevant educational videos for each subtopic .

### **Prompt Classification & Output Formatting**

The chatbot classifies a student's prompt as either a **Topic** or a **Question** using **Natural Language Processing (NLP)** and formats the output accordingly.

---

### **1. Prompt Classification**
The chatbot first determines whether the user input is:
- **Topic** → A broad subject (e.g., *"Data Science"*)
- **Question** → A specific inquiry (e.g., *"What is Data Science?"*)

This classification is done using **NLP techniques**, such as:
- **Keyword Matching** (Checking if the input is a subject or contains interrogative words like "What," "How," etc.)
- **Machine Learning Models** (Classifying text based on a trained dataset)

---

### **2. Output Formatting Based on Classification**

#### **i) If the Prompt is a Topic:**
- The topic is divided into **five modules** based on difficulty level, progressing from **basic to advanced**.
- Each module includes a **YouTube video with the highest views** related to that topic.
- A **mini chatbot** is available on every page for **doubt clarifications**.
- At the end of all modules, a **quiz is conducted** to assess understanding.
- The **quiz results are projected** to evaluate the user's learning progress.

##### **Example Output:**
**User Prompt:** *"Machine Learning"*

**Chatbot Response:**
*"Machine Learning is a branch of AI that allows systems to learn from data. Below is a structured learning path for this topic:"*

| **Module** | **Level** | **Description** | **YouTube Video** |
|------------|----------|----------------|--------------------|
| **Module 1** | Beginner | Introduction to ML | [Top Video](YouTube_Link) |
| **Module 2** | Basic | Supervised & Unsupervised Learning | [Top Video](YouTube_Link) |
| **Module 3** | Intermediate | Feature Engineering & Model Training | [Top Video](YouTube_Link) |
| **Module 4** | Advanced | Deep Learning & Neural Networks | [Top Video](YouTube_Link) |
| **Module 5** | Expert | Reinforcement Learning & AI Applications | [Top Video](YouTube_Link) |

(*YouTube links are fetched dynamically based on real-time highest views.*)

---

#### **ii) If the Prompt is a Question:**
- The chatbot **answers the question step by step**, breaking the solution into **five clear steps** according to the question's complexity.
- Each step is explained in detail to ensure **better understanding**.

##### **Example Output:**
**User Prompt:** *"What is supervised learning?"*

**Chatbot Response:**
1. **Definition:** *Supervised learning is a type of Machine Learning where a model learns from labeled data.*
2. **Examples:** *It includes classification and regression models.*
3. **How It Works:** *The model is trained using input-output pairs.*
4. **Use Cases:** *Used in spam detection, image recognition, etc.*
5. **Resources:** *Here’s a top YouTube video explaining it:* [Top Video](YouTube_Link)

---

### **Conclusion**
By first classifying the prompt, the chatbot ensures a **structured learning experience**:
✔ **For Topics** → It provides **five difficulty-based modules** with YouTube resources, a chatbot for clarifications, and a quiz for assessment.
✔ **For Questions** → It delivers **step-by-step answers** for better comprehension.

This structure enhances **learning efficiency and engagement** for students.


