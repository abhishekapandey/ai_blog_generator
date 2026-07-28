from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent the blog Node
    """

    def __init__(self,llm):
        self.llm = llm

    def title_creation(self, state:BlogState):
        """
        Create the title of the blog post
        """
        if "topic" in state and state["topic"]:
            prompt=""" You are an expert blog content writer. Use Markdown formatting. 
            Generate a blog title for the topic:{topic}. This title should be creative
            and SEO friendly. Give me only 1 title which you think is the best."""

        system_message = prompt.format(topic=state["topic"])
        response = self.llm.invoke(system_message)
        return {"blog":{"title":response.content}}

    def content_generation(self, state:BlogState):
        """
        Generate the content based on the given topic
        """
        if "topic" in state and state["topic"]:
            prompt=""" You are an expert blog content writer. Use Markdown formatting. 
            Generate a detailed blog content with detailed breakdown for the topic:{topic}. This title should be creative
            and SEO friendly """

            system_message = prompt.format(topic=state["topic"])

            response = self.llm.invoke(system_message)

            return {"blog": {"title":state["blog"]["title"], "content": response.content}}

    def translation(self, state:BlogState):
        """
        Translate the content to the specified language.
        """
        
        translation_prompt ="""
        Translate the following content into {current_language}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be apprpriate for {current_language}.

        ORIGINAL CONTENT:
        {blog_content}
        """
        blog_content = state["blog"]["content"]
        messages = [
            HumanMessage(translation_prompt.format(current_language=state["current_language"],blog_content=blog_content))
        ]
    
        translation_content = self.llm.with_structured_output(Blog).invoke(messages)
        return {"blog": {"translated_content": translation_content.content}}

    def route(self, state:BlogState):
        return {"current_language":state["current_language"]}

    def route_decision(self, state:BlogState):
        """
        Route the content to the respective translation function.
        """

        if state["current_language"]== "hindi":
            return "hindi"
        elif state["current_language"]== "french":
            return "french"
        else:
            return state["current_language"]
        

