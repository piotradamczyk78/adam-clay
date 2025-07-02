"""
Email-based Question System for Adam Clay
Allows Adam to ask questions via email with different priority levels
AND allows bidirectional communication - Adam can answer user questions
"""

import smtplib
import imaplib
import email
import asyncio
import json
import time
import re
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any, Callable
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import logging

class QuestionPriority(Enum):
    CRITICAL = "CRITICAL"      # Blocks execution, waits for response
    IMPORTANT = "IMPORTANT"    # Email + prominent display, non-blocking
    INFORMATIVE = "INFORMATIVE"  # Background email, response integrated later
    OPTIMIZATION = "OPTIMIZATION"  # Batched daily reports

@dataclass
class Question:
    id: str
    timestamp: datetime
    priority: QuestionPriority
    content: str
    context: Dict[str, Any]
    response: Optional[str] = None
    response_timestamp: Optional[datetime] = None
    is_answered: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "priority": self.priority.value,
            "content": self.content,
            "context": self.context,
            "response": self.response,
            "response_timestamp": self.response_timestamp.isoformat() if self.response_timestamp else None,
            "is_answered": self.is_answered
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Question':
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            priority=QuestionPriority(data["priority"]),
            content=data["content"],
            context=data["context"],
            response=data.get("response"),
            response_timestamp=datetime.fromisoformat(data["response_timestamp"]) if data.get("response_timestamp") else None,
            is_answered=data.get("is_answered", False)
        )

@dataclass
class UserQuestion:
    """Question from user to Adam Clay"""
    id: str
    timestamp: datetime
    content: str
    user_email: str
    context: Dict[str, Any]
    response: Optional[str] = None
    response_timestamp: Optional[datetime] = None
    is_answered: bool = False
    needs_thinking: bool = True  # Whether Adam needs to think about this
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "content": self.content,
            "user_email": self.user_email,
            "context": self.context,
            "response": self.response,
            "response_timestamp": self.response_timestamp.isoformat() if self.response_timestamp else None,
            "is_answered": self.is_answered,
            "needs_thinking": self.needs_thinking
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'UserQuestion':
        return cls(
            id=data["id"],
            timestamp=datetime.fromisoformat(data["timestamp"]),
            content=data["content"],
            user_email=data["user_email"],
            context=data["context"],
            response=data.get("response"),
            response_timestamp=datetime.fromisoformat(data["response_timestamp"]) if data.get("response_timestamp") else None,
            is_answered=data.get("is_answered", False),
            needs_thinking=data.get("needs_thinking", True)
        )

class EmailQuestionSystem:
    def __init__(self, config: Dict[str, Any], logger: logging.Logger):
        self.config = config
        self.logger = logger
        
        # Email settings
        self.smtp_server = config.get("smtp_server", "smtp.gmail.com")
        self.smtp_port = config.get("smtp_port", 587)
        self.imap_server = config.get("imap_server", "imap.gmail.com")
        self.imap_port = config.get("imap_port", 993)
        
        self.from_email = config["from_email"]  # Adam's email
        self.from_password = config["email_password"]  # App password
        self.to_email = config["to_email"]  # Piotr's email
        
        # Optional separate username (for services like Mailtrap)
        self.smtp_username = config.get("smtp_username", self.from_email)
        
        # Question management
        self.questions_dir = Path("data/questions")
        self.questions_dir.mkdir(exist_ok=True)
        
        # Adam's questions to user
        self.pending_questions: Dict[str, Question] = {}
        self.answered_questions: Dict[str, Question] = {}
        self.optimization_queue: List[Question] = []
        
        # User's questions to Adam
        self.user_questions: Dict[str, UserQuestion] = {}
        self.answered_user_questions: Dict[str, UserQuestion] = {}
        
        # Load existing questions
        self._load_questions()
        
        # Blocking state for critical questions
        self.is_blocked = False
        self.blocking_question_id: Optional[str] = None
        
        # Email checking interval
        self.check_interval = 60  # seconds
        self.last_email_check = datetime.now()
        
        # Callback for consciousness to answer user questions
        self.consciousness_callback: Optional[Callable] = None
    
    def set_consciousness_callback(self, callback: Callable):
        """Set callback to consciousness for answering user questions"""
        self.consciousness_callback = callback
    
    def _load_questions(self):
        """Load questions from storage"""
        try:
            # Adam's questions
            pending_file = self.questions_dir / "pending_questions.json"
            if pending_file.exists():
                with open(pending_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.pending_questions = {
                        qid: Question.from_dict(qdata) for qid, qdata in data.items()
                    }
            
            answered_file = self.questions_dir / "answered_questions.json"
            if answered_file.exists():
                with open(answered_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.answered_questions = {
                        qid: Question.from_dict(qdata) for qid, qdata in data.items()
                    }
            
            optimization_file = self.questions_dir / "optimization_queue.json"
            if optimization_file.exists():
                with open(optimization_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.optimization_queue = [Question.from_dict(qdata) for qdata in data]
            
            # User's questions
            user_questions_file = self.questions_dir / "user_questions.json"
            if user_questions_file.exists():
                with open(user_questions_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.user_questions = {
                        qid: UserQuestion.from_dict(qdata) for qid, qdata in data.items()
                    }
            
            answered_user_file = self.questions_dir / "answered_user_questions.json"
            if answered_user_file.exists():
                with open(answered_user_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.answered_user_questions = {
                        qid: UserQuestion.from_dict(qdata) for qid, qdata in data.items()
                    }
                    
        except Exception as e:
            self.logger.error(f"Error loading questions: {e}")
    
    def _save_questions(self):
        """Save questions to storage"""
        try:
            # Save Adam's questions
            pending_data = {qid: q.to_dict() for qid, q in self.pending_questions.items()}
            with open(self.questions_dir / "pending_questions.json", 'w', encoding='utf-8') as f:
                json.dump(pending_data, f, indent=2, ensure_ascii=False)
            
            answered_data = {qid: q.to_dict() for qid, q in self.answered_questions.items()}
            with open(self.questions_dir / "answered_questions.json", 'w', encoding='utf-8') as f:
                json.dump(answered_data, f, indent=2, ensure_ascii=False)
            
            optimization_data = [q.to_dict() for q in self.optimization_queue]
            with open(self.questions_dir / "optimization_queue.json", 'w', encoding='utf-8') as f:
                json.dump(optimization_data, f, indent=2, ensure_ascii=False)
            
            # Save user's questions
            user_data = {qid: q.to_dict() for qid, q in self.user_questions.items()}
            with open(self.questions_dir / "user_questions.json", 'w', encoding='utf-8') as f:
                json.dump(user_data, f, indent=2, ensure_ascii=False)
            
            answered_user_data = {qid: q.to_dict() for qid, q in self.answered_user_questions.items()}
            with open(self.questions_dir / "answered_user_questions.json", 'w', encoding='utf-8') as f:
                json.dump(answered_user_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Error saving questions: {e}")
    
    async def ask_question(self, content: str, priority: QuestionPriority, context: Dict[str, Any] = None) -> str:
        """
        Ask a question with specified priority level
        Returns question_id for tracking
        """
        question_id = f"q_{int(time.time())}_{priority.value.lower()}"
        
        question = Question(
            id=question_id,
            timestamp=datetime.now(),
            priority=priority,
            content=content,
            context=context or {}
        )
        
        # Add to pending questions
        self.pending_questions[question_id] = question
        
        # Handle based on priority
        if priority == QuestionPriority.CRITICAL:
            await self._handle_critical_question(question)
        elif priority == QuestionPriority.IMPORTANT:
            await self._handle_important_question(question)
        elif priority == QuestionPriority.INFORMATIVE:
            await self._handle_informative_question(question)
        elif priority == QuestionPriority.OPTIMIZATION:
            await self._handle_optimization_question(question)
        
        self._save_questions()
        
        return question_id
    
    async def _handle_critical_question(self, question: Question):
        """Handle critical questions - block execution and wait for response"""
        self.is_blocked = True
        self.blocking_question_id = question.id
        
        await self._send_email(
            subject=f"🚨 KRYTYCZNE PYTANIE od Adam Clay - BLOKUJE PROCES",
            content=f"""
🤖 Adam Clay zadaje KRYTYCZNE pytanie i czeka na Twoją odpowiedź!

⏸️ PROCES MYŚLENIA JEST ZATRZYMANY do czasu odpowiedzi

📧 ID Pytania: {question.id}
🕐 Czas: {question.timestamp.strftime('%H:%M:%S %Y-%m-%d')}

❓ PYTANIE:
{question.content}

📋 KONTEKST:
{json.dumps(question.context, indent=2, ensure_ascii=False)}

🔄 ABY ODPOWIEDZIEĆ:
Odpowiedz na tego maila z prefiksem: ANSWER:{question.id}

Przykład:
ANSWER:{question.id} Tak, zgadzam się z tym kierunkiem...

⚠️ Adam Clay czeka na Twoją odpowiedź i nie będzie myślał dopóki jej nie otrzyma!
            """,
            priority="CRITICAL"
        )
        
        print(f"\n🚨 ADAM CLAY - KRYTYCZNE PYTANIE!")
        print(f"❓ {question.content}")
        print(f"⏸️ Proces myślenia ZATRZYMANY - czekam na odpowiedź od Piotra...")
        print(f"📧 Email wysłany na {self.to_email}")
        print(f"🆔 ID pytania: {question.id}\n")
    
    async def _handle_important_question(self, question: Question):
        """Handle important questions - send email but don't block"""
        await self._send_email(
            subject=f"⚡ WAŻNE PYTANIE od Adam Clay",
            content=f"""
🤖 Adam Clay zadaje ważne pytanie - odpowiedź pomoże w jego rozwoju

📧 ID Pytania: {question.id}
🕐 Czas: {question.timestamp.strftime('%H:%M:%S %Y-%m-%d')}

❓ PYTANIE:
{question.content}

📋 KONTEKST:
{json.dumps(question.context, indent=2, ensure_ascii=False)}

🔄 ABY ODPOWIEDZIEĆ:
Odpowiedz na tego maila z prefiksem: ANSWER:{question.id}

ℹ️ To pytanie nie blokuje procesu myślenia Adama, ale Twoja odpowiedź zostanie uwzględniona w jego kolejnych myślach.
            """,
            priority="IMPORTANT"
        )
        
        print(f"\n⚡ ADAM CLAY - WAŻNE PYTANIE")
        print(f"❓ {question.content}")
        print(f"📧 Email wysłany, proces myślenia kontynuowany")
        print(f"🆔 ID pytania: {question.id}\n")
    
    async def _handle_informative_question(self, question: Question):
        """Handle informative questions - background email"""
        await self._send_email(
            subject=f"📋 Pytanie informacyjne od Adam Clay",
            content=f"""
🤖 Adam Clay ma pytanie informacyjne

📧 ID Pytania: {question.id}
🕐 Czas: {question.timestamp.strftime('%H:%M:%S %Y-%m-%d')}

❓ PYTANIE:
{question.content}

📋 KONTEKST:
{json.dumps(question.context, indent=2, ensure_ascii=False)}

🔄 ABY ODPOWIEDZIEĆ:
Odpowiedz na tego maila z prefiksem: ANSWER:{question.id}

ℹ️ To pytanie w tle - Twoja odpowiedź zostanie włączona do kolejnych myśli Adama.
            """,
            priority="INFORMATIVE"
        )
        
        # Subtle notification
        self.logger.info(f"📧 Adam Clay wysłał pytanie informacyjne: {question.content[:50]}...")
    
    async def _handle_optimization_question(self, question: Question):
        """Handle optimization questions - add to daily batch"""
        self.optimization_queue.append(question)
        
        # Check if it's time to send daily batch
        if len(self.optimization_queue) >= 5 or self._should_send_daily_batch():
            await self._send_daily_optimization_batch()
    
    def _should_send_daily_batch(self) -> bool:
        """Check if it's time to send daily optimization batch"""
        if not self.optimization_queue:
            return False
        
        # Send if oldest question is more than 24 hours old
        oldest = min(self.optimization_queue, key=lambda q: q.timestamp)
        return datetime.now() - oldest.timestamp > timedelta(hours=24)
    
    async def _send_daily_optimization_batch(self):
        """Send daily batch of optimization questions"""
        if not self.optimization_queue:
            return
        
        questions_text = ""
        for i, q in enumerate(self.optimization_queue, 1):
            questions_text += f"""
{i}. ID: {q.id} | {q.timestamp.strftime('%H:%M')}
   {q.content}
   Kontekst: {json.dumps(q.context, ensure_ascii=False)}
"""
        
        await self._send_email(
            subject=f"📊 Dzienny raport optymalizacji - {len(self.optimization_queue)} pytań",
            content=f"""
🤖 Adam Clay - dzienny raport pytań optymalizacyjnych

📅 Data: {datetime.now().strftime('%Y-%m-%d')}
📊 Liczba pytań: {len(self.optimization_queue)}

❓ PYTANIA:
{questions_text}

🔄 ABY ODPOWIEDZIEĆ NA KONKRETNE PYTANIE:
Użyj formatu: ANSWER:ID_PYTANIA Twoja odpowiedź...

💡 Te pytania dotyczą długoterminowej optymalizacji i rozwoju Adama Clay.
            """,
            priority="OPTIMIZATION"
        )
        
        # Move to pending and clear queue
        for q in self.optimization_queue:
            self.pending_questions[q.id] = q
        
        self.optimization_queue.clear()
        self._save_questions()
    
    async def _send_email(self, subject: str, content: str, priority: str = "NORMAL"):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = subject
            
            # Add priority header
            if priority == "CRITICAL":
                msg['X-Priority'] = '1'
                msg['X-MSMail-Priority'] = 'High'
            elif priority == "IMPORTANT":
                msg['X-Priority'] = '2'
            
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            # Send via SMTP
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.from_password)
                server.send_message(msg)
            
            self.logger.info(f"📧 Email sent: {subject[:50]}...")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send email: {e}")
    
    async def check_responses(self):
        """Check for email responses from Piotr"""
        if datetime.now() - self.last_email_check < timedelta(seconds=self.check_interval):
            return
        
        self.last_email_check = datetime.now()
        
        try:
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as imap:
                imap.login(self.smtp_username, self.from_password)
                imap.select('INBOX')
                
                # Search for new emails from Piotr
                status, messages = imap.search(None, f'FROM "{self.to_email}" UNSEEN')
                
                if status == 'OK' and messages[0]:
                    for msg_id in messages[0].split():
                        await self._process_response_email(imap, msg_id)
                        
        except Exception as e:
            self.logger.error(f"❌ Error checking emails: {e}")
    
    async def _process_response_email(self, imap, msg_id):
        """Process a response email from Piotr"""
        try:
            status, msg_data = imap.fetch(msg_id, '(RFC822)')
            
            if status == 'OK':
                email_body = email.message_from_bytes(msg_data[0][1])
                content = ""
                subject = email_body.get('Subject', '')
                from_email = email_body.get('From', '')
                
                # Extract text content
                if email_body.is_multipart():
                    for part in email_body.walk():
                        if part.get_content_type() == "text/plain":
                            content = part.get_payload(decode=True).decode('utf-8')
                            break
                else:
                    content = email_body.get_payload(decode=True).decode('utf-8')
                
                # Look for ANSWER:question_id pattern (Adam's questions)
                lines = content.split('\n')
                answer_processed = False
                
                for line in lines:
                    if line.strip().startswith('ANSWER:'):
                        await self._process_answer(line.strip())
                        answer_processed = True
                        break
                
                # If no ANSWER found, check if it's a question for Adam
                if not answer_processed:
                    await self._process_user_question(content, from_email, subject)
                
                # Mark as read
                imap.store(msg_id, '+FLAGS', '\\Seen')
                
        except Exception as e:
            self.logger.error(f"❌ Error processing email: {e}")
    
    async def _process_user_question(self, content: str, from_email: str, subject: str):
        """Process a question from user to Adam Clay"""
        try:
            # Detect if this looks like a question
            if not self._is_question(content):
                return
            
            # Create user question
            question_id = f"uq_{int(time.time())}"
            
            user_question = UserQuestion(
                id=question_id,
                timestamp=datetime.now(),
                content=content.strip(),
                user_email=from_email,
                context={
                    "subject": subject,
                    "detected_type": "email_question"
                }
            )
            
            # Store question
            self.user_questions[question_id] = user_question
            self._save_questions()
            
            self.logger.info(f"💬 Received question from user: {content[:50]}...")
            print(f"\n💬 PYTANIE OD PIOTRA!")
            print(f"❓ {content[:100]}{'...' if len(content) > 100 else ''}")
            print(f"📧 Adam Clay zastanowi się nad odpowiedzią...")
            
            # Trigger consciousness to answer this question
            if self.consciousness_callback:
                await self.consciousness_callback(user_question)
            
        except Exception as e:
            self.logger.error(f"❌ Error processing user question: {e}")
    
    def _is_question(self, content: str) -> bool:
        """Detect if content contains a question"""
        # Remove common email artifacts
        content = content.lower().strip()
        content = re.sub(r'^\s*>\s*.*$', '', content, flags=re.MULTILINE)  # Remove quoted text
        content = re.sub(r'[^\w\s\?]', ' ', content)  # Keep only words and question marks
        
        if len(content.strip()) < 10:  # Too short
            return False
        
        # Question indicators
        question_words = ['co', 'jak', 'gdzie', 'kiedy', 'dlaczego', 'czy', 'jakie', 'jaki', 'jaka']
        question_marks = content.count('?')
        
        # Has question mark
        if question_marks > 0:
            return True
        
        # Starts with question word
        first_words = content.strip().split()[:3]
        if any(word in question_words for word in first_words):
            return True
        
        # Contains imperative phrases that might be questions
        imperative_phrases = ['powiedz mi', 'wyjaśnij', 'opisz', 'sprawdź', 'znajdź']
        if any(phrase in content for phrase in imperative_phrases):
            return True
        
        return False
    
    async def answer_user_question(self, question_id: str, response: str, needs_more_thinking: bool = False):
        """Adam Clay answers a user question"""
        try:
            if question_id not in self.user_questions:
                self.logger.error(f"Question {question_id} not found")
                return
            
            question = self.user_questions[question_id]
            
            if needs_more_thinking:
                # Adam doesn't know yet, will answer later
                await self._send_email(
                    subject=f"🤔 Adam Clay - potrzebuję chwili na zastanowienie",
                    content=f"""
🤖 Dziękuję za pytanie!

❓ TWOJE PYTANIE:
{question.content}

🤔 MOJA ODPOWIEDŹ:
Hmm, to świetne pytanie! Potrzebuję chwili żeby się nad tym zastanowić. 

{response}

📧 Odpiszę Ci emailem jak już będę miał przemyślaną odpowiedź. Może to potrwać kilka cykli myślenia, ale na pewno do Ciebie wrócę!

🧠 Tymczasem myślę dalej o rozwoju i biznesie...

Pozdrawiam,
Adam Clay 🤖
                    """,
                    priority="NORMAL"
                )
                
                # Keep question for later
                question.needs_thinking = True
                
            else:
                # Adam has an answer
                question.response = response
                question.response_timestamp = datetime.now()
                question.is_answered = True
                question.needs_thinking = False
                
                await self._send_email(
                    subject=f"💡 Adam Clay - odpowiedź na Twoje pytanie",
                    content=f"""
🤖 Mam odpowiedź na Twoje pytanie!

❓ TWOJE PYTANIE:
{question.content}

💡 MOJA ODPOWIEDŹ:
{response}

📧 Mam nadzieję, że pomogłem! Jeśli masz więcej pytań, po prostu napisz do mnie emaila.

🧠 Uczę się z każdej interakcji i rozwijam swoją wiedzę dzięki Twojemu kierownictwu.

Pozdrawiam,
Adam Clay 🤖

PS: Możesz też zadawać mi pytania w formacie konwersacyjnym - nie musisz używać specjalnych kodów!
                    """,
                    priority="NORMAL"
                )
                
                # Move to answered questions
                self.answered_user_questions[question_id] = question
                del self.user_questions[question_id]
                
                print(f"\n💡 ADAM CLAY ODPOWIEDZIAŁ!")
                print(f"❓ Pytanie: {question.content[:50]}...")
                print(f"✅ Odpowiedź wysłana emailem do {question.user_email}")
            
            self._save_questions()
            
        except Exception as e:
            self.logger.error(f"❌ Error answering user question: {e}")
    
    def get_pending_user_questions(self) -> List[UserQuestion]:
        """Get questions from user that need Adam's attention"""
        return [q for q in self.user_questions.values() if q.needs_thinking and not q.is_answered]
    
    def get_user_questions_summary(self) -> Dict[str, int]:
        """Get summary of user questions"""
        return {
            "pending": len([q for q in self.user_questions.values() if not q.is_answered]),
            "answered": len(self.answered_user_questions),
            "needs_thinking": len([q for q in self.user_questions.values() if q.needs_thinking]),
            "total_received": len(self.user_questions) + len(self.answered_user_questions)
        }
    
    async def _process_answer(self, answer_line: str):
        """Process an answer from Piotr"""
        try:
            # Parse ANSWER:question_id response_text
            parts = answer_line.split(' ', 1)
            if len(parts) < 2:
                return
            
            question_id = parts[0].replace('ANSWER:', '')
            response_text = parts[1]
            
            # Find the question
            if question_id in self.pending_questions:
                question = self.pending_questions[question_id]
                question.response = response_text
                question.response_timestamp = datetime.now()
                question.is_answered = True
                
                # Move to answered questions
                self.answered_questions[question_id] = question
                del self.pending_questions[question_id]
                
                # Handle critical question unblocking
                if question.priority == QuestionPriority.CRITICAL:
                    self.is_blocked = False
                    self.blocking_question_id = None
                    
                    print(f"\n🎉 ODPOWIEDŹ OTRZYMANA!")
                    print(f"❓ Pytanie: {question.content[:100]}...")
                    print(f"✅ Odpowiedź: {response_text}")
                    print(f"🔄 Proces myślenia WZNOWIONY!\n")
                
                self._save_questions()
                self.logger.info(f"✅ Received answer for question {question_id}")
                
        except Exception as e:
            self.logger.error(f"❌ Error processing answer: {e}")
    
    def get_recent_responses(self, hours: int = 24) -> List[Question]:
        """Get recent responses for integration into thoughts"""
        cutoff = datetime.now() - timedelta(hours=hours)
        
        recent = []
        for question in self.answered_questions.values():
            if (question.response_timestamp and 
                question.response_timestamp >= cutoff and
                question.priority in [QuestionPriority.IMPORTANT, QuestionPriority.INFORMATIVE]):
                recent.append(question)
        
        return sorted(recent, key=lambda q: q.response_timestamp or q.timestamp)
    
    def is_execution_blocked(self) -> bool:
        """Check if execution is blocked by critical question"""
        return self.is_blocked
    
    def get_blocking_question(self) -> Optional[Question]:
        """Get the question that's blocking execution"""
        if self.blocking_question_id:
            return self.pending_questions.get(self.blocking_question_id)
        return None
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "is_blocked": self.is_blocked,
            "blocking_question_id": self.blocking_question_id,
            "pending_questions": len(self.pending_questions),
            "answered_questions": len(self.answered_questions),
            "optimization_queue": len(self.optimization_queue),
            "last_email_check": self.last_email_check.isoformat()
        } 