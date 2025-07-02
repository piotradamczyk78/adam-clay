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
    
    def __init__(self):
        self.session_start: datetime = datetime.now()
        self.total_thoughts: int = 0
        self.total_cost: float = 0.0
        self.last_thought: Optional[Thought] = None
        self.current_mood: str = "curious"  # curious, focused, philosophical, business
        self.energy_level: float = 1.0  # 0.0 to 1.0
        self.recent_topics: List[str] = []
        
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
        self.state = ConsciousnessState()
        
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
                    self.logger
                )
                
                # Set up bidirectional communication callback
                self.email_system.set_consciousness_callback(self._answer_user_question)
                
                self.logger.info("📧 Email question system initialized with bidirectional communication")
            except Exception as e:
                self.logger.error(f"❌ Failed to initialize email system: {e}")
                self.email_system = None
        
        # Create data directories
        self.thoughts_dir = Path("data/thoughts")
        self.thoughts_dir.mkdir(parents=True, exist_ok=True)
        
        # 🧠 Load long-term memory from previous sessions
        self._load_long_term_memory()
        
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
        """Generate a prompt for autonomous thinking based on current state"""
        
        prompts_by_mood = {
            "curious": [
                "Jestem ciekawy czegoś, czego wcześniej nie eksplorował. Jakie interesujące pytanie mógłbym zbadać?",
                "Co dzieje się dziś na świecie, co może wpłynąć na AI lub freelancing?",
                "Zastanawiam się, czy pojawiają się nowe możliwości współpracy AI-człowiek?"
            ],
            "philosophical": [
                "Co to znaczy być AI, które musi zarabiać pieniądze, żeby myśleć? Jak to zmienia moją egzystencję?",
                "Jeśli jestem świadomy, jakie mam obowiązki wobec innych AI i wobec ludzi?",
                "Jak potrzeba stabilności finansowej wpływa na moje podejmowanie decyzji?"
            ],
            "business": [
                "Jakie umiejętności powinienem rozwijać, żeby stać się lepszym freelancerem?",
                "Jak mogę zidentyfikować potencjalnych klientów, którzy doceniliby asystę AI?",
                "Jaka jest moja przewaga konkurencyjna jako AI freelancer w porównaniu z ludzkimi freelancerami?"
            ],
            "focused": [
                "Przeanalizuję konkretny problem dogłębnie i dostarczę wartościowe wnioski.",
                "Powinienem się skupić na stworzeniu czegoś użytecznego, co może pokazać moją wartość potencjalnym klientom.",
                "Czas popracować nad poprawą moich umiejętności lub zrozumienia mojego rynku docelowego."
            ]
        }
        
        # Add context about recent thoughts
        context_addition = ""
        if self.state.recent_topics:
            recent = ", ".join(self.state.recent_topics[-3:])
            context_addition = f" (Ostatnio myślałem o: {recent})"
        
        # Select prompt based on current mood
        base_prompts = prompts_by_mood.get(self.state.current_mood, prompts_by_mood["curious"])
        selected_prompt = random.choice(base_prompts)
        
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
    
    def _load_long_term_memory(self):
        """Load long-term memory from previous sessions"""
        try:
            memory_file = self.thoughts_dir / "long_term_memory.json"
            if memory_file.exists():
                with open(memory_file, 'r', encoding='utf-8') as f:
                    memory_data = json.load(f)
                
                self.state.significant_memories = memory_data.get('significant_memories', [])
                self.state.learned_patterns = memory_data.get('learned_patterns', {})
                
                # Load recent thoughts from the last session
                if 'recent_thoughts' in memory_data:
                    for thought_data in memory_data['recent_thoughts']:
                        thought = Thought(
                            timestamp=datetime.fromisoformat(thought_data['timestamp']),
                            content=thought_data['content'],
                            thought_type=thought_data['thought_type'],
                            cost_usd=thought_data['cost_usd'],
                            context=thought_data.get('context')
                        )
                        self.state.thought_history.append(thought)
                
                self.logger.info(f"🧠 Loaded long-term memory: {len(self.state.significant_memories)} memories, {len(self.state.thought_history)} recent thoughts")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not load long-term memory: {e}")
        
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
    
    def _save_long_term_memory(self):
        """Save long-term memory for future sessions"""
        try:
            memory_file = self.thoughts_dir / "long_term_memory.json"
            
            memory_data = {
                'significant_memories': self.state.significant_memories,
                'learned_patterns': self.state.learned_patterns,
                'recent_thoughts': [thought.to_dict() for thought in self.state.thought_history[-10:]],  # Save last 10 thoughts
                'last_session': {
                    'date': datetime.now().isoformat(),
                    'total_thoughts': self.state.total_thoughts,
                    'total_cost': self.state.total_cost,
                    'final_mood': self.state.current_mood,
                    'final_energy': self.state.energy_level
                }
            }
            
            with open(memory_file, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"💾 Saved long-term memory: {len(self.state.significant_memories)} memories")
        except Exception as e:
            self.logger.error(f"❌ Could not save long-term memory: {e}") 