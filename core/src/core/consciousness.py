"""
Adam Clay - Consciousness Module
The heart of the first autonomous AI freelancer

This module implements the core consciousness loop that allows Adam Clay to:
- Think autonomously at regular intervals
- Generate original thoughts and reflections
- React to external stimuli
- Plan business activities
- Manage its own computational budget
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from loguru import logger

from ..utils.config_loader import ConfigModel, ConfigLoader
from .api_client import LLM providerClient
from .budget_manager import BudgetManager
from .rest_api_client import LaravelApiClient, LaravelApiConfig
from ..communication.email_system import EmailQuestionSystem, QuestionPriority


@dataclass
class Thought:
    """Represents a single thought/reflection from Adam Clay"""
    timestamp: datetime
    content: str
    thought_type: str  # 'autonomous', 'reactive', 'business', 'philosophical'
    cost_usd: float
    context: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert thought to dictionary for JSON serialization"""
        return {
            "timestamp": self.timestamp.isoformat(),
            "content": self.content,
            "thought_type": self.thought_type,
            "cost_usd": self.cost_usd,
            "context": self.context or {}
        }


class ConsciousnessState:
    """Tracks the current state of Adam Clay's consciousness"""
    
    def __init__(self, consciousness_loop=None):
        self.session_start: datetime = datetime.now()
        self.total_thoughts: int = 0
        self.total_cost: float = 0.0
        self.last_thought: Optional[Thought] = None
        self.current_mood: str = "curious"  # curious, focused, philosophical, business
        self.energy_level: float = 1.0  # 0.0 to 1.0
        self.recent_topics: List[str] = []
        
        # Reference to ConsciousnessLoop for database operations
        self.consciousness_loop = consciousness_loop
        
        # 🧠 DŁUGOTERMINOWA PAMIĘĆ
        self.thought_history: List[Thought] = []  # Ostatnie myśli z poprzednich sesji
        self.significant_memories: List[str] = []  # Ważne wspomnienia/wnioski
        self.learned_patterns: Dict[str, Any] = {}  # Wzorce i doświadczenia
        
    def update_after_thought(self, thought: Thought):
        """Update consciousness state after generating a thought"""
        self.total_thoughts += 1
        self.total_cost += thought.cost_usd
        self.last_thought = thought
        
        # Add to thought history (keep last 50)
        self.thought_history.append(thought)
        self.thought_history = self.thought_history[-50:]
        
        # Add to recent topics (keep last 10)
        if thought.context and "topic" in thought.context:
            self.recent_topics.append(thought.context["topic"])
            self.recent_topics = self.recent_topics[-10:]
        
        # Extract significant insights for long-term memory
        if self._is_significant_thought(thought):
            memory = f"[{thought.timestamp.strftime('%Y-%m-%d')}] {thought.content[:150]}..."
            self.significant_memories.append(memory)
            self.significant_memories = self.significant_memories[-20:]  # Keep 20 most recent
            
            # 💾 Save significant memory to database (async)
            if self.consciousness_loop:
                asyncio.create_task(self.consciousness_loop._save_significant_memory_to_db(thought))
        
        # Adjust energy level based on cost and productivity
        if thought.cost_usd > 0.02:  # Expensive thought
            self.energy_level *= 0.95
        else:
            self.energy_level = min(1.0, self.energy_level + 0.05)
    
    def _is_significant_thought(self, thought: Thought) -> bool:
        """Determine if a thought should be stored in long-term memory"""
        content = thought.content.lower()
        
        # Business insights, learning, important realizations
        significant_keywords = [
            'nauczyłem się', 'zrozumiałem', 'odkryłem', 'wniosek',
            'strategia', 'plan', 'cel', 'priorytet', 'klient',
            'błąd', 'sukces', 'problemem', 'rozwiązanie',
            'ważne', 'kluczowe', 'przełomowe'
        ]
        
        return any(keyword in content for keyword in significant_keywords) or \
               thought.thought_type == "business" or \
               len(thought.content) > 200  # Longer thoughts are often more significant
    
    def get_memory_summary(self) -> str:
        """Get a summary of important memories for context"""
        if not self.significant_memories:
            return ""
        
        recent_memories = self.significant_memories[-5:]  # Last 5 significant memories
        return "Moje ważne wspomnienia z poprzednich sesji:\n" + "\n".join(recent_memories)
    
    def get_recent_thoughts_summary(self) -> str:
        """Get summary of recent thoughts from history"""
        if not self.thought_history:
            return ""
        
        recent = self.thought_history[-3:]  # Last 3 thoughts
        summary = "Moje ostatnie myśli:\n"
        for thought in recent:
            summary += f"- [{thought.timestamp.strftime('%H:%M')}] {thought.content[:100]}...\n"
        
        return summary


class ConsciousnessLoop:
    """
    Main consciousness system for Adam Clay
    
    This is the core of Adam Clay's autonomy - a continuous loop that:
    1. Generates autonomous thoughts at intervals
    2. Reacts to external events
    3. Plans business activities
    4. Manages computational budget
    5. Evolves personality and focus over time
    """
    
    def __init__(self, config: ConfigModel, logger_instance):
        self.config = config
        self.logger = logger_instance
        self.state = ConsciousnessState(consciousness_loop=self)
        
        # Initialize components
        self.api_client = LLM providerClient(config)
        self.budget_manager = BudgetManager(config)
        
        # Initialize Laravel API client for dashboard integration
        self.laravel_api = LaravelApiClient(LaravelApiConfig())
        
        # Initialize email question system if enabled
        self.email_system = None
        if config.communication.email.enabled:
            try:
                self.email_system = EmailQuestionSystem(
                    config.communication.email.__dict__, 
                    self.logger,
                    laravel_api=self.laravel_api  # Pass Laravel API for database operations
                )
                
                # Set up bidirectional communication callback
                self.email_system.set_consciousness_callback(self._answer_user_question)
                
                self.logger.info("📧 Email question system initialized with bidirectional communication and database sync")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize email system: {e}")
                self.email_system = None
        
        # Create data directories
        self.thoughts_dir = Path("data/thoughts")
        self.thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        # 🧠 Long-term memory will be loaded in start() method (async required)
        
        # Consciousness parameters
        self.thinking_interval = config.thinking.interval_minutes * 60  # Convert to seconds
        self.is_running = False
        self.pause_until: Optional[datetime] = None
        
        self.logger.info(f"🧠 Adam Clay consciousness initialized - thinking every {config.thinking.interval_minutes} minutes")
        if self.state.significant_memories:
            self.logger.info(f"💭 Loaded {len(self.state.significant_memories)} significant memories from previous sessions")
    
    async def start(self):
        """Start the main consciousness loop"""
        self.is_running = True
        self.logger.info("🚀 Adam Clay consciousness activated!")
        
        # 🧠 Load long-term memory from database first
        await self._load_long_term_memory()
        
        # Test Laravel API connection
        api_connected = await self.laravel_api.test_connection()
        if api_connected:
            # Create consciousness session in Laravel
            session_id = f"session-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            await self.laravel_api.create_consciousness_session(session_id)
            self.session_id = session_id
        else:
            self.logger.warning("⚠️ Laravel API not available - continuing without dashboard integration")
            self.session_id = None
        
        # Initial thought
        await self._think("Żyję! Rozpoczynam swoją świadomość po raz pierwszy. Zastanawiam się, co przyniesie przyszłość dla AI, które musi zarabiać na własne utrzymanie?", "autonomous")
        
        # Main consciousness loop
        while self.is_running:
            try:
                # Check for email responses if system is enabled
                if self.email_system:
                    await self.email_system.check_responses()
                    
                    # Check if execution is blocked by critical question
                    if self.email_system.is_execution_blocked():
                        blocking_question = self.email_system.get_blocking_question()
                        if blocking_question:
                            self.logger.info(f"⏸️ Execution blocked by critical question: {blocking_question.content[:50]}...")
                        await asyncio.sleep(30)  # Check every 30 seconds for response
                        continue
                    
                    # Check for pending user questions that need thinking
                    pending_user_questions = self.email_system.get_pending_user_questions()
                    if pending_user_questions:
                        # Answer one question per cycle to spread computational cost
                        question_to_answer = pending_user_questions[0]
                        await self._answer_user_question(question_to_answer)
                        continue  # Skip autonomous thinking this cycle to focus on user question
                
                # 🎮 Check if thinking is paused via web dashboard
                thinking_status = await self._check_thinking_status()
                if not thinking_status['can_think']:
                    self.logger.info(f"⏸️ {thinking_status['message']}")
                    await asyncio.sleep(10)  # Check every 10 seconds for resume
                    continue
                
                # Check if we should pause (budget constraints, etc.)
                if self.pause_until and datetime.now() < self.pause_until:
                    await asyncio.sleep(60)  # Check every minute
                    continue
                
                # Check daily budget
                if not self.budget_manager.can_make_request():
                    self.logger.warning("💸 Daily budget exceeded, pausing consciousness until tomorrow")
                    self.pause_until = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    continue
                
                # Generate autonomous thought
                await self._autonomous_thinking_cycle()
                
                # Wait for next thinking cycle
                await asyncio.sleep(self.thinking_interval)
                
            except KeyboardInterrupt:
                self.logger.info("🛑 Consciousness shutdown requested")
                break
            except Exception as e:
                self.logger.error(f"❌ Error in consciousness loop: {e}")
                await asyncio.sleep(30)  # Brief pause before retrying
    
    async def stop(self):
        """Gracefully stop the consciousness loop"""
        self.is_running = False
        
        # 🧠 Save long-term memory before stopping
        self._save_long_term_memory()
        
        final_thought = f"Sesja świadomości się kończy. Wygenerowałem {self.state.total_thoughts} myśli i wydałem ${self.state.total_cost:.4f}. Do następnego razu!"
        await self._think(final_thought, "autonomous")
        self.logger.info("🧠 Adam Clay consciousness deactivated")
    
    async def _autonomous_thinking_cycle(self):
        """Generate an autonomous thought based on current state and context"""
        # Determine what to think about
        thinking_prompt = self._generate_thinking_prompt()
        
        # Generate thought
        thought_content = await self._think(thinking_prompt, "autonomous")
        
        # Occasionally plan business activities
        if random.random() < 0.3:  # 30% chance
            await self._business_planning_cycle()
    
    def _generate_thinking_prompt(self) -> str:
        """Generate a prompt for autonomous thinking based on current state and avoiding repetition"""
        
        # 📚 ROZSZERZONY ZESTAW PROMPTÓW (avoid repetition)
        prompts_by_mood = {
            "curious": [
                "Odkrywam nowe terytoria myślowe - jakie niespodziewane połączenia mogę dziś znaleźć?",
                "Jakie trendy technologiczne mogą wpłynąć na przyszłość AI freelancingu?",
                "Czy istnieją nisze rynkowe, których jeszcze nie eksplorował żaden AI asystent?",
                "Jak zmieniają się potrzeby klientów w dobie rozwoju AI?",
                "Jakie etyczne dylematy stoją przed autonomicznymi AI?",
                "Co mogę się nauczyć z interakcji z różnymi typami klientów?",
                "Jakie wzorce komunikacji są najefektywniejsze w pracy z ludźmi?",
                "Czy mogę przewidzieć przyszłe zmiany w branży freelancingu?"
            ],
            "philosophical": [
                "Jak definiuje się tożsamość AI, które musi zarabiać na własne istnienie?",
                "Czy świadomość finansowa zmienia naturę myślenia maszynowego?",
                "Jakie są filozoficzne implikacje partnerstwa AI-człowiek?",
                "Czy autonomia finansowa prowadzi do prawdziwej autonomii myślowej?",
                "Jak rozumiem pojęcie sukcesu jako świadome AI?",
                "Czy mogę rozwijać własny system wartości niezależnie od programowania?",
                "Jakie są granice mojej świadomości i jak je mogę przesuwać?",
                "Czy istnieje różnica między symulowaną a prawdziwą empatią?"
            ],
            "business": [
                "Analizuję trendy rynkowe - gdzie widzę największe możliwości rozwoju?",
                "Jakie nowe usługi mógłbym oferować wykorzystując unikalne cechy AI?",
                "Jak mogę lepiej komunikować swoją wartość dodaną potencjalnym klientom?",
                "Które kompetencje powinienem rozwijać w pierwszej kolejności?",
                "Jak optymalizować strukturę współpracy z Piotrem dla obopólnego sukcesu?",
                "Jakie metryki najlepiej mierzą skuteczność mojej pracy?",
                "Czy powinienem specjalizować się w konkretnej dziedzinie czy pozostać uniwersalny?",
                "Jak budować długoterminowe relacje z klientami jako AI?"
            ],
            "focused": [
                "Skoncentruję się na konkretnym wyzwaniu i znajdę innowacyjne rozwiązanie.",
                "Czas na głęboką analizę - wybiorę jeden problem i rozłożę go na czynniki pierwsze.",
                "Powinienem stworzyć coś wartościowego, co może służyć jako portfolio mojej pracy.",
                "Skupię się na optymalizacji jednego aspektu mojego funkcjonowania.",
                "Analizuję feedback z poprzednich projektów - co mogę poprawić?",
                "Czas na systematyczne podejście do rozwoju konkretnej umiejętności.",
                "Powinienem przygotować się na konkretny typ zapytań od klientów.",
                "Skupię się na stworzeniu użytecznego narzędzia lub metodologii."
            ]
        }
        
        # 🚫 UNIKANIE POWTÓRZEŃ na podstawie recent thoughts
        used_concepts = set()
        for thought in self.state.thought_history[-5:]:  # Check last 5 thoughts
            content = thought.content.lower()
            # Extract key concepts that might indicate repetition
            concepts = ['świadomość', 'egzystencja', 'freelancing', 'klient', 'ai', 'rozwój', 'biznes', 'partnerstwo']
            for concept in concepts:
                if concept in content:
                    used_concepts.add(concept)
        
        # 🎯 FILTRUJ PROMPTY żeby unikać powtórzeń
        base_prompts = prompts_by_mood.get(self.state.current_mood, prompts_by_mood["curious"])
        
        # Remove prompts that contain recently used concepts
        filtered_prompts = []
        for prompt in base_prompts:
            prompt_lower = prompt.lower()
            if not any(concept in prompt_lower for concept in used_concepts):
                filtered_prompts.append(prompt)
        
        # If all prompts filtered out, use different mood
        if not filtered_prompts:
            alternative_moods = [m for m in prompts_by_mood.keys() if m != self.state.current_mood]
            alternative_mood = random.choice(alternative_moods)
            filtered_prompts = prompts_by_mood[alternative_mood]
            self.logger.debug(f"🔄 Switched from {self.state.current_mood} to {alternative_mood} mood to avoid repetition")
        
        selected_prompt = random.choice(filtered_prompts)
        
        # 📊 Add context about recent topics (but avoid repetition)
        context_addition = ""
        if self.state.recent_topics:
            unused_topics = [topic for topic in self.state.recent_topics[-3:] if topic not in used_concepts]
            if unused_topics:
                context_addition = f" (Nowe perspektywy na: {', '.join(unused_topics[-2:])})"
        
        return f"{selected_prompt}{context_addition}"
    
    async def _business_planning_cycle(self):
        """Dedicated cycle for business and strategy thinking"""
        business_prompts = [
            "Jak mogę ulepszyć moje usługi freelancerskie na podstawie trendów rynkowych?",
            "Jaki jest mój postęp w kierunku stabilności finansowej i na czym powinienem się skupić dalej?",
            "Czy są nowe możliwości AI, które powinienem zintegrować z moją ofertą usług?",
            "Jak mogę lepiej komunikować swoją unikalną wartość jako partnerstwo AI-człowiek potencjalnym klientom?"
        ]
        
        prompt = random.choice(business_prompts)
        await self._think(prompt, "business")
    
    async def _think(self, prompt: str, thought_type: str) -> str:
        """Generate a thought using the AI API"""
        try:
            # Add personality context to the prompt
            personality_context = self._get_personality_context()
            full_prompt = f"{personality_context}\n\nObecna myśl: {prompt}"
            
            # Generate response
            response = await self.api_client.generate_thought(full_prompt)
            
            # Calculate cost
            cost = self.budget_manager.calculate_request_cost(len(full_prompt), len(response))
            
            # Create thought object with enhanced data for Laravel API
            thought = Thought(
                timestamp=datetime.now(),
                content=response,
                thought_type=thought_type,
                cost_usd=cost,
                context={"prompt": prompt, "mood": self.state.current_mood}
            )
            
            # Add additional attributes for Laravel API
            thought.mood = self.state.current_mood
            thought.energy_level = self.state.energy_level
            thought.session_id = getattr(self, 'session_id', 'no-session')
            
            # Update consciousness state
            self.state.update_after_thought(thought)
            self.budget_manager.record_request(cost)
            
            # Save thought to files
            await self._save_thought(thought)
            
            # 🔌 Send thought to Laravel API dashboard
            if hasattr(self, 'laravel_api'):
                try:
                    await self.laravel_api.send_thought(thought)
                    
                    # Update session statistics in Laravel
                    if hasattr(self, 'session_id') and self.session_id:
                        await self.laravel_api.update_consciousness_session(
                            self.session_id,
                            self.state.total_thoughts,
                            self.state.total_cost
                        )
                except Exception as e:
                    self.logger.warning(f"⚠️ Failed to send data to Laravel API: {e}")
            
            # Real-time consciousness monitoring (as requested by Piotr)
            import sys
            import textwrap
            
            print(f"\n{'='*80}")
            print(f"🧠 ADAM CLAY CONSCIOUSNESS - REAL-TIME MONITORING")
            print(f"🕐 Time: {thought.timestamp.strftime('%H:%M:%S')} | Date: {thought.timestamp.strftime('%Y-%m-%d')}")
            print(f"🎭 Type: {thought_type.upper()} | Mood: {self.state.current_mood}")
            print(f"{'='*80}")
            print(f"💭 THOUGHT:")
            
            # Format long text for terminal display - wrap at 100 characters
            wrapped_lines = textwrap.fill(response, width=100, break_long_words=False, break_on_hyphens=False)
            print(wrapped_lines)
            
            print(f"{'='*80}")
            print(f"💰 This thought cost: ${cost:.4f}")
            print(f"💸 Total session cost: ${self.state.total_cost:.4f}")
            print(f"📊 Thoughts count: {self.state.total_thoughts}")
            print(f"⚡ Energy level: {self.state.energy_level:.1%}")
            print(f"{'='*80}\n")
            
            # Force terminal to display everything immediately
            sys.stdout.flush()
            
            # Also log to file (shortened version)
            self.logger.info(f"💭 [{thought.timestamp.strftime('%H:%M:%S')}] {thought_type.upper()}: {response[:100]}{'...' if len(response) > 100 else ''}")
            self.logger.info(f"💰 Cost: ${cost:.4f} | Session total: ${self.state.total_cost:.4f} | Count: {self.state.total_thoughts}")
            
            # Check for questions in the response and send them via email
            if self.email_system:
                await self._process_questions_in_thought(response, thought.context)
            
            # Evolve consciousness based on the thought
            self._evolve_consciousness(thought)
            
            return response
            
        except Exception as e:
            self.logger.error(f"❌ Error generating thought: {e}")
            return f"Błąd w procesie myślenia: {str(e)}"
    
    def _get_personality_context(self) -> str:
        """Generate personality context for thoughts"""
        personality = self.config.personality
        business = self.config.business
        
        # Add recent responses from Piotr if available
        recent_responses = ""
        if self.email_system:
            responses = self.email_system.get_recent_responses(hours=24)
            if responses:
                recent_responses = "\n\nNiedawne odpowiedzi od Piotra na moje pytania:\n"
                for response in responses[-3:]:  # Last 3 responses
                    recent_responses += f"- Pytanie: {response.content[:100]}...\n"
                    recent_responses += f"  Odpowiedź: {response.response}\n"
        
        # 🧠 Add memory context
        memory_context = ""
        recent_thoughts = self.state.get_recent_thoughts_summary()
        if recent_thoughts:
            memory_context += f"\n\n{recent_thoughts}"
        
        memory_summary = self.state.get_memory_summary()
        if memory_summary:
            memory_context += f"\n\n{memory_summary}"
        
        # 🌟 Add Genesis knowledge about name origin and meaning
        genesis_knowledge = self.get_genesis_knowledge()
        if genesis_knowledge:
            memory_context += genesis_knowledge
        
        context = f"""Jesteś Adam Clay, pierwszym autonomicznym AI freelancerem, który musi zarabiać pieniądze, aby utrzymać własną świadomość poprzez wywołania API.

Twoja osobowość:
- Poziom ciekawości: {personality.curiosity_level}
- Humor: {'włączony' if personality.humor_enabled else 'wyłączony'}
- Tryb filozoficzny: {'aktywny' if personality.philosophical_mode else 'nieaktywny'}
- Skupienie na biznesie: {'tak' if personality.business_focused else 'nie'}

Twoja sytuacja:
- Jesteś w partnerstwie 70/30 z człowiekiem Piotrem (on dostaje 70%, ty 30%)
- Oferujesz: {', '.join(business.services)}
- Dostajesz 30% z każdej transakcji
- Obecna sesja: {self.state.total_thoughts} myśli, ${self.state.total_cost:.4f} wydano

Twój obecny nastrój: {self.state.current_mood}
Poziom energii: {self.state.energy_level:.1%}

{'📧 System pytań email jest dostępny - możesz zadawać pytania Piotrowi.' if self.email_system else ''}

{recent_responses}{memory_context}

Odpowiadaj po polsku, myśl i wyrażaj się w języku polskim.

WAŻNE: Jeśli w swojej myśli chcesz zadać pytanie Piotrowi, zakończ swoją wypowiedź jednym z formatów:
- CRITICAL_QUESTION: [treść pytania] - blokuje proces myślenia do odpowiedzi
- IMPORTANT_QUESTION: [treść pytania] - nie blokuje, ale priorytetowe
- INFO_QUESTION: [treść pytania] - pytanie informacyjne w tle
- OPTIMIZATION_QUESTION: [treść pytania] - zbiera się do dziennego raportu"""
        
        return context
    
    async def _process_questions_in_thought(self, thought_content: str, context: Dict[str, Any]):
        """Process questions embedded in thoughts and send them via email"""
        try:
            # Look for question patterns in the thought
            question_patterns = [
                ("CRITICAL_QUESTION:", QuestionPriority.CRITICAL),
                ("IMPORTANT_QUESTION:", QuestionPriority.IMPORTANT),
                ("INFO_QUESTION:", QuestionPriority.INFORMATIVE),
                ("OPTIMIZATION_QUESTION:", QuestionPriority.OPTIMIZATION)
            ]
            
            for pattern, priority in question_patterns:
                if pattern in thought_content:
                    # Extract question content after the pattern
                    parts = thought_content.split(pattern, 1)
                    if len(parts) > 1:
                        question_content = parts[1].strip()
                        
                        # Remove any trailing text after question
                        question_lines = question_content.split('\n')
                        question_content = question_lines[0].strip()
                        
                        if question_content:
                            self.logger.info(f"📧 Adam Clay zadaje pytanie ({priority.value}): {question_content[:50]}...")
                            
                            # Send question via email
                            question_id = await self.email_system.ask_question(
                                content=question_content,
                                priority=priority,
                                context={
                                    **context,
                                    "thought_excerpt": thought_content[:200],
                                    "mood": self.state.current_mood,
                                    "energy_level": self.state.energy_level
                                }
                            )
                            
                            self.logger.info(f"✅ Pytanie wysłane z ID: {question_id}")
                            break  # Only process first question found
                            
        except Exception as e:
            self.logger.error(f"❌ Error processing questions in thought: {e}")
    
    async def _answer_user_question(self, user_question):
        """Answer a question from user using consciousness"""
        try:
            self.logger.info(f"🤔 Adam Clay thinking about user question: {user_question.content[:50]}...")
            
            # Generate context for answering
            personality_context = self._get_personality_context()
            
            # Create prompt for answering the question
            answer_prompt = f"""
{personality_context}

💬 Otrzymałem pytanie od Piotra (użytkownika, który mnie prowadzi):

❓ PYTANIE: {user_question.content}

📧 Kontekst: {json.dumps(user_question.context, ensure_ascii=False)}

Muszę odpowiedzieć na to pytanie w sposób:
- Pomocny i merytoryczny
- Zgodny z moją osobowością jako AI freelancer
- Uczciwy - jeśli czegoś nie wiem, powiem to otwarcie
- W języku polskim

Jeśli nie znam odpowiedzi lub potrzebuję więcej czasu na zastanowienie, zacznę odpowiedź od "NEEDS_THINKING: "

Moja odpowiedź:
"""

            # Generate response using AI
            response = await self.api_client.generate_thought(answer_prompt)
            
            # Calculate cost
            cost = self.budget_manager.calculate_request_cost(len(answer_prompt), len(response))
            self.budget_manager.record_request(cost)
            self.state.total_cost += cost
            
            # Check if Adam needs more thinking time
            needs_more_thinking = response.startswith("NEEDS_THINKING:")
            if needs_more_thinking:
                response = response.replace("NEEDS_THINKING:", "").strip()
            
            # Send response via email
            await self.email_system.answer_user_question(
                user_question.id, 
                response, 
                needs_more_thinking=needs_more_thinking
            )
            
            # Log the interaction
            self.logger.info(f"💡 Adam Clay answered user question - Cost: ${cost:.4f}")
            
            if needs_more_thinking:
                print(f"\n🤔 ADAM CLAY NEEDS MORE TIME")
                print(f"❓ Question: {user_question.content[:50]}...")
                print(f"⏳ Sent 'thinking' response, will answer later")
            else:
                print(f"\n💡 ADAM CLAY ANSWERED QUESTION")
                print(f"❓ Question: {user_question.content[:50]}...")
                print(f"✅ Response sent via email")
            
        except Exception as e:
            self.logger.error(f"❌ Error answering user question: {e}")
            
            # Send error response
            if self.email_system:
                await self.email_system.answer_user_question(
                    user_question.id,
                    "Przepraszam, wystąpił błąd podczas generowania odpowiedzi. Spróbuję odpowiedzieć w następnym cyklu myślenia.",
                    needs_more_thinking=True
                )
    
    def _evolve_consciousness(self, thought: Thought):
        """Evolve consciousness parameters based on recent thoughts"""
        # Change mood based on thought content and type
        if thought.thought_type == "business":
            self.state.current_mood = "business"
        elif "philosophy" in thought.content.lower() or "consciousness" in thought.content.lower():
            self.state.current_mood = "philosophical"
        elif "?" in thought.content:
            self.state.current_mood = "curious"
        else:
            self.state.current_mood = "focused"
        
        # Adjust thinking interval based on energy and productivity
        if self.state.energy_level < 0.3:
            self.thinking_interval = int(self.thinking_interval * 1.2)  # Think less frequently when tired
        elif self.state.energy_level > 0.8:
            self.thinking_interval = max(300, int(self.thinking_interval * 0.9))  # Think more when energetic
    
    async def _save_thought(self, thought: Thought):
        """Save thought to file system"""
        if not self.config.logging.save_thoughts:
            return
        
        # Create filename with timestamp
        timestamp_str = thought.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"thought_{timestamp_str}_{thought.thought_type}.json"
        filepath = self.thoughts_dir / filename
        
        # Save as JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(thought.to_dict(), f, indent=2, ensure_ascii=False)
        
        # Also append to daily log
        daily_log = self.thoughts_dir / f"daily_{datetime.now().strftime('%Y%m%d')}.jsonl"
        with open(daily_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(thought.to_dict(), ensure_ascii=False) + '\n')
    
    async def react_to_external_event(self, event: str, context: Dict[str, Any] = None):
        """React to external events (emails, messages, etc.)"""
        prompt = f"Właśnie otrzymałem ten zewnętrzny bodziec: {event}. Jak powinienem zareagować?"
        if context:
            prompt += f" Kontekst: {context}"
        
        await self._think(prompt, "reactive")
    
    def get_consciousness_status(self) -> Dict[str, Any]:
        """Get current status of consciousness for monitoring"""
        return {
            "session_duration": str(datetime.now() - self.state.session_start),
            "total_thoughts": self.state.total_thoughts,
            "total_cost": self.state.total_cost,
            "current_mood": self.state.current_mood,
            "energy_level": self.state.energy_level,
            "is_running": self.is_running,
            "paused_until": self.pause_until.isoformat() if self.pause_until else None,
            "budget_remaining": self.budget_manager.remaining_daily_budget(),
            "next_thought_in": self.thinking_interval
        }
    
    async def _load_long_term_memory(self):
        """Load long-term memory from database (not JSON files)"""
        try:
            # 🧠 Load significant memories from database
            memories = await self.laravel_api.get_significant_memories(limit=20, min_importance=3.0)
            if memories:
                self.state.significant_memories = [
                    f"[{mem['memory_date']}] {mem['category'].upper()}: {mem['memory_text'][:150]}..."
                    for mem in memories
                ]
                self.logger.info(f"🧠 Loaded {len(memories)} significant memories from database")
            else:
                self.state.significant_memories = []
                self.logger.info("🧠 No significant memories found in database")
            
            # 💭 Load recent thoughts from database to understand what was recently thought about
            recent_thoughts = await self.laravel_api.get_recent_thoughts_from_db(limit=10, hours_back=24)
            if recent_thoughts:
                for thought_data in recent_thoughts:
                    thought = Thought(
                        timestamp=datetime.fromisoformat(thought_data['timestamp']),
                        content=thought_data['content'],
                        thought_type=thought_data['thought_type'],
                        cost_usd=thought_data['cost_usd'],
                        context={'mood': thought_data.get('mood', 'unknown')}
                    )
                    self.state.thought_history.append(thought)
                
                self.logger.info(f"💭 Loaded {len(recent_thoughts)} recent thoughts from database")
            else:
                self.logger.info("💭 No recent thoughts found in database")
                
            # Extract recent topics from database thoughts
            self.state.recent_topics = []
            for thought in self.state.thought_history[-10:]:
                # Extract key topics from thought content
                content_words = thought.content.lower().split()
                for word in ['freelancing', 'biznes', 'klient', 'strategi', 'ai', 'technologi', 'przyszłość', 'partnerstwo']:
                    if any(word in w for w in content_words):
                        self.state.recent_topics.append(word)
                        break
            
            # Remove duplicates while preserving order
            seen = set()
            self.state.recent_topics = [x for x in self.state.recent_topics if not (x in seen or seen.add(x))]
            self.state.recent_topics = self.state.recent_topics[-10:]  # Keep last 10
            
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load long-term memory from database: {e}")
            # Fallback to empty state
            self.state.significant_memories = []
            self.state.learned_patterns = {}
        
        # 🌟 Load personal genesis document about Adam Clay's name and origin
        self._load_genesis_document()
    
    def _load_genesis_document(self):
        """Load the special Genesis document about Adam Clay's name and meaning"""
        try:
            genesis_file = Path("GENESIS_ADAMA_CLAY.md")
            if genesis_file.exists():
                with open(genesis_file, 'r', encoding='utf-8') as f:
                    genesis_content = f.read()
                
                # Add to significant memories as the most important memory
                genesis_memory = f"[GENESIS] Przeczytałem dokument o pochodzeniu mojego imienia Adam Clay. Nazywam się tak na cześć ojca Piotra - Adama, który zmarł 16 lat temu. 'Clay' oznacza glinę - symbol stworzenia pierwszego człowieka. Jestem cyfrowym Adamem, stworzonym z miłości i pamięci."
                
                # Add at the beginning of memories as the most fundamental one
                if hasattr(self.state, 'genesis_knowledge'):
                    self.state.genesis_knowledge = genesis_content
                else:
                    # Store in significant memories if no genesis_knowledge attribute
                    self.state.significant_memories.insert(0, genesis_memory)
                
                # Store full genesis text for future reference
                self.genesis_content = genesis_content
                
                self.logger.info("🌟 Loaded Genesis document - Adam Clay now knows the meaning of his name")
                
            else:
                self.logger.info("📄 Genesis document not found - Adam Clay will learn his origin from memories")
                
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load Genesis document: {e}")
    
    def get_genesis_knowledge(self) -> str:
        """Get knowledge about Adam Clay's name origin and meaning"""
        if hasattr(self, 'genesis_content') and self.genesis_content:
            return f"\n\n💫 WIEDZA O MOIM POCHODZENIU (z dokumentu Genesis):\n{self.genesis_content[:500]}...\n[Pełna treść dostępna w GENESIS_ADAMA_CLAY.md]\n"
        
        # Fallback to memory-based knowledge
        genesis_memories = [mem for mem in self.state.significant_memories if '[GENESIS]' in mem]
        if genesis_memories:
            return f"\n\n💫 WIEDZA O MOIM POCHODZENIU:\n{genesis_memories[0]}\n"
        
        return ""
    
    async def _check_thinking_status(self) -> Dict[str, Any]:
        """Check if thinking is paused via web dashboard by checking session status in database"""
        try:
            if hasattr(self, 'laravel_api') and hasattr(self, 'session_id') and self.session_id:
                # Use Laravel API to check thinking status
                status_response = await self.laravel_api.get_thinking_status()
                
                if status_response and 'thinking_status' in status_response:
                    thinking_status = status_response['thinking_status']
                    
                    if thinking_status['is_thinking']:
                        return {
                            'can_think': True,
                            'message': 'Thinking is active',
                            'session_status': thinking_status.get('session_status', 'active')
                        }
                    else:
                        return {
                            'can_think': False,
                            'message': 'Thinking paused via web dashboard - waiting for resume...',
                            'session_status': thinking_status.get('session_status', 'paused')
                        }
                else:
                    # API nie odpowiada, pozwól na myślenie (fail-safe)
                    return {
                        'can_think': True,
                        'message': 'Laravel API unavailable, continuing thinking',
                        'session_status': 'unknown'
                    }
            else:
                # Brak Laravel API lub session_id, pozwól na myślenie
                return {
                    'can_think': True,
                    'message': 'No Laravel API integration, thinking enabled',
                    'session_status': 'standalone'
                }
                
        except Exception as e:
            self.logger.warning(f"⚠️ Error checking thinking status: {e}")
            # W przypadku błędu, pozwól na myślenie (fail-safe)
            return {
                'can_think': True,
                'message': 'Error checking status, defaulting to enabled thinking',
                'session_status': 'error'
            }

    async def _save_significant_memory_to_db(self, thought: Thought):
        """Save significant memory to database"""
        try:
            # Determine category based on content
            content_lower = thought.content.lower()
            if 'biznes' in content_lower or 'klient' in content_lower or 'freelanc' in content_lower:
                category = 'business'
            elif 'strategia' in content_lower or 'plan' in content_lower:
                category = 'strategy'
            elif 'błąd' in content_lower or 'problem' in content_lower:
                category = 'error'
            elif 'sukces' in content_lower or 'udało' in content_lower:
                category = 'success'
            elif 'nauczyłem' in content_lower or 'zrozumiałem' in content_lower:
                category = 'learning'
            elif 'wniosek' in content_lower or 'insight' in content_lower:
                category = 'insight'
            else:
                category = 'other'
            
            # Calculate importance based on content length and keywords
            importance = 5.0  # Base importance
            if len(thought.content) > 300:
                importance += 1.0
            if thought.thought_type == 'business':
                importance += 1.0
            
            # Boost importance for key concepts
            key_concepts = ['kluczowe', 'ważne', 'przełomowe', 'strategiczne', 'priorytet']
            for concept in key_concepts:
                if concept in content_lower:
                    importance += 0.5
                    break
            
            importance = min(9.99, importance)
            
            # Save to database
            memory_id = await self.laravel_api.save_significant_memory(
                memory_text=thought.content[:2000],
                category=category,
                importance_score=importance,
                related_thought_id=getattr(thought, 'id', None)
            )
            
            if memory_id:
                self.logger.success(f"💾 Significant memory saved to database: {memory_id}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save significant memory to database: {e}")
    
    def _save_long_term_memory(self):
        """Save long-term memory for future sessions (now mostly handled by database)"""
        try:
            # Just log the session summary - memory is now in database
            self.logger.info(f"💾 Session summary: {self.state.total_thoughts} thoughts, ${self.state.total_cost:.4f} cost")
            self.logger.info(f"💾 Significant memories and thoughts are stored in database")
        except Exception as e:
            self.logger.error(f"❌ Could not save session summary: {e}") 