"""
generate_samples.py - Generate sample resume text files for testing
Run: python generate_samples.py
"""

sample_resumes = {
    "alice_ml_engineer.txt": """
Alice Chen
alice.chen@email.com | +1-555-0101 | linkedin.com/in/alicechen | github.com/alicechen

SUMMARY
Machine Learning Engineer with 4 years of experience building production ML systems.
Passionate about NLP, deep learning, and building scalable AI pipelines.

EXPERIENCE
Senior ML Engineer — TechCorp AI (2022 - Present)
- Built NLP pipelines using BERT and transformers for document classification (94% accuracy)
- Designed and deployed PyTorch models on AWS SageMaker serving 1M+ requests/day
- Led team of 3 engineers to build real-time recommendation system using collaborative filtering
- Reduced model inference latency by 40% through ONNX optimization

ML Engineer — DataStar Inc (2020 - 2022)
- Developed Python-based ETL pipelines using Apache Spark and Airflow
- Built computer vision models using TensorFlow/Keras for defect detection
- Created REST APIs with FastAPI to serve ML models in production
- Implemented CI/CD pipelines with GitHub Actions and Docker

EDUCATION
M.S. Computer Science (Machine Learning) — Stanford University, 2020
B.S. Computer Science — UC Berkeley, 2018

SKILLS
Programming: Python, Java, SQL, Bash
ML/AI: PyTorch, TensorFlow, scikit-learn, transformers, BERT, GPT, XGBoost
Cloud: AWS (SageMaker, EC2, S3), GCP, Docker, Kubernetes
Data: pandas, numpy, Spark, Kafka, Airflow, PostgreSQL, MongoDB
Tools: Git, Jupyter, MLflow, Weights & Biases

PROJECTS
- Open-source NLP toolkit with 500+ GitHub stars
- Kaggle competition: Top 3% in NLP classification challenge
""",

    "bob_software_engineer.txt": """
Bob Martinez
bob.m@email.com | +1-555-0202 | github.com/bobm

SUMMARY
Full-stack Software Engineer with 3 years of experience in web development.
Strong background in React, Node.js, and cloud deployment.

EXPERIENCE
Software Engineer — WebWorks Ltd (2021 - Present)
- Built responsive web applications using React and TypeScript
- Developed RESTful APIs with Node.js and Express
- Managed PostgreSQL and MongoDB databases
- Deployed applications to AWS (EC2, RDS, S3) using Docker

Junior Developer — StartupXYZ (2020 - 2021)
- Contributed to Django-based backend services
- Wrote unit tests and maintained CI/CD pipelines with Jenkins
- Worked in Agile/Scrum environment with 2-week sprints

EDUCATION
B.S. Computer Science — University of Texas, 2020

SKILLS
Programming: JavaScript, TypeScript, Python, HTML, CSS
Frameworks: React, Node.js, Django, Express, Next.js
Databases: PostgreSQL, MongoDB, Redis
Cloud: AWS, Docker, GitHub Actions
Other: Git, Agile, REST API

PROJECTS
- Built a task management web app with real-time collaboration
- Personal portfolio website with 200+ visitors/month
""",

    "carol_data_scientist.txt": """
Carol Williams
carol.w@gmail.com | linkedin.com/in/carolw

OBJECTIVE
Data Scientist with strong statistical background and 2 years of experience.
Looking to apply machine learning skills in a challenging environment.

EXPERIENCE
Data Scientist — Analytics Co (2022 - Present)
- Built predictive models using scikit-learn and XGBoost for customer churn (85% accuracy)
- Performed exploratory data analysis with pandas and matplotlib
- Created dashboards in Tableau for business stakeholders
- Wrote SQL queries for data extraction from PostgreSQL

Data Analyst Intern — Finance Corp (2021 - 2022)
- Analyzed large datasets to identify trends and patterns
- Built automated reports using Python and Excel
- Collaborated with cross-functional teams to present insights

EDUCATION
M.S. Statistics — Columbia University, 2021
B.S. Mathematics — NYU, 2019

SKILLS
Programming: Python, R, SQL
ML: scikit-learn, XGBoost, pandas, numpy, matplotlib, seaborn
Deep Learning: basic TensorFlow, Keras (coursework)
Tools: Tableau, Excel, Jupyter, Git, PostgreSQL

CERTIFICATIONS
- Google Professional Data Analyst (2022)
- AWS Cloud Practitioner (2023)
"""
}

sample_jd = """
SAMPLE JOB DESCRIPTION - Senior Machine Learning Engineer

We are looking for a Senior Machine Learning Engineer to join our AI team.

REQUIREMENTS:
- 3+ years of experience in machine learning or deep learning
- Strong proficiency in Python and PyTorch or TensorFlow
- Experience with NLP, transformers, and BERT-based models
- Hands-on experience deploying ML models to production (AWS, GCP, or Azure)
- Experience with MLOps tools: Docker, Kubernetes, CI/CD pipelines
- Strong understanding of data pipelines (Spark, Kafka, Airflow)
- Excellent problem-solving and communication skills

NICE TO HAVE:
- Experience with large language models (GPT, LLM fine-tuning)
- Contributions to open-source ML projects
- Experience with distributed training

RESPONSIBILITIES:
- Design and implement production-grade ML systems
- Collaborate with data engineers and product teams
- Lead technical discussions and mentor junior engineers
- Stay current with the latest research in ML/AI
"""

if __name__ == "__main__":
    import os
    os.makedirs("sample_resumes", exist_ok=True)

    for filename, content in sample_resumes.items():
        path = os.path.join("sample_resumes", filename)
        with open(path, "w") as f:
            f.write(content.strip())
        print(f"✅ Created: {path}")

    with open("sample_resumes/sample_jd.txt", "w") as f:
        f.write(sample_jd.strip())
    print("✅ Created: sample_resumes/sample_jd.txt")

    print("\n🎉 Sample files ready! Use these for testing the app.")
    print("Paste the JD content into the app and upload resumes as PDFs (or paste text).")
