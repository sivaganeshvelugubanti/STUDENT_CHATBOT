from flask import Flask, render_template, request,jsonify
from flask import render_template_string

import google.generativeai as genai
import requests
import re
import markdown
global entry1,entry2,entry3,entry4,entry5,entry6,entry7
global txt1,link1
global txt2,link2
global txt3,link3
global txt4,link4
global txt5,link5
global txt6,link6
entry1=0
entry2=0
entry3=0
entry4=0
entry5=0
entry6=0

modules_dict = {}
app = Flask(__name__)

# Set up the Generative AI model
genai.configure(api_key="genai api key")
model = genai.GenerativeModel("gemini-1.5-flash")
def gemini_api_response(user_input):
   
    #prompt="do exactly what i say don't do any thing extra give me a  quiz on topics() it should have exactly 8 question remember exactly 5 questions and 4 options for each and here me this is the main part  all questions and options you give me must be in the form of a dictionaty named as quiz_q all the questions must be the keys and options must be in the form of the lists  and corext answers myst be returnet seperatly in a list named as quiz_a"
    response = model.generate_content(user_input)
    response_text =response.text
    # Replace this function with actual API call to Gemini 1.5
    # For now, simulate a response
    return response_text

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

def classify_prompt(prompt):
    """
    Classifies a given prompt as either a 'topic' or a 'question'.
    """
    prompt = str(prompt)
    print(prompt)
    prompt = prompt.strip()
    if re.search(r'\b(what|how|why|when|where|who|which|can|is|are|does|did|should|could|would|explain|define|solve|find|calculate)\b', prompt, re.IGNORECASE):
        return "question"
    elif prompt.endswith('?'):
        return "question"
    return "topic"



def generate_learning_path(search_query):
    global modules_dict
    # search_query = request.form.get("search_query")
    ip = f"Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 6 main topics for {search_query}. The 6 main topics should be divided into modules, with the 1st module covering the basics and introduction. The topics should become more advanced as we progress to the next modules. Remember, under each module, you should give me exactly 5 subtopics for that particular module. The response you provide must be structured: first, list all 5 modules, then list all the subtopics. Remember, just give me the names of the topics and subtopics, and don't provide any additional information."

    response = model.generate_content(ip)
    response_text =response.text
    # Initialize the dictionary to store modules and their subtopics
    

    # Split the content into modules and subtopics
    modules = response_text.split('**Module')

    for module in modules[1:]:
        # Extract the module name and subtopics
        module_lines = module.strip().split('\n')
        module_name = module_lines[0].strip()  # Get module name (e.g., Module 1: Introduction to Linear Algebra)
        
        # Find the subtopics by extracting lines starting with a number
        subtopics = []
        for line in module_lines[1:]:
            if line.strip().startswith(str(len(subtopics) + 1)):
                subtopics.append(line.strip()[3:])  # Remove the numbering (e.g., "1." becomes "")
        
        # Add module and subtopics to the dictionary
        modules_dict[module_name] = subtopics
        subtopics = []
    del modules_dict['s:**']  # Removes the key 'b' and its value
    return render_template("results3.html", modules=modules_dict)
def get_youtube_urls(topics, api_key="youtube api key", max_results=1):
    search_url= "https://www.googleapis.com/youtube/v3/search"
    video_details_url = "https://www.googleapis.com/youtube/v3/videos"
    results = {}
    for topic in topics:
        params = {
            "part": "snippet",
            "q": topic,
            "type": "video",
            "order": "viewCount",  # Fetch most popular videos by view count
            "maxResults": max_results,
            "key": api_key
        }
        
        search_response = requests.get(search_url, params=params)
        
        if search_response.status_code == 200:
            video_data = search_response.json()
            video_ids = [item['id']['videoId'] for item in video_data.get("items", [])]

            # Get details for the fetched videos
            details_params = {
                "part": "contentDetails",
                "id": ",".join(video_ids),
                "key": api_key
            }

            details_response = requests.get(video_details_url, params=details_params)
            if details_response.status_code == 200:
                details_data = details_response.json()
                embeddable_videos = [
                    f"https://www.youtube.com/embed/{item['id']}"
                    for item in details_data.get("items", [])
                    if not item['contentDetails'].get("regionRestriction", {}).get("blocked", False)
                ]
                results[topic] = embeddable_videos
            else:
                print(f"Error fetching details for videos: {details_response.status_code}")
                results[topic] = []
        else:
            print(f"Error fetching videos for topic '{topic}': {search_response.status_code}")
            results[topic] = []
    print("----------------------------------------------------------------------------------------")
    print(list(results.values()))
    print("----------------------------------------------------------------------------------------")
    return list(results.values())
@app.route("/1")
def module_1():
    global entry1
    global txt1
    global link1
    if entry1==0:
        txt1=[]
        txt1.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[0]][0]).text)
        txt1.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[0]][1]).text)
        txt1.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[0]][2]).text)
        txt1.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[0]][3]).text)
        txt1.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[0]][4]).text)    
        link1=get_youtube_urls(modules_dict[list(modules_dict.keys())[0]])
        entry1=entry1+1
        return render_template("modules/moduke1v2.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[0]],text=txt1,links=link1)
    else:
        return render_template("modules/moduke1v2.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[0]],text=txt1,links=link1)
@app.route("/2")
def module_2():
    global entry2
    global txt2
    global link2
    if entry2==0:
        txt2=[]
        txt2.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[1]][0]).text)
        txt2.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[1]][1]).text)
        txt2.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[1]][2]).text)
        txt2.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[1]][3]).text)
        txt2.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[1]][4]).text)    
        link2=get_youtube_urls(modules_dict[list(modules_dict.keys())[1]])
        entry2=1
        return render_template("modules/module2.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[1]],text=txt2,links=link2)
    else:
        return render_template("modules/module2.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[1]],text=txt2,links=link2)
@app.route("/3")
def module_3():
    global entry3
    global txt3
    global link3
    if entry3==0:
        txt3=[]
        txt3.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[2]][0]).text)
        txt3.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[2]][1]).text)
        txt3.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[2]][2]).text)
        txt3.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[2]][3]).text)
        txt3.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[2]][4]).text)    
        link3=get_youtube_urls(modules_dict[list(modules_dict.keys())[2]])
        entry3=1
        return render_template("modules/module3.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[2]],text=txt3,links=link3)
    else:
        return render_template("modules/module3.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[2]],text=txt3,links=link3)
@app.route("/4")
def module_4():
    global entry4
    global txt4
    global link4
    if entry4==0:
        txt4=[]
        txt4.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[3]][0]).text)
        txt4.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[3]][1]).text)
        txt4.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[3]][2]).text)
        txt4.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[3]][3]).text)
        txt4.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[3]][4]).text)    
        link4=get_youtube_urls(modules_dict[list(modules_dict.keys())[3]])
        entry4=1
        return render_template("modules/module4.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[3]],text=txt4,links=link4)
    else:
        return render_template("modules/module4.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[3]],text=txt4,links=link4)
@app.route("/5")
def module_5():
    global entry5
    global txt5
    global link5
    if entry5==0:
        txt5=[]
        txt5.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[4]][0]).text)
        txt5.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[4]][1]).text)
        txt5.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[4]][2]).text)
        txt5.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[4]][3]).text)
        txt5.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[4]][4]).text)    
        link5=get_youtube_urls(modules_dict[list(modules_dict.keys())[4]])
        entry5=1
        return render_template("modules/module5.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[4]],text=txt5,links=link5)
    else:
        return render_template("modules/module5.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[4]],text=txt5,links=link5)
@app.route("/6")
def module_6():
    
    txt=[]
    txt.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[5]][0]).text)
    txt.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[5]][1]).text)
    txt.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[5]][2]).text)
    txt.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[5]][3]).text)
    txt.append(model.generate_content("Remember, tell me exactly what I ask. Don't give me any additional information. Give me exactly 300 words detailed paragraph  about "+modules_dict[list(modules_dict.keys())[5]][4]).text)    

    link=get_youtube_urls(modules_dict[list(modules_dict.keys())[4]])
    return render_template("modules/module6.html",modules=modules_dict, module=modules_dict[list(modules_dict.keys())[5]],text=txt,links=link)

def generate_prompt(user_input, input_type):
    """
    Generates a prompt based on input type (topic or question) and returns rendered HTML.
    """
    if input_type == "topic":
        # prompt = (
        #     f"Act as a tutor for '{user_input}'. Break down the topic into 5 modules, arranged by difficulty level:\n\n"
        #     "1. **Basics**: Explain foundational concepts or introductory ideas.\n"
        #     "2. **Intermediate Concepts**: Expand on the basics with more detailed explanations and examples.\n"
        #     "3. **Advanced Concepts**: Cover more complex ideas, techniques, or theories related to the topic.\n"
        #     "4. **Practical Applications**: Demonstrate how the topic is applied in real-world scenarios or problems.\n"
        #     "5. **Additional Resources**: Suggest external resources like articles, videos, and books to deepen understanding.\n\n"
        #     "Ensure the explanations are clear and suitable for students at various levels of understanding."
        # )
        return generate_learning_path(user_input)
    elif input_type == "question":
        prompt = (f"Act as a knowledgeable tutor. Answer the following question: '{user_input}'"
                "Please break down your answer into distinct, easy-to-follow steps. Each step should be in its own block for clarity. The structure should be:"
                "1. **Step 1: Restate the Problem** " 
                "Start by restating the question in your own words. Clarify any important details to ensure the question is well understood."
                "2. **Step 2: Identify Key Concepts** " 
                "Outline the key concepts or principles that are necessary to answer this question. If applicable, provide any formulas, theories, or foundational ideas."
                "3. **Step 3: Approach the Solution**  "
                "Walk through the process or methodology needed to solve the problem. Be as clear as possible, breaking down each action in logical order."
                "4. **Step 4: Apply the Concepts** " 
                'Demonstrate how to apply the key concepts to the problem at hand. Use examples, numbers, or explanations to show how the theory is applied.'
               " 5. **Step 5: Summarize the Solution** " 
                "Recap the solution, including key takeaways and any final thoughts. If there are any additional points or caveats, mention them here."
                "'Ensure each step is clear and easy to follow. Use formatting or bullet points for additional clarity. Avoid using overly technical language unless it necessary for the explanation.")
        gemini_response = model.generate_content(prompt)
        response_text = gemini_response.text
        response_text = markdown.markdown(response_text)
        return render_template("response.html", response_text=response_text)
    else:
        # Handle invalid input type
        prompt = "Invalid input type. Please provide either 'topic' or 'question'."

    # Simulated content generation (replace with actual logic if using a model)

    # Render the response in the HTML template
    return render_template("result3.html", response_text=response_text)

# Set up the Generative AI model
genai.configure(api_key="AIzaSyD101zERBMJp-Us2qlNJ2d8RZp8wBvAWME")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/generate", methods=["POST"])
def process_input():
    """
    Processes user input, classifies it as a topic or question,
    and generates a prompt accordingly.
    """
    modules_dict.clear()
    user_input = request.form.get("search_query") # User's input from the form
    input_type = classify_prompt(user_input)    # Classify as topic or question
    return generate_prompt(user_input, input_type)  # Generate appropriate prompt

def render_quiz_template(quiz_q, score=None):
    quiz_html = ""
    for i, (question, options) in enumerate(quiz_q.items()):
        quiz_html += f"<div><p>{i+1}. {question}</p>"
        for option in options:
            quiz_html += f'<label><input type="radio" name="question-{i}" value="{option}"> {option}</label><br>'
        quiz_html += "</div>"
    result = f"<p>Your score: {score}/{len(quiz_q)}</p>" if score is not None else ""
    return f"""
    <form method="POST" action="/q1">
        {quiz_html}
        <button type="submit">Submit</button>
    </form>
    {result}
    """

@app.route("/q1", methods=['GET', 'POST'])
def quiz_module1():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "do exactly what i say don't do any thing extra give me a quiz on topics" + str(modules_dict[list(modules_dict.keys())[0]]) + "it should have exactly 5 questions remember exactly 5 questions and 4 options for each and hear me this is the main part all questions and options you give me must be in the form of a dictionary named as quiz_q all the questions must be the keys and options must be in the form of lists and correct answers must be returned separately in a list named as quiz_a"
    response = model.generate_content(prompt)
    response_text = response.text.replace("\n", " ").replace("     ", "")
    response_text1 = response_text.split("quiz_q = ")[1]
    dic = response_text1.split("quiz_a = ")
    quiz_q = eval(dic[0])
    quiz_a = eval(dic[1].replace("```", ""))
    
    if request.method == 'POST':
        user_answers = request.form
        score = 0
        for i, question in enumerate(quiz_q.keys()):
            if user_answers.get(f"question-{i}") == quiz_a[i]:
                score += 1
        return render_template_string(render_quiz_template(quiz_q, score))
    
    return render_template_string(render_quiz_template(quiz_q))

@app.route("/q2", methods=['GET', 'POST'])
def quiz_module2():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "do exactly what i say don't do any thing extra give me a quiz on topics" + str(modules_dict[list(modules_dict.keys())[1]]) + "it should have exactly 8 questions remember exactly 5 questions and 4 options for each and hear me this is the main part all questions and options you give me must be in the form of a dictionary named as quiz_q all the questions must be the keys and options must be in the form of lists and correct answers must be returned separately in a list named as quiz_a"
    response = model.generate_content(prompt)
    response_text = response.text.replace("\n", " ").replace("     ", "")
    response_text1 = response_text.split("quiz_q = ")[1]
    dic = response_text1.split("quiz_a = ")
    quiz_q = eval(dic[0])
    quiz_a = eval(dic[1].replace("```", ""))
    
    if request.method == 'POST':
        user_answers = request.form
        score = 0
        for i, question in enumerate(quiz_q.keys()):
            if user_answers.get(f"question-{i}") == quiz_a[i]:
                score += 1
        return render_template_string(render_quiz_template(quiz_q, score))
    
    return render_template_string(render_quiz_template(quiz_q))
@app.route("/q3", methods=['GET', 'POST'])
def quiz_module3():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "do exactly what i say don't do any thing extra give me a quiz on topics" + str(modules_dict[list(modules_dict.keys())[2]]) + "it should have exactly 8 questions remember exactly 5 questions and 4 options for each and hear me this is the main part all questions and options you give me must be in the form of a dictionary named as quiz_q all the questions must be the keys and options must be in the form of lists and correct answers must be returned separately in a list named as quiz_a"
    response = model.generate_content(prompt)
    response_text = response.text.replace("\n", " ").replace("     ", "")
    response_text1 = response_text.split("quiz_q = ")[1]
    dic = response_text1.split("quiz_a = ")
    quiz_q = eval(dic[0])
    quiz_a = eval(dic[1].replace("```", ""))
    
    if request.method == 'POST':
        user_answers = request.form
        score = 0
        for i, question in enumerate(quiz_q.keys()):
            if user_answers.get(f"question-{i}") == quiz_a[i]:
                score += 1
        return render_template_string(render_quiz_template(quiz_q, score))
    
    return render_template_string(render_quiz_template(quiz_q))
@app.route("/q4", methods=['GET', 'POST'])
def quiz_module4():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "do exactly what i say don't do any thing extra give me a quiz on topics" + str(modules_dict[list(modules_dict.keys())[3]]) + "it should have exactly 8 questions remember exactly 5 questions and 4 options for each and hear me this is the main part all questions and options you give me must be in the form of a dictionary named as quiz_q all the questions must be the keys and options must be in the form of lists and correct answers must be returned separately in a list named as quiz_a"
    response = model.generate_content(prompt)
    response_text = response.text.replace("\n", " ").replace("     ", "")
    response_text1 = response_text.split("quiz_q = ")[1]
    dic = response_text1.split("quiz_a = ")
    quiz_q = eval(dic[0])
    quiz_a = eval(dic[1].replace("```", ""))
    
    if request.method == 'POST':
        user_answers = request.form
        score = 0
        for i, question in enumerate(quiz_q.keys()):
            if user_answers.get(f"question-{i}") == quiz_a[i]:
                score += 1
        return render_template_string(render_quiz_template(quiz_q, score))
    
    return render_template_string(render_quiz_template(quiz_q))
@app.route("/q5", methods=['GET', 'POST'])
def quiz_module5():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "do exactly what i say don't do any thing extra give me a quiz on topics" + str(modules_dict[list(modules_dict.keys())[4]]) + "it should have exactly 8 questions remember exactly 5 questions and 4 options for each and hear me this is the main part all questions and options you give me must be in the form of a dictionary named as quiz_q all the questions must be the keys and options must be in the form of lists and correct answers must be returned separately in a list named as quiz_a"
    response = model.generate_content(prompt)
    response_text = response.text.replace("\n", " ").replace("     ", "")
    response_text1 = response_text.split("quiz_q = ")[1]
    dic = response_text1.split("quiz_a = ")
    quiz_q = eval(dic[0])
    quiz_a = eval(dic[1].replace("```", ""))
    
    if request.method == 'POST':
        user_answers = request.form
        score = 0
        for i, question in enumerate(quiz_q.keys()):
            if user_answers.get(f"question-{i}") == quiz_a[i]:
                score += 1
        return render_template_string(render_quiz_template(quiz_q, score))
    
    return render_template_string(render_quiz_template(quiz_q))
@app.route("/q6", methods=['GET', 'POST'])
def quiz_module6():
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = "do exactly what i say don't do any thing extra give me a quiz on topics" + str(modules_dict[list(modules_dict.keys())[5]]) + "it should have exactly 8 questions remember exactly 5 questions and 4 options for each and hear me this is the main part all questions and options you give me must be in the form of a dictionary named as quiz_q all the questions must be the keys and options must be in the form of lists and correct answers must be returned separately in a list named as quiz_a"
    response = model.generate_content(prompt)
    response_text = response.text.replace("\n", " ").replace("     ", "")
    response_text1 = response_text.split("quiz_q = ")[1]
    dic = response_text1.split("quiz_a = ")
    quiz_q = eval(dic[0])
    quiz_a = eval(dic[1].replace("```", ""))
    
    if request.method == 'POST':
        user_answers = request.form
        score = 0
        for i, question in enumerate(quiz_q.keys()):
            if user_answers.get(f"question-{i}") == quiz_a[i]:
                score += 1
        return render_template_string(render_quiz_template(quiz_q, score))
    
    return render_template_string(render_quiz_template(quiz_q))

@app.route("/c")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message.strip():
        return jsonify({"error": "Empty message!"}), 400

    # Call the Gemini 1.5 API (or mock response here)
    bot_response = gemini_api_response(user_message)
    return jsonify({"response": bot_response})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
