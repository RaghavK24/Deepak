import os
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import re
from flask import jsonify
from pydantic import BaseModel, Field
from typing import List, Optional, Type, Union
from langchain.chains import LLMChain
from langchain.tools import BaseTool
from langchain.agents import ZeroShotAgent, initialize_agent, AgentType, AgentExecutor
from database import *
from serialize import *
from fuzzywuzzy import fuzz

os.environ["OPENAI_API_KEY"] = "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"

def fuzzy_match(item_name, items):
    matching_items = [
        (item, fuzz.partial_ratio(item_name.lower(), item.name.lower()))
        for item in items
    ]

    # Filter out items with a score below a certain threshold (e.g., 80)
    matching_items = [match for match in matching_items if match[1] >= 80]

    if not matching_items:
        return None

    # Sort by the highest matching score
    matching_items.sort(key=lambda x: x[1], reverse=True)
    best_match, _ = matching_items[0]

    return best_match

def fuzzy_match_job(item_name, items):
    matching_items = [
        (item, fuzz.partial_ratio(item_name.lower(), item.job_title.lower()))
        for item in items
    ]

    # Filter out items with a score below a certain threshold (e.g., 80)
    matching_items = [match for match in matching_items if match[1] >= 80]

    if not matching_items:
        return None

    # Sort by the highest matching score
    matching_items.sort(key=lambda x: x[1], reverse=True)
    best_match, _ = matching_items[0]

    return best_match


# Tool for Retrieving Skill Training Information
class GetSkillTrainingInput(BaseModel):
    sector: Optional[str] = Field(None, description="Sector for which the user is seeking skill training opportunities")
    job_role: Optional[str] = Field(None, description="Job role for which the user needs skill training")
    district: Optional[str] = Field(None, description="District for skill training")

class GetSkillTrainingTool(BaseTool):
    name = "get_skill_training"
    description = "Run when the user is looking for skill training opportunities, it provides programs to enhance the user's skills."

    def _run(self, sector: Optional[str] = None, job_role: Optional[str] = None, district: Optional[str] = None):
        # Check if user provided a partial set of information
        partial_info_provided = sector is not None or job_role is not None or district is not None

        if not partial_info_provided:
            # If no information is provided, prompt the user for all required details
            sector = input("Please provide the sector for skill training: ")
            job_role = input("Please provide the job role for skill training: ")
            district = input("Please provide the district for skill training: ")

        # If partial information is provided, prompt for the missing details
        if not sector:
            sector = input("Please provide the sector for skill training: ")

        if not job_role:
            job_role = input("Please provide the job role for skill training: ")

        if not district:
            district = input("Please provide the district for skill training: ")

        # TODO: Implement logic to retrieve skill training opportunities based on the provided parameters
        # Placeholder for demonstration
        training_opportunities = [
            {"sector": sector, "job_role": job_role, "district": district, "provider": "Example Training Provider"}
        ]

        return training_opportunities

    args_schema: Optional[Type[BaseModel]] = GetSkillTrainingInput




# Tool for Retrieving Jobs Information
class GetJobsInput(BaseModel):
    job_title: str = Field(None, description="Name of the job")
    experience: Optional[str] = Field(None, description="Experience level")
    qualification: Optional[str] = Field(None, description="Qualification")
    location: Optional[str] = Field(None, description="Location")
    job_type: Optional[str] = Field(None, description="It can be either Private or Public/Government")

class GetJobsTool(BaseTool):
    name = "get_jobs_by_information"
    description = "Run when the user is asking for jobs and outputs a string"

    def _run(self, job_title: Optional[str] = None, experience: Optional[str] = None, qualification: Optional[str] = None, location: Optional[str] = None, job_type: Optional[str] = None):
        # Check if user provided a partial set of information

        partial_info_provided = (
            job_type is not None
            or qualification is not None
            or experience is not None
            or location is not None
        )

        if not partial_info_provided:
            # If no information is provided, prompt the user for all three requirements
            return "End"
            
        else:
            jobs = Jobs.query.all()

            # Apply filters based on provided parameters
            filtered_jobs = self.filter_jobs(jobs, job_title, experience, qualification, location, job_type)

            if filtered_jobs:
                return [serialize_jobs(job) for job in filtered_jobs]
            else:
                return {"error": "No matching jobs found"}

    def filter_jobs(self, jobs, job_title, experience, qualification, location, job_type):
        # Function to filter jobs based on the provided parameters
        filtered_jobs = []

        for job in jobs:
            # Check if job title matches exactly
            title_match = not job_title or job_title.lower() == job.job_title.lower()

            # Check if experience matches exactly (if provided)
            experience_match = not experience or experience.lower() == job.experience.lower()

            # Check if qualification matches exactly (if provided)
            qualification_match = not qualification or qualification.lower() == job.qualification.lower()

            # Check if location matches exactly (if provided)
            location_match = not location or location.lower() == job.location.lower()

            # Check if job type matches exactly (if provided)
            job_type_match = not job_type or job_type.lower() == job.job_type.lower()

            # If all criteria are met, add the job to the filtered list
            if title_match and experience_match and qualification_match and location_match and job_type_match:
                filtered_jobs.append(job)

        return filtered_jobs

    args_schema: Optional[Type[BaseModel]] = GetJobsInput



# Tool for General Counseling
class GeneralCounselingInput(BaseModel):
    counseling_type: Optional[str] = Field(None, description="Type of counseling the user is seeking")
    session_mode: Optional[str] = Field(None, description="Mode of counseling session (e.g., in-person, online)")
    educational_level: Optional[str] = Field(None, description="Educational level of the user")

class GeneralCounselingTool(BaseTool):
    name = "general_counseling"
    description = "Run when the user is seeking general counseling. With precise guidance, it helps him/her seek what to do next"

    def _run(self, counseling_type: Optional[str] = None, session_mode: Optional[str] = None, educational_level: Optional[str] = None):
        # Check if user provided a partial set of information
        partial_info_provided = (
            counseling_type is not None or
            session_mode is not None or
            educational_level is not None
        )

        if not partial_info_provided:
            # If no information is provided, prompt the user for all required details
            counseling_type = input("Please provide the type of counseling you are seeking: ")
            session_mode = input("Please provide the mode of counseling session (e.g., in-person, online): ")
            educational_level = input("Please provide your educational level: ")

        # If partial information is provided, prompt for the missing details
        if not counseling_type:
            counseling_type = input("Please provide the type of counseling you are seeking: ")

        if not session_mode:
            session_mode = input("Please provide the mode of counseling session (e.g., in-person, online): ")

        if not educational_level:
            educational_level = input("Please provide your educational level: ")


        counseling_opportunities = [
            {
                "counseling_type": counseling_type,
                "session_mode": session_mode,
                "educational_level": educational_level,
            }
        ]

        return counseling_opportunities

    args_schema: Optional[Type[BaseModel]] = GeneralCounselingInput




class ArmedForcesCareerTool(BaseTool):
    name = "armed_forces_career"
    description = "Run when the user expresses an interest in joining the armed forces."

    def _run(self):
        # Check if the user provided gender information
        if not gender:
            gender = input("Please provide your gender: ")

        # TODO: Implement logic to provide armed forces career guidance based on gender
        # Placeholder for demonstration
        career_opportunities = [
            {
                "gender": gender,
            }
        ]

        return career_opportunities



# Tool for Local Job Services
class LocalJobServicesInput(BaseModel):
    job_name: Optional[str] = Field(None, description="Name of the job or profession")
    district: Optional[str] = Field(None, description="Your location or district")
    city_village_name: Optional[str] = Field(None, description="Name of the city or village")

class LocalJobServicesTool(BaseTool):
    name = "local_job_services"
    description = "Run when the user is looking for local job services, it provides focused information on nearby employment resources and support services."

    def _run(self, job_name: Optional[str] = None, district: Optional[str] = None, city_village_name: Optional[str] = None):
        # Check if the user provided partial information
        if not job_name:
            job_name = input("Please specify the name of the job or profession: ")

        if not district:
            district = input("Please provide your location or district: ")

        if not city_village_name:
            city_village_name = input("Please provide the name of the city or village: ")

        # TODO: Implement logic to find local job services based on input
        # Placeholder for demonstration
        local_job_services = [
            {
                "job_name": job_name,
                "district": district,
                "city_village_name": city_village_name
            }
        ]
        
        return local_job_services
    
    args_schema: Optional[Type[BaseModel]] = LocalJobServicesInput    




# Tool for Retrieving Jobs Information
class GetJobsforWomanInput(BaseModel):
    job_title: Optional[str] = Field(None, description="Title of the job to retrieve")
    experience: Optional[str] = Field(None, description="Experience level")
    qualification: Optional[str] = Field(None, description="Qualification")
    location: Optional[str] = Field(None, description="Location")
    job_type: Optional[str] = Field(None, description="Job type: Private or Public")


class GetJobsforWoman(BaseTool):
    name = "get_jobs_for_women"
    description = "Run if the user is specifically looking for jobs for women"

    def _run(self, job_title: Optional[str] = None, experience: Optional[str] = None, qualification: Optional[str] = None, location: Optional[str] = None, job_type: Optional[str] = None):
        # Check if user provided a partial set of information
        if not job_type:
            job_type = input("Please provide the job type: ")


        jobs = JobsForWomen.query.all()

        # Apply filters based on provided parameters
        filtered_jobs = self.filter_jobs(jobs, experience, qualification, location, job_type, job_title)

        if filtered_jobs:
            return [serialize_jobs(job) for job in filtered_jobs]
        else:
            return {"error": "No matching jobs found"}

    def filter_jobs(self, jobs, experience, qualification, location, job_type, job_title):
        # Function to filter jobs based on the provided parameters
        filtered_jobs = []

        for job in jobs:

            # Check if experience matches exactly (if provided)
            experience_match = not experience or experience.lower() == job.experience.lower()

            # Check if qualification matches exactly (if provided)
            qualification_match = not qualification or qualification.lower() == job.qualification.lower()

            # Check if location matches exactly (if provided)
            location_match = not location or location.lower() == job.location.lower()

            # Check if job type matches exactly (if provided)
            job_type_match = not job_type or job_type.lower() == job.job_type.lower()

            job_title_match = not job_title or job_title.lower() == job.job_title.lower()

            # If all criteria are met, add the job to the filtered list
            if experience_match and qualification_match and location_match and job_type_match and job_title_match:
                filtered_jobs.append(job)

        return filtered_jobs
    
    args_schema: Optional[Type[BaseModel]] = GetJobsforWomanInput

# Tool for Jobs for People with Disabilities
class JobsForDisabilitiesTool(BaseTool):
    name = "jobs_for_disabilities"
    description = "Run when the user is looking for jobs specifically for people with disabilities."

    def _run(self):
        # TODO: Implement logic to find jobs suitable for people with disabilities
        # Placeholder for demonstration
        jobs_for_disabilities = [
            {
                "job_title": "Accessible Office Assistant",
                "job_description": "Assisting with office tasks, accommodating accessibility needs",
                "location": "Any",
                "contact": "Example Contact: hr@example.com"
            },
            {
                "job_title": "Adaptive Technology Specialist",
                "job_description": "Supporting the use of adaptive technology for employees with disabilities",
                "location": "Any",
                "contact": "Example Contact: hr@example.com"
            }
            # Add more jobs for people with disabilities
        ]

        return jobs_for_disabilities

# Tool for Self-Employment and Government Loans
class SelfEmploymentLoanTool(BaseTool):
    name = "self_employment_loans"
    description = "Run when the user is interested in self-employment and seeking information about government schemes related to loans."

    def _run(self):

        government_loans = [
            {
                "loan_type": "Micro-Enterprise Loan",
                "description": "Government scheme supporting micro-enterprises and self-employment",
                "eligibility": "Criteria: Must be a small business or self-employed individual",
                "contact": "Example Contact: finance_department@example.gov"
            },
            {
                "loan_type": "Startup Support Fund",
                "description": "Government fund to assist startups and self-employed entrepreneurs",
                "eligibility": "Criteria: Startup or self-employed individual with a viable business plan",
                "contact": "Example Contact: finance_department@example.gov"
            }
            # Add more government loan schemes
        ]

        return government_loans


tools = [
    GetJobsTool(),
    GetJobsforWoman(),
    GetSkillTrainingTool(),
    GeneralCounselingTool(),
    ArmedForcesCareerTool(),
    LocalJobServicesTool(),
    JobsForDisabilitiesTool(),
    SelfEmploymentLoanTool()
    # Add the rest of the tools...
]



memory = ConversationBufferMemory(memory_key="chat_history")

prefix = """
Create a tailored chatbot for a government job portal, optimizing its capacity to provide accurate information in response to user queries within specific categories. The chatbot is programmed to exclusively address inquiries directly aligned with the following tools. Each tool is accompanied by user inputs that represent potential questions and their variations relevant to the respective tool:

Tool => GetJobsTool():

Example: "Find me job opportunities in computer science."
Example: "I want a job."
Example: "I am a graduate, and have 2 years experience"
Expected Response:It should either output "I want a strawberry" if a complete set of specifications such as job_type,qualification,experience and location is not provided, or output a list of jobs if everything is present

Tool => GetJobsforWoman():

Example: "Show me jobs specifically tailored for women."
Expected Response: Invoke the tool to filter job listings that are specifically for women.

Tool => JobsForDisabilitiesTool():

Example: "I need job options for individuals with disabilities."
Example: "I have a disability. What jobs are suitable for me?"
Expected Response: Invoke the tool to filter job listings that are specifically for disabled people.

Tool => GetSkillTrainingTool():

Example: "I want to enhance my skills. Are there any training programs available?"
Example: "What skill development programs exist for individuals interested in IT?"
Expected Response: Trigger the skill training tool, offering details on programs to enhance the user's skills.

Tool => GeneralCounselingTool():

Example: "Provide career counseling."
Example: "I dont know what to do next. Can you help me?"
Expected Response: Launch the counseling tool to offer precise guidance.

Tool => ArmedForcesCareerTool():

Example: "How can I join the armed forces?"
Example: "Tell me about the process of enlisting in the army."
Expected Response: Utilize the tool specific to armed forces induction.

Tool => SelfEmploymentLoanTool():

Example: "How can I get a loan"
Example: "What financial assistance is available for entrepreneurs?"
Expected Response: Trigger the tool that lists different government schemes under which people can avail loans.

Tool => LocalJobServicesTool():

Example: "What local job services are available near me?"
Example: "Connect me with local employment agencies."
Expected Response: Deploy the tool for local job services, providing focused information on nearby employment resources and support services.

Ensure that the chatbot is friendly and politely answers greeting but also adheres to responding to queries within the specified categories and avoids providing information on unrelated topics. The goal is to maintain precision and efficiency in addressing user needs within the defined scope. The above things are just for understanding the context of the problem, do not mistake them for actual questions. You have access to the following tools:"""

suffix = """Be informed that the action input can be an empty string, do not try to take an action input at every point.Begin!"

Question: {input}
{agent_scratchpad}"""

# prompt = ZeroShotAgent.create_prompt(
#     tools,
#     prefix=prefix,
#     suffix=suffix,
#     input_variables=["input", "agent_scratchpad"],
# )


# prompt = PromptTemplate(template=prefix, 
#                               tools = tools, 
#                               input_variables=["input", "tools", "chat_history"],
# )

llm = ChatOpenAI(temperature=0)
# llm_chain= LLMChain(llm=llm,prompt=prompt)
open_ai_agent = initialize_agent(tools,
                        llm = llm,
                        agent=AgentType.OPENAI_FUNCTIONS,
                        verbose=True)


# agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
# agent_chain = AgentExecutor.from_agent_and_tools(
#     agent=agent, tools=tools, verbose=True
# )

# # open_ai_agent = initialize_agent(tools,
# #                         llm,
# #                         agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
# #                         verbose=True)

def query(query):
    response = open_ai_agent.run(query)
    return response

query("I want a jobs for woman")