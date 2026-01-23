from typing import Final
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from datetime import datetime
import logging

# Setup logging to see errors
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your actual bot token
TOKEN: Final = "8550870558:AAFwSN5DDgR2VlgF3tHj1RtiSaRxXd3BVrM"
BOT_USERNAME: Final = "@art_rag_bot"

# Load your JSON data
art_data = [
    {"doc_id":"starry_night","chunk_id":"starry_night_0","content":"The Starry Night is an 1889 oil-on-canvas painting by the Dutch post-impressionist painter Vincent van Gogh. Painted from the window of his room at the Saint-Remy-de-Provence asylum, it depicts a dreamlike view of a village under a swirling night sky.","source_url":"https://en.wikipedia.org/wiki/The_Starry_Night"},
    {"doc_id":"starry_night","chunk_id":"starry_night_1","content":"The bold brushwork and vivid contrasts influenced generations of modern artists and remains one of the most recognized paintings in Western art.","source_url":"https://en.wikipedia.org/wiki/The_Starry_Night"},
    {"doc_id":"mona_lisa","chunk_id":"mona_lisa_0","content":"The Mona Lisa is a half-length portrait painting by Italian artist Leonardo da Vinci. Considered an archetypal masterpiece of the Italian Renaissance, it has been described as the best known, most visited, and most parodied work of art in the world.","source_url":"https://en.wikipedia.org/wiki/Mona_Lisa"},
    {"doc_id":"mona_lisa","chunk_id":"mona_lisa_1","content":"The sitter's enigmatic expression and sfumato technique contribute to the painting's enduring fascination.","source_url":"https://en.wikipedia.org/wiki/Mona_Lisa"},
    {"doc_id":"persistence_of_memory","chunk_id":"persistence_of_memory_0","content":"The Persistence of Memory is a 1931 painting by artist Salvador Dali and is one of his most recognizable works. The painting introduced the imagery of soft, melting pocket watches, often interpreted as a symbolic exploration of time and decay.","source_url":"https://en.wikipedia.org/wiki/The_Persistence_of_Memory"},
    {"doc_id":"persistence_of_memory","chunk_id":"persistence_of_memory_1","content":"It became a defining example of surrealism and is housed at the Museum of Modern Art in New York City.","source_url":"https://en.wikipedia.org/wiki/The_Persistence_of_Memory"},
    {"doc_id":"david","chunk_id":"david_0","content":"David is a masterpiece of Renaissance sculpture created in marble between 1501 and 1504 by Italian artist Michelangelo. The 5.17-metre statue represents the Biblical hero David and was originally commissioned for the Florence Cathedral.","source_url":"https://en.wikipedia.org/wiki/David_(Michelangelo)"},
    {"doc_id":"david","chunk_id":"david_1","content":"Celebrated for its anatomical precision and expression of tense anticipation, the sculpture has become a symbol of civic freedom for the city of Florence.","source_url":"https://en.wikipedia.org/wiki/David_(Michelangelo)"}
]

# ArtRAG Response Handler
def handle_art_query(query: str) -> str:
    """
    Simulates a RAG system by searching through art data and generating responses.
    """
    query_lower = query.lower()
    
    # Simple keyword-based search
    matching_chunks = []
    
    # Check for specific art pieces
    art_keywords = {
        "starry night": ["starry", "van gogh", "night sky", "starry night"],
        "mona lisa": ["mona", "lisa", "leonardo", "da vinci", "mona lisa"],
        "persistence of memory": ["persistence", "memory", "dali", "melting", "watches", "persistence of memory"],
        "david": ["david", "michelangelo", "sculpture", "statue"]
    }
    
    # Find relevant chunks
    for item in art_data:
        content_lower = item["content"].lower()
        
        # Check if query contains art piece name
        for art_name, keywords in art_keywords.items():
            if art_name in query_lower or any(keyword in query_lower for keyword in keywords):
                if item["doc_id"] in art_name.replace(" ", "_"):
                    matching_chunks.append(item)
                    break
        
        # Also search by content if no direct match
        if not matching_chunks and any(word in content_lower for word in query_lower.split()):
            matching_chunks.append(item)
    
    # Generate response based on found chunks
    if matching_chunks:
        # Group by artwork
        artworks = {}
        for chunk in matching_chunks[:3]:  # Limit to top 3 chunks
            doc_id = chunk["doc_id"]
            if doc_id not in artworks:
                artworks[doc_id] = []
            artworks[doc_id].append(chunk)
        
        # Build response - FIXED: Use plain text instead of problematic Markdown
        response = ""
        for doc_id, chunks in artworks.items():
            artwork_name = doc_id.replace("_", " ").title()
            response += f"🎨 *{artwork_name}*\n\n"
            
            # Combine relevant content
            combined_content = " ".join([chunk["content"] for chunk in chunks])
            response += f"{combined_content}\n\n"
            
            # Add source without Markdown formatting
            if chunks[0]["source_url"]:
                response += f"📚 Source: {chunks[0]['source_url']}\n\n"
        
        response += "\n_Note: This is a demonstration. In production, connect to your actual RAG pipeline._"
        return response
    
    # If no specific match found, provide general info
    else:
        available_art = ["Starry Night (Vincent van Gogh)", 
                        "Mona Lisa (Leonardo da Vinci)", 
                        "The Persistence of Memory (Salvador Dali)", 
                        "David (Michelangelo)"]
        
        response = "🤔 I couldn't find specific information about your query in my art database.\n\n"
        response += "I have information about these artworks:\n"
        for art in available_art:
            response += f"• {art}\n"
        response += "\nTry asking about one of these artworks or be more specific!"
        return response

# Telegram Bot Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🎨 *Welcome to ArtRAG Bot!*

I can answer questions about famous artworks using my Retrieval-Augmented Generation system.

*Available Commands:*
/start - Start the bot
/help - Get help
/list - List available artworks
/about [artwork] - Get information about specific artwork

*Example Questions:*
• Tell me about Starry Night
• Who painted the Mona Lisa?
• What is The Persistence of Memory about?
• Describe Michelangelo's David

*Try asking me anything about art!*
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 *Help Guide*

*How to use ArtRAG Bot:*
1. Just type your question about any artwork
2. Use /list to see all available artworks
3. Use /about [artwork] for specific information

*Examples:*
• "What is Starry Night?"
• "Tell me about Van Gogh's painting"
• "Who created David sculpture?"

*Available Artworks:*
• Starry Night
• Mona Lisa
• The Persistence of Memory
• David

*Note:* This bot uses a demonstration RAG system. In production, it would connect to a full RAG pipeline with vector search and LLM generation.
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_text = """
📚 *Available Artworks in Database*

1. *The Starry Night*
   - Artist: Vincent van Gogh
   - Year: 1889
   - Type: Oil on canvas

2. *Mona Lisa*
   - Artist: Leonardo da Vinci
   - Period: Italian Renaissance
   - Type: Oil on poplar panel

3. *The Persistence of Memory*
   - Artist: Salvador Dali
   - Year: 1931
   - Movement: Surrealism

4. *David*
   - Artist: Michelangelo
   - Years: 1501-1504
   - Type: Marble sculpture

Ask about any of these artworks for detailed information!
    """
    await update.message.reply_text(list_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please specify an artwork. Example: /about starry night")
        return
    
    query = " ".join(context.args)
    response = handle_art_query(query)
    await update.message.reply_text(response, parse_mode='Markdown')

# Handle regular messages - FIXED VERSION
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message_type: str = update.message.chat.type
        text: str = update.message.text
        
        logger.info(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
        
        if message_type == 'group' or message_type == 'supergroup':
            if BOT_USERNAME in text:
                new_text: str = text.replace(BOT_USERNAME, '').strip()
                if new_text:
                    response: str = handle_art_query(new_text)
                    await update.message.reply_text(response, parse_mode='Markdown')
        else:
            # Private chat
            response: str = handle_art_query(text)
            logger.info(f'Bot response: {response[:100]}...')
            await update.message.reply_text(response, parse_mode='Markdown')
            
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await update.message.reply_text(
            "I encountered an issue while processing your request. Please try again with a different question."
        )

# Error handler - FIXED
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f'Update {update} caused error {context.error}')
    
    # Check if update has message
    if update and update.message:
        try:
            await update.message.reply_text(
                "Sorry, I encountered an error. Please try asking your question again."
            )
        except:
            pass  # If we can't send message, just log it

# Main function
if __name__ == '__main__':
    print('🎨 Starting ArtRAG Bot...')
    
    # Create application
    app = Application.builder().token(TOKEN).build()
    
    # Add command handlers
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('list', list_command))
    app.add_handler(CommandHandler('about', about_command))
    
    # Add message handler
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Add error handler
    app.add_error_handler(error_handler)
    
    # Start polling
    print('🤖 Bot is polling...')
    app.run_polling(poll_interval=3, drop_pending_updates=True)