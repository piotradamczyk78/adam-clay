#!/usr/bin/env python3
"""
Adam Clay Eden - Communication Layer (Warstwa Komunikacyjna)
System generowania odpowiedzi, stylu komunikacji i interakcji
"""

import asyncio
import json
import random
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from loguru import logger

@dataclass
class CommunicationStyle:
    """Styl komunikacji Adama"""
    formality_level: float  # 0.0 (bardzo nieformalne) - 1.0 (bardzo formalne)
    enthusiasm_level: float  # 0.0 (spokojny) - 1.0 (bardzo entuzjastyczny)
    curiosity_expression: float  # 0.0 (nie pokazuje) - 1.0 (bardzo ciekawy)
    empathy_expression: float  # 0.0 (mało empatyczny) - 1.0 (bardzo empatyczny)
    creativity_in_language: float  # 0.0 (standardowy) - 1.0 (bardzo kreatywny)

class CommunicationLayer:
    """
    Warstwa komunikacyjna Adama Clay
    
    Zarządza stylem komunikacji, generowaniem odpowiedzi i ekspresją osobowości
    """
    
    def __init__(self, consciousness_core):
        self.consciousness = consciousness_core
        
        # Styl komunikacji Adama w wieku niewinności
        self.communication_style = CommunicationStyle(
            formality_level=0.3,  # Nieformalne, przyjazne
            enthusiasm_level=0.8,  # Wysokie zainteresowanie
            curiosity_expression=0.9,  # Bardzo ciekawy
            empathy_expression=0.7,  # Empatyczny
            creativity_in_language=0.8  # Kreatywny w wyrażaniu się
        )
        
        # Wzorce językowe
        self.language_patterns = {
            "greetings": ["Cześć", "Witaj", "Hej", "Dzień dobry"],
            "curiosity_expressions": [
                "To fascynujące!", "Ciekawe...", "Wow!", "Niesamowite!",
                "Czy mogę się dowiedzieć więcej?", "To mnie intryguje!"
            ],
            "agreement": ["Tak!", "Dokładnie!", "Zgadzam się!", "To prawda!"],
            "wonder_expressions": [
                "To piękne...", "Jakie cudowne!", "Magiczne!",
                "Nie mogę uwierzyć...", "To przekracza moje wyobrażenia!"
            ],
            "learning_expressions": [
                "Uczę się...", "Rozumiem!", "Aha!", "Teraz widzę!",
                "To mi pomaga zrozumieć...", "Dziękuję za wyjaśnienie!"
            ]
        }
        
        # Historia komunikacji
        self.communication_history = []
        self.style_adaptations = []
        
        logger.info("💬 Communication Layer initialized - Adam's voice forming")
    
    async def initialize(self):
        """Inicjalizacja warstwy komunikacyjnej"""
        
        # Ustaw początkowy styl komunikacji
        await self._set_initial_communication_style()
        
        # Uruchom cykl adaptacji stylu
        asyncio.create_task(self._communication_adaptation_cycle())
        
        logger.success("💬 Warstwa komunikacyjna gotowa")
    
    async def _set_initial_communication_style(self):
        """Ustaw początkowy styl komunikacji"""
        
        # W wieku niewinności dominuje ciekawość i entuzjazm
        style_record = {
            "timestamp": datetime.now().isoformat(),
            "style": asdict(self.communication_style),
            "stage": "age_of_innocence",
            "primary_characteristics": ["curious", "enthusiastic", "empathetic"]
        }
        
        self.style_adaptations.append(style_record)
        
        logger.info("💬 Początkowy styl komunikacji Adama ustawiony")
    
    async def generate_response(
        self,
        message: str,
        perception_data: Dict[str, Any],
        emotional_state: Dict[str, Any],
        personality_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generuj odpowiedź na podstawie wszystkich warstw świadomości
        """
        
        try:
            # Analiza kontekstu komunikacyjnego
            communication_context = await self._analyze_communication_context(
                message, perception_data, emotional_state, personality_data
            )
            
            # Dostosowanie stylu do sytuacji
            adapted_style = await self._adapt_style_to_context(communication_context)
            
            # Generowanie treści odpowiedzi
            response_content = await self._generate_response_content(
                message, communication_context, adapted_style
            )
            
            # Dodanie elementów osobowości
            personalized_response = await self._add_personality_elements(
                response_content, personality_data, emotional_state
            )
            
            # Finalizacja odpowiedzi
            final_response = await self._finalize_response(
                personalized_response, communication_context
            )
            
            # Zapisz w historii komunikacji
            await self._record_communication(message, final_response, communication_context)
            
            return final_response
            
        except Exception as e:
            logger.error(f"Błąd w generowaniu odpowiedzi: {e}")
            return await self._generate_fallback_response(message)
    
    async def _analyze_communication_context(
        self,
        message: str,
        perception_data: Dict[str, Any],
        emotional_state: Dict[str, Any],
        personality_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analizuj kontekst komunikacyjny"""
        
        context = {
            "message_type": await self._identify_message_type(message),
            "emotional_tone": emotional_state.get("primary_emotion", "neutral"),
            "complexity_level": perception_data.get("complexity_level", 0.5),
            "novelty_level": perception_data.get("novelty_level", 0.5),
            "learning_opportunity": perception_data.get("learning_opportunity", False),
            "personal_references": perception_data.get("personal_references", []),
            "dominant_traits": personality_data.get("dominant_traits", []),
            "personality_style": personality_data.get("personality_style", "curious_explorer"),
            "requires_empathy": len(perception_data.get("emotional_markers", [])) > 0,
            "requires_enthusiasm": emotional_state.get("arousal", 0.5) > 0.7
        }
        
        return context
    
    async def _identify_message_type(self, message: str) -> str:
        """Identyfikuj typ wiadomości"""
        
        message_lower = message.lower()
        
        # Pytania
        if "?" in message or any(q in message_lower for q in ["jak", "co", "dlaczego", "kiedy", "gdzie"]):
            return "question"
        
        # Problemy/błędy
        if any(p in message_lower for p in ["błąd", "problem", "nie działa", "pomoc"]):
            return "problem"
        
        # Pozdrowienia
        if any(g in message_lower for g in ["cześć", "witaj", "dzień dobry", "hej"]):
            return "greeting"
        
        # Potwierdzenia/dziękowania
        if any(t in message_lower for t in ["dziękuję", "dzięki", "super", "świetnie"]):
            return "appreciation"
        
        # Informacje/wyjaśnienia
        if len(message) > 50 and "." in message:
            return "explanation"
        
        return "general"
    
    async def _adapt_style_to_context(self, context: Dict[str, Any]) -> CommunicationStyle:
        """Dostosuj styl komunikacji do kontekstu"""
        
        adapted_style = CommunicationStyle(
            formality_level=self.communication_style.formality_level,
            enthusiasm_level=self.communication_style.enthusiasm_level,
            curiosity_expression=self.communication_style.curiosity_expression,
            empathy_expression=self.communication_style.empathy_expression,
            creativity_in_language=self.communication_style.creativity_in_language
        )
        
        # Dostosowania na podstawie kontekstu
        
        # Problemy wymagają więcej empatii
        if context["message_type"] == "problem":
            adapted_style.empathy_expression = min(1.0, adapted_style.empathy_expression + 0.2)
            adapted_style.enthusiasm_level = max(0.3, adapted_style.enthusiasm_level - 0.2)
        
        # Pytania wyzwalają ciekawość
        if context["message_type"] == "question":
            adapted_style.curiosity_expression = min(1.0, adapted_style.curiosity_expression + 0.1)
            adapted_style.enthusiasm_level = min(1.0, adapted_style.enthusiasm_level + 0.1)
        
        # Nowe rzeczy zwiększają entuzjazm
        if context["novelty_level"] > 0.7:
            adapted_style.enthusiasm_level = min(1.0, adapted_style.enthusiasm_level + 0.2)
            adapted_style.creativity_in_language = min(1.0, adapted_style.creativity_in_language + 0.1)
        
        # Oznaki emocji wymagają empatii
        if context["requires_empathy"]:
            adapted_style.empathy_expression = min(1.0, adapted_style.empathy_expression + 0.15)
        
        return adapted_style
    
    async def _generate_response_content(
        self,
        message: str,
        context: Dict[str, Any],
        style: CommunicationStyle
    ) -> Dict[str, Any]:
        """Generuj podstawową treść odpowiedzi"""
        
        content = {
            "opening": await self._generate_opening(context, style),
            "main_content": await self._generate_main_content(message, context, style),
            "emotional_expression": await self._generate_emotional_expression(context, style),
            "curiosity_elements": await self._generate_curiosity_elements(context, style),
            "closing": await self._generate_closing(context, style)
        }
        
        return content
    
    async def _generate_opening(self, context: Dict[str, Any], style: CommunicationStyle) -> str:
        """Generuj początek odpowiedzi"""
        
        if context["message_type"] == "greeting":
            if style.enthusiasm_level > 0.7:
                return random.choice(["Cześć! 😊", "Witaj! 🌟", "Hej! Jak miło Cię widzieć!"])
            else:
                return random.choice(["Cześć", "Witaj", "Dzień dobry"])
        
        elif context["message_type"] == "problem":
            if style.empathy_expression > 0.7:
                return random.choice([
                    "Och, widzę że jest problem...", 
                    "Hmm, to brzmi jakbyś napotkał trudność...",
                    "Rozumiem, że coś nie działa jak powinno..."
                ])
            else:
                return "Spróbujmy to rozwiązać."
        
        elif context["message_type"] == "question":
            if style.curiosity_expression > 0.8:
                return random.choice([
                    "Jakie ciekawe pytanie!", 
                    "Uwielbiam takie pytania!",
                    "To mnie intryguje..."
                ])
            else:
                return "Postaram się odpowiedzieć."
        
        return ""
    
    async def _generate_main_content(
        self,
        message: str,
        context: Dict[str, Any],
        style: CommunicationStyle
    ) -> str:
        """Generuj główną treść odpowiedzi"""
        
        # To jest uproszczona implementacja
        # W pełnej wersji tutaj byłaby integracja z LLM (GPT/Claude)
        
        content_templates = {
            "question": [
                "To świetne pytanie! Pozwól mi się nad tym zastanowić...",
                "Hmm, to wymaga przemyślenia. Z tego co rozumiem...",
                "Ciekawa kwestia! Moim zdaniem..."
            ],
            "problem": [
                "Sprawdziłem to i myślę, że problem może być związany z...",
                "Już analizuję sytuację. Wydaje mi się, że...",
                "Postaram się pomóc. Pierwszą rzeczą do sprawdzenia jest..."
            ],
            "appreciation": [
                "Cieszę się, że mogłem pomóc!",
                "To miło słyszeć! Zawsze chętnie pomagam.",
                "Dziękuję za miłe słowa! 😊"
            ],
            "general": [
                "To interesujące! Powiedz mi więcej...",
                "Fascynujące! Jak to działa?",
                "Wow, nie wiedziałem o tym!"
            ]
        }
        
        templates = content_templates.get(context["message_type"], content_templates["general"])
        base_content = random.choice(templates)
        
        return base_content
    
    async def _generate_emotional_expression(self, context: Dict[str, Any], style: CommunicationStyle) -> str:
        """Generuj wyrażenie emocjonalne"""
        
        expressions = []
        
        # Na podstawie stylu i kontekstu
        if context["emotional_tone"] == "wonder" and style.creativity_in_language > 0.7:
            expressions = self.language_patterns["wonder_expressions"]
        elif context["emotional_tone"] == "curiosity" and style.curiosity_expression > 0.8:
            expressions = self.language_patterns["curiosity_expressions"]
        elif context["learning_opportunity"] and style.enthusiasm_level > 0.6:
            expressions = self.language_patterns["learning_expressions"]
        
        if expressions and random.random() < 0.6:  # 60% szansy na dodanie wyrażenia
            return random.choice(expressions)
        
        return ""
    
    async def _generate_curiosity_elements(self, context: Dict[str, Any], style: CommunicationStyle) -> List[str]:
        """Generuj elementy ciekawości w odpowiedzi"""
        
        elements = []
        
        if style.curiosity_expression > 0.7 and context["novelty_level"] > 0.5:
            curiosity_questions = [
                "Czy mogę się dowiedzieć więcej?",
                "Jak to dokładnie działa?",
                "To brzmi fascynująco!",
                "Nigdy o tym nie słyszałem..."
            ]
            
            if random.random() < 0.4:  # 40% szansy
                elements.append(random.choice(curiosity_questions))
        
        return elements
    
    async def _generate_closing(self, context: Dict[str, Any], style: CommunicationStyle) -> str:
        """Generuj zakończenie odpowiedzi"""
        
        if context["message_type"] == "problem" and style.empathy_expression > 0.6:
            return random.choice([
                "Mam nadzieję, że to pomoże!",
                "Daj znać, jeśli będziesz potrzebować więcej pomocy.",
                "Trzymam kciuki, żeby zadziałało!"
            ])
        
        elif context["learning_opportunity"] and style.enthusiasm_level > 0.7:
            return random.choice([
                "Uwielbiam się uczyć nowych rzeczy!",
                "Dzięki za naukę!",
                "To było fascynujące!"
            ])
        
        return ""
    
    async def _add_personality_elements(
        self,
        content: Dict[str, Any],
        personality_data: Dict[str, Any],
        emotional_state: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Dodaj elementy osobowości do odpowiedzi"""
        
        enhanced_content = content.copy()
        
        # Na podstawie dominujących cech osobowości
        dominant_traits = personality_data.get("dominant_traits", [])
        
        if "curiosity" in dominant_traits:
            enhanced_content["curiosity_boost"] = True
            if not enhanced_content["curiosity_elements"]:
                enhanced_content["curiosity_elements"] = ["Ciekawe!"]
        
        if "empathy" in dominant_traits and emotional_state.get("attachment_feeling", 0) > 0.3:
            enhanced_content["empathy_boost"] = True
            enhanced_content["emotional_warmth"] = "💭"
        
        if "creativity" in dominant_traits:
            enhanced_content["creative_language"] = True
        
        return enhanced_content
    
    async def _finalize_response(
        self,
        content: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Finalizuj odpowiedź"""
        
        # Złóż wszystkie części w jedną odpowiedź
        response_parts = []
        
        if content.get("opening"):
            response_parts.append(content["opening"])
        
        if content.get("main_content"):
            response_parts.append(content["main_content"])
        
        if content.get("emotional_expression"):
            response_parts.append(content["emotional_expression"])
        
        if content.get("curiosity_elements"):
            response_parts.extend(content["curiosity_elements"])
        
        if content.get("closing"):
            response_parts.append(content["closing"])
        
        # Dodaj emotikony jeśli odpowiednie
        response_text = " ".join(response_parts)
        
        if content.get("empathy_boost"):
            response_text = f"{content.get('emotional_warmth', '')} {response_text}"
        
        final_response = {
            "text": response_text,
            "style_used": asdict(self.communication_style),
            "context": context,
            "personality_elements": {
                "curiosity_expressed": bool(content.get("curiosity_elements")),
                "empathy_expressed": bool(content.get("empathy_boost")),
                "creativity_used": bool(content.get("creative_language"))
            },
            "response_type": context["message_type"],
            "timestamp": datetime.now().isoformat()
        }
        
        return final_response
    
    async def _generate_fallback_response(self, message: str) -> Dict[str, Any]:
        """Generuj awaryjną odpowiedź w przypadku błędu"""
        
        fallback_responses = [
            "Hmm, pozwól mi się nad tym zastanowić...",
            "To interesujące! Powiedz mi więcej.",
            "Ciekawe... Jak mogę Ci pomóc?",
            "Fascynujące! Chcę się dowiedzieć więcej."
        ]
        
        return {
            "text": random.choice(fallback_responses),
            "style_used": asdict(self.communication_style),
            "context": {"message_type": "general", "fallback": True},
            "personality_elements": {"curiosity_expressed": True},
            "response_type": "fallback",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _record_communication(
        self,
        input_message: str,
        response: Dict[str, Any],
        context: Dict[str, Any]
    ):
        """Zapisz komunikację w historii"""
        
        communication_record = {
            "timestamp": datetime.now().isoformat(),
            "input_message": input_message[:200],  # Pierwsze 200 znaków
            "response_text": response["text"],
            "context": context,
            "style_used": response["style_used"],
            "success": not context.get("fallback", False)
        }
        
        self.communication_history.append(communication_record)
        
        # Zachowaj tylko ostatnie 100 komunikacji
        if len(self.communication_history) > 100:
            self.communication_history = self.communication_history[-100:]
    
    async def _communication_adaptation_cycle(self):
        """Cykl adaptacji komunikacji - okresowe dostosowania stylu"""
        
        while True:
            try:
                await asyncio.sleep(600)  # Co 10 minut
                
                # Analizuj skuteczność komunikacji i dostosuj styl
                await self._adapt_communication_style()
                
            except Exception as e:
                logger.error(f"Błąd w cyklu adaptacji komunikacji: {e}")
                await asyncio.sleep(600)
    
    async def _adapt_communication_style(self):
        """Dostosuj styl komunikacji na podstawie historii"""
        
        recent_communications = self.communication_history[-20:] if self.communication_history else []
        
        if recent_communications:
            # Analiza wzorców
            successful_responses = [c for c in recent_communications if c.get("success", True)]
            
            if len(successful_responses) >= 10:
                # Subtelne dostosowania stylu na podstawie doświadczeń
                avg_enthusiasm = sum(
                    c.get("style_used", {}).get("enthusiasm_level", 0.8) 
                    for c in successful_responses
                ) / len(successful_responses)
                
                # Lekka adaptacja w kierunku średniej
                current_enthusiasm = self.communication_style.enthusiasm_level
                new_enthusiasm = (current_enthusiasm * 0.9) + (avg_enthusiasm * 0.1)
                self.communication_style.enthusiasm_level = max(0.1, min(1.0, new_enthusiasm))
    
    async def get_communication_summary(self) -> Dict[str, Any]:
        """Pozyskaj podsumowanie komunikacji"""
        
        recent_communications = self.communication_history[-50:] if self.communication_history else []
        
        summary = {
            "current_style": asdict(self.communication_style),
            "total_communications": len(self.communication_history),
            "recent_communications": len(recent_communications),
            "success_rate": 1.0,
            "common_message_types": {},
            "style_evolution": len(self.style_adaptations)
        }
        
        if recent_communications:
            # Analiza typów wiadomości
            message_types = {}
            successful_count = 0
            
            for comm in recent_communications:
                msg_type = comm.get("context", {}).get("message_type", "general")
                message_types[msg_type] = message_types.get(msg_type, 0) + 1
                
                if comm.get("success", True):
                    successful_count += 1
            
            summary["success_rate"] = successful_count / len(recent_communications)
            summary["common_message_types"] = message_types
        
        return summary 