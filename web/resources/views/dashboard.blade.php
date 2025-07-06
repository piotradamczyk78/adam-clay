<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Adam Clay - Live Dashboard</title>
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body class="bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 min-h-screen">
    <div class="container mx-auto p-6" x-data="dashboard()" x-init="init()">
        
        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-5xl font-bold text-white mb-2">
                🧠 <span class="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Adam Clay</span>
            </h1>
            <p class="text-gray-300 text-lg">AI Consciousness Live Dashboard</p>
            <div class="mt-4 flex justify-center items-center space-x-4">
                <div class="flex items-center">
                    <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse mr-2"></div>
                    <span class="text-green-400 font-semibold">LIVE</span>
                </div>
                <span class="text-gray-400" x-text="currentTime"></span>
            </div>
        </header>

        <!-- Control Panel -->
        <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-8">
            <h2 class="text-xl font-bold text-white mb-4 flex items-center">
                🎮 Control Panel
            </h2>
            <div class="flex flex-wrap gap-4 items-center">
                <!-- Pause/Resume button - tylko gdy nie blocked by email -->
                <button x-show="blockingReason !== 'email_question_blocking'"
                        @click="thinkingActive ? pauseThinking() : resumeThinking()" 
                        :disabled="loading"
                        :class="thinkingActive ? 'bg-orange-600 hover:bg-orange-700' : 'bg-green-600 hover:bg-green-700'"
                        class="px-6 py-3 rounded-lg font-semibold text-white transition-all duration-200 transform hover:scale-105 disabled:transform-none disabled:opacity-50">
                    <span x-show="!loading && thinkingActive">⏸️ Wstrzymaj myślenie</span>
                    <span x-show="!loading && !thinkingActive">▶️ Wznów myślenie</span>
                    <span x-show="loading" class="flex items-center">
                        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 714 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Loading...
                    </span>
                </button>
                
                <!-- Email blocking notification -->
                <div x-show="blockingReason === 'email_question_blocking'" 
                     class="bg-red-600/20 border border-red-500/30 rounded-lg p-4 text-red-300">
                    <div class="flex items-center mb-2">
                        <span class="text-red-400 text-xl mr-2">🚨</span>
                        <span class="font-semibold">BLOKOWANE PRZEZ KRYTYCZNE PYTANIE EMAIL</span>
                    </div>
                    <div class="text-sm" x-show="blockingQuestion">
                        <strong>Pytanie:</strong> <span x-text="blockingQuestion?.content"></span>
                        <br><strong>Utworzone:</strong> <span x-text="blockingQuestion?.created_at"></span>
                    </div>
                    <div class="text-xs mt-2 opacity-75">
                        📧 Adam Clay czeka na odpowiedź email żeby kontynuować myślenie
                    </div>
                </div>
                
                <div x-show="blockingReason !== 'email_question_blocking'" class="text-sm text-gray-300">
                    💡 <em>Adam Clay działa w tle, ale można wstrzymać/wznowić myślenie</em>
                </div>
                
                <div class="flex items-center ml-4">
                    <div :class="getStatusIndicatorColor()" 
                         class="w-3 h-3 rounded-full animate-pulse mr-2"></div>
                    <span :class="getStatusTextColor()" 
                          class="font-semibold">
                        <span x-text="getStatusText()"></span>
                    </span>
                </div>
                
                <div x-show="thinkingStatus" class="text-gray-300 text-sm ml-4">
                    🧠 Status: <span x-text="thinkingStatus"></span>
                </div>
            </div>
            
            <!-- Status messages -->
            <div x-show="statusMessage" class="mt-4 p-3 rounded-lg" 
                 :class="statusMessageType === 'success' ? 'bg-green-600/20 text-green-300 border border-green-500/30' : 'bg-red-600/20 text-red-300 border border-red-500/30'">
                <span x-text="statusMessage"></span>
            </div>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-300 text-sm">Dzisiejsze myśli</p>
                        <p class="text-2xl font-bold text-white" x-text="stats.today_thoughts">-</p>
                    </div>
                    <div class="text-blue-400 text-2xl">💭</div>
                </div>
            </div>
            
            <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-300 text-sm">Koszt dziś</p>
                        <p class="text-2xl font-bold text-white">$<span x-text="stats.today_cost">-</span></p>
                    </div>
                    <div class="text-green-400 text-2xl">💰</div>
                </div>
            </div>
            
            <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-300 text-sm">Status sesji</p>
                        <p class="text-lg font-bold" 
                           :class="sessionStatus === 'AKTYWNA' ? 'text-green-400' : 'text-red-400'"
                           x-text="sessionStatus">-</p>
                    </div>
                    <div class="text-purple-400 text-2xl">🧠</div>
                </div>
            </div>
            
            <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20">
                <div class="flex items-center justify-between">
                    <div>
                        <p class="text-gray-300 text-sm">Ostatnia aktywność</p>
                        <p class="text-sm font-bold text-white" x-text="lastActivity">-</p>
                    </div>
                    <div class="text-yellow-400 text-2xl">⚡</div>
                </div>
            </div>
        </div>

        <!-- Current Session Info -->
        <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-8" x-show="currentSession">
            <h2 class="text-xl font-bold text-white mb-4 flex items-center">
                🎯 Aktualna sesja świadomości
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                    <p class="text-gray-400 text-sm">ID Sesji</p>
                    <p class="text-white font-mono text-sm" x-text="currentSession?.id">-</p>
                </div>
                <div>
                    <p class="text-gray-400 text-sm">Rozpoczęta</p>
                    <p class="text-white" x-text="formatDate(currentSession?.started_at)">-</p>
                </div>
                <div>
                    <p class="text-gray-400 text-sm">Myśli w sesji</p>
                    <p class="text-white font-bold" x-text="currentSession?.total_thoughts">-</p>
                </div>
            </div>
        </div>

        <!-- Latest Thought -->
        <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-8" x-show="lastThought">
            <h2 class="text-xl font-bold text-white mb-4 flex items-center">
                💡 Ostatnia myśl
            </h2>
            <div class="space-y-2">
                <div class="flex justify-between items-center">
                    <span class="text-gray-400">Typ:</span>
                    <span class="text-white bg-blue-500/20 px-2 py-1 rounded" x-text="lastThought?.type">-</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-400">Czas:</span>
                    <span class="text-white" x-text="formatDate(lastThought?.timestamp)">-</span>
                </div>
                <div class="flex justify-between items-center">
                    <span class="text-gray-400">ID:</span>
                    <span class="text-white font-mono text-sm" x-text="lastThought?.id">-</span>
                </div>
            </div>
        </div>

        <!-- Live Thoughts Stream -->
        <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-8">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold text-white flex items-center">
                    💭 Live Thoughts Stream
                </h2>
                <div class="flex gap-2">
                    <button @click="refreshThoughts()" 
                            class="px-3 py-1 bg-blue-600 hover:bg-blue-700 rounded text-white text-sm transition-colors">
                        🔄 Refresh
                    </button>
                    <a href="/thoughts/history" 
                       class="px-3 py-1 bg-purple-600 hover:bg-purple-700 rounded text-white text-sm transition-colors">
                        📚 Historia
                    </a>
                </div>
            </div>
            
            <div class="space-y-3 max-h-96 overflow-y-auto">
                <template x-for="thought in recentThoughts" :key="thought.id">
                    <div class="bg-black/20 rounded-lg p-4 border border-white/10 hover:border-white/20 transition-colors">
                        <div class="flex justify-between items-start mb-2">
                            <div class="flex items-center gap-2">
                                <span class="inline-block px-2 py-1 text-xs font-semibold rounded-full"
                                      :class="{
                                          'bg-blue-500/20 text-blue-300': thought.thought_type === 'autonomous',
                                          'bg-green-500/20 text-green-300': thought.thought_type === 'business', 
                                          'bg-purple-500/20 text-purple-300': thought.thought_type === 'philosophical',
                                          'bg-yellow-500/20 text-yellow-300': thought.thought_type === 'reactive'
                                      }"
                                      x-text="thought.thought_type"></span>
                                <span x-show="thought.mood" 
                                      class="inline-block px-2 py-1 text-xs bg-gray-500/20 text-gray-300 rounded-full"
                                      x-text="thought.mood"></span>
                            </div>
                            <div class="text-right text-sm text-gray-400">
                                <div x-text="formatDate(thought.timestamp)"></div>
                                <div class="text-xs">$<span x-text="(thought.cost_usd || 0).toFixed(4)"></span></div>
                            </div>
                        </div>
                        
                        <div class="text-white text-sm leading-relaxed" x-text="thought.content"></div>
                        
                        <div class="flex justify-between items-center mt-2 text-xs text-gray-400">
                            <span>ID: <span x-text="thought.id"></span></span>
                            <div class="flex items-center gap-2">
                                <span x-show="thought.energy_level" class="flex items-center">
                                    ⚡ <span x-text="Math.round(thought.energy_level * 100)"></span>%
                                </span>
                                <span x-show="thought.session_id" x-text="thought.session_id"></span>
                            </div>
                        </div>
                    </div>
                </template>
                
                <div x-show="recentThoughts.length === 0" class="text-center py-8 text-gray-400">
                    <div class="text-4xl mb-2">💭</div>
                    <div>Brak aktualnych myśli</div>
                    <div class="text-sm">Adam Clay jeszcze nie myślał lub jest zatrzymany</div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="text-center text-gray-400 mt-8">
            <p>🚀 Laravel {{ app()->version() }} • MySQL • REST API</p>
            <p class="text-sm mt-2">Auto-refresh co 30 sekund</p>
        </footer>
    </div>

    <script>
        function dashboard() {
            return {
                stats: {},
                currentSession: null,
                lastThought: null,
                sessionStatus: 'NIEZNANY',
                lastActivity: '-',
                currentTime: '',
                
                // Thinking control (via database, not process control)
                thinkingActive: true,
                thinkingStatus: 'Sprawdzanie...',
                blockingReason: null,
                blockingQuestion: null,
                loading: false,
                statusMessage: '',
                statusMessageType: 'success',
                
                // Live thoughts
                recentThoughts: [],
                lastThoughtTimestamp: null,
                
                init() {
                    this.updateTime();
                    this.fetchData();
                    this.fetchThinkingStatus();
                    this.fetchRecentThoughts();
                    
                    setInterval(() => this.updateTime(), 1000);
                    setInterval(() => this.fetchData(), 10000); // Refresh co 10s
                    setInterval(() => this.fetchThinkingStatus(), 15000); // Thinking status co 15s
                    setInterval(() => this.fetchRecentThoughts(), 20000); // Recent thoughts co 20s
                },
                
                updateTime() {
                    this.currentTime = new Date().toLocaleTimeString('pl-PL');
                },
                
                async fetchData() {
                    try {
                        const response = await fetch('/api/status');
                        const data = await response.json();
                        
                        if (data.success) {
                            this.stats = {
                                today_thoughts: data.status.today_stats.thoughts,
                                today_cost: data.status.today_stats.cost.toFixed(4)
                            };
                            
                            this.currentSession = data.status.current_session;
                            this.lastThought = data.status.last_thought;
                            
                            this.sessionStatus = this.currentSession ? 'AKTYWNA' : 'NIEAKTYWNA';
                            this.lastActivity = this.lastThought ? this.formatDate(this.lastThought.timestamp) : 'Brak';
                        }
                    } catch (error) {
                        console.error('Błąd pobierania danych:', error);
                    }
                },
                
                formatDate(dateString) {
                    if (!dateString) return '-';
                    return new Date(dateString).toLocaleString('pl-PL');
                },
                
                // Thinking Control Methods (via database)
                async fetchThinkingStatus() {
                    try {
                        const response = await fetch('/api/consciousness/thinking-status');
                        const data = await response.json();
                        
                        if (data.success && data.thinking_status) {
                            this.thinkingActive = data.thinking_status.is_thinking;
                            this.thinkingStatus = data.thinking_status.message;
                            this.blockingReason = data.thinking_status.blocking_reason;
                            this.blockingQuestion = data.thinking_status.blocking_question;
                        } else {
                            this.thinkingStatus = 'Brak danych o statusie';
                            this.blockingReason = null;
                            this.blockingQuestion = null;
                        }
                    } catch (error) {
                        console.error('Błąd pobierania statusu myślenia:', error);
                        this.thinkingStatus = 'Błąd połączenia';
                        this.blockingReason = null;
                        this.blockingQuestion = null;
                    }
                },
                
                async pauseThinking() {
                    if (this.loading || !this.thinkingActive) return;
                    
                    this.loading = true;
                    this.statusMessage = '';
                    
                    try {
                        const response = await fetch('/api/consciousness/pause', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
                            }
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            this.statusMessage = '⏸️ Myślenie Adam Clay zostało wstrzymane';
                            this.statusMessageType = 'success';
                            this.thinkingActive = false;
                            this.thinkingStatus = 'Wstrzymane przez dashboard';
                        } else {
                            this.statusMessage = '❌ Błąd: ' + data.message;
                            this.statusMessageType = 'error';
                        }
                    } catch (error) {
                        this.statusMessage = '❌ Błąd połączenia: ' + error.message;
                        this.statusMessageType = 'error';
                    } finally {
                        this.loading = false;
                        setTimeout(() => this.statusMessage = '', 5000);
                    }
                },
                
                async resumeThinking() {
                    if (this.loading || this.thinkingActive) return;
                    
                    this.loading = true;
                    this.statusMessage = '';
                    
                    try {
                        const response = await fetch('/api/consciousness/resume', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'X-CSRF-TOKEN': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
                            }
                        });
                        
                        const data = await response.json();
                        
                        if (data.success) {
                            this.statusMessage = '▶️ Myślenie Adam Clay zostało wznowione';
                            this.statusMessageType = 'success';
                            this.thinkingActive = true;
                            this.thinkingStatus = 'Aktywne przez dashboard';
                        } else {
                            this.statusMessage = '❌ Błąd: ' + data.message;
                            this.statusMessageType = 'error';
                        }
                    } catch (error) {
                        this.statusMessage = '❌ Błąd połączenia: ' + error.message;
                        this.statusMessageType = 'error';
                    } finally {
                        this.loading = false;
                        setTimeout(() => this.statusMessage = '', 5000);
                    }
                },
                
                // Live Thoughts Methods
                async fetchRecentThoughts() {
                    try {
                        const url = this.lastThoughtTimestamp 
                            ? `/api/thoughts/recent?since=${encodeURIComponent(this.lastThoughtTimestamp)}&limit=10`
                            : '/api/thoughts/recent?limit=10';
                            
                        const response = await fetch(url);
                        const data = await response.json();
                        
                        if (data.success) {
                            if (this.lastThoughtTimestamp) {
                                // Dodaj nowe myśli na początek
                                this.recentThoughts = [...data.thoughts, ...this.recentThoughts].slice(0, 10);
                            } else {
                                // Pierwszego ładowania - zastąp wszystko
                                this.recentThoughts = data.thoughts;
                            }
                            
                            // Aktualizuj timestamp ostatniej myśli
                            if (data.thoughts.length > 0) {
                                this.lastThoughtTimestamp = data.thoughts[0].timestamp;
                            }
                        }
                    } catch (error) {
                        console.error('Błąd pobierania myśli:', error);
                    }
                },
                
                async refreshThoughts() {
                    this.lastThoughtTimestamp = null; // Reset timestamp
                    await this.fetchRecentThoughts();
                },
                
                // Status display helpers
                getStatusIndicatorColor() {
                    if (this.blockingReason === 'email_question_blocking') {
                        return 'bg-red-500'; // Blocked by email - red
                    } else if (this.thinkingActive) {
                        return 'bg-green-500'; // Active thinking - green
                    } else {
                        return 'bg-orange-500'; // Paused by dashboard - orange
                    }
                },
                
                getStatusTextColor() {
                    if (this.blockingReason === 'email_question_blocking') {
                        return 'text-red-400';
                    } else if (this.thinkingActive) {
                        return 'text-green-400';
                    } else {
                        return 'text-orange-400';
                    }
                },
                
                getStatusText() {
                    if (this.blockingReason === 'email_question_blocking') {
                        return 'ZABLOKOWANE PRZEZ EMAIL';
                    } else if (this.thinkingActive) {
                        return 'MYŚLI AKTYWNIE';
                    } else {
                        return 'MYŚLENIE WSTRZYMANE';
                    }
                }
            }
        }
    </script>
</body>
</html> 