import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

class ChatbotService:
    """Service to manage chatbot interactions using LangChain and OpenAI."""
    
    def __init__(self):
        """Initialize the chatbot service with OpenAI LLM."""
        self.llm = ChatOpenAI(
            openai_api_key=os.environ.get('OPENAI_API_KEY'),
            model_name="gpt-3.5-turbo",
            temperature=0.7
        )
        
        # System message to define chatbot behavior
        self.system_message = SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant that responds concisely and accurately. "
            "You provide clear answers to questions and helpful suggestions when appropriate."
        )
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            self.system_message,
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])
        
    def create_conversation_chain(self, chat_history=None):
        """Create a conversation chain with memory."""
        # Initialize memory with existing chat history if provided
        memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
        
        if chat_history:
            for message in chat_history:
                if message.is_user:
                    memory.chat_memory.add_user_message(message.content)
                else:
                    memory.chat_memory.add_ai_message(message.content)
        
        # Create the conversation chain
        chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=True,
            memory=memory
        )
        
        return chain
    
    def generate_response(self, user_input, chat_history=None):
        """Generate a response to the user's input."""
        chain = self.create_conversation_chain(chat_history)
        response = chain.predict(input=user_input)
        return response
    
    def generate_chat_title(self, first_message):
        """Generate a title for a new chat based on the first message."""
        title_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                "Create a concise title (5 words or less) that summarizes the following message."
            ),
            HumanMessagePromptTemplate.from_template("{message}")
        ])
        
        title_chain = LLMChain(
            llm=self.llm,
            prompt=title_prompt,
            verbose=False
        )
        
        title = title_chain.predict(message=first_message)
        return title.strip()
