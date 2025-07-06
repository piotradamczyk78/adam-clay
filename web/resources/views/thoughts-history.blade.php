<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📚 Adam Clay - Historia Myśli</title>
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
</head>
<body class="bg-gradient-to-br from-gray-900 via-blue-900 to-purple-900 min-h-screen">
    <div class="container mx-auto p-6" x-data="thoughtsHistory()" x-init="init()">
        
        <!-- Header -->
        <header class="text-center mb-8">
            <h1 class="text-5xl font-bold text-white mb-2">
                📚 <span class="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">Adam Clay</span>
            </h1>
            <p class="text-gray-300 text-lg">Historia Myśli AI</p>
            <div class="mt-4 flex justify-center items-center space-x-4">
                <a href="/dashboard" class="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg text-white transition-colors">
                    🏠 Dashboard
                </a>
                <span class="text-gray-400" x-text="currentTime"></span>
            </div>
        </header>

        <!-- Wybór daty -->
        <div class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-8">
            <h2 class="text-xl font-bold text-white mb-4">📅 Wybierz datę</h2>
            
            <!-- Loading state -->
            <div x-show="loading" class="text-center py-4">
                <div class="inline-flex items-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span class="text-white">Ładowanie...</span>
                </div>
            </div>
            
            <!-- Available dates -->
            <div x-show="!loading && availableDates.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <template x-for="dateInfo in availableDates" :key="dateInfo.date">
                    <button @click="selectDate(dateInfo.date)"
                            :class="selectedDate === dateInfo.date ? 'bg-blue-600/30 border-blue-400' : 'bg-black/20 border-white/10 hover:border-white/20'"
                            class="p-4 rounded-lg border transition-all duration-200 text-left">
                        <div class="text-white font-semibold" x-text="formatDatePL(dateInfo.date)"></div>
                        <div class="text-gray-300 text-sm mt-1">
                            💭 <span x-text="dateInfo.count"></span> myśli
                        </div>
                        <div class="text-gray-400 text-xs">
                            💰 $<span x-text="(dateInfo.total_cost || 0).toFixed(4)"></span>
                        </div>
                    </button>
                </template>
            </div>
            
            <div x-show="!loading && availableDates.length === 0" class="text-center py-8 text-gray-400">
                <div class="text-4xl mb-2">📚</div>
                <div>Brak dostępnych dat</div>
                <div class="text-sm">Adam Clay jeszcze nie tworzył myśli</div>
            </div>
        </div>

        <!-- Statystyki dnia -->
        <div x-show="selectedDate && dayStats" class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-8">
            <h2 class="text-xl font-bold text-white mb-4">
                📊 Statystyki - <span x-text="formatDatePL(selectedDate)"></span>
            </h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="text-center">
                    <div class="text-3xl font-bold text-blue-400" x-text="dayStats?.total_thoughts || 0"></div>
                    <div class="text-gray-300">Łączne myśli</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-green-400">$<span x-text="(dayStats?.total_cost || 0).toFixed(4)"></span></div>
                    <div class="text-gray-300">Łączny koszt</div>
                </div>
                <div class="text-center">
                    <div class="text-3xl font-bold text-yellow-400" x-text="dayStats?.avg_energy ? Math.round(dayStats.avg_energy * 100) + '%' : '-'"></div>
                    <div class="text-gray-300">Średnia energia</div>
                </div>
            </div>
        </div>

        <!-- Myśli -->
        <div x-show="selectedDate" class="bg-white/10 backdrop-blur-lg rounded-xl p-6 border border-white/20 mb-8">
            <div class="flex justify-between items-center mb-4">
                <h2 class="text-xl font-bold text-white">
                    💭 Myśli z <span x-text="formatDatePL(selectedDate)"></span>
                </h2>
            </div>
            
            <!-- Loading thoughts -->
            <div x-show="loadingThoughts" class="text-center py-8">
                <div class="inline-flex items-center">
                    <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span class="text-white">Ładowanie myśli...</span>
                </div>
            </div>
            
            <!-- Thoughts list -->
            <div x-show="!loadingThoughts" class="space-y-4 max-h-96 overflow-y-auto">
                <template x-for="thought in thoughts" :key="thought.id">
                    <div class="bg-black/20 rounded-lg p-5 border border-white/10 hover:border-white/20 transition-all duration-200">
                        <div class="flex justify-between items-start mb-3">
                            <div class="flex items-center gap-2 flex-wrap">
                                <span class="inline-block px-3 py-1 text-xs font-semibold rounded-full"
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
                                <div x-text="formatTime(thought.timestamp)"></div>
                                <div class="text-xs">$<span x-text="(thought.cost_usd || 0).toFixed(4)"></span></div>
                            </div>
                        </div>
                        
                        <div class="text-white text-sm leading-relaxed mb-3" x-text="thought.content"></div>
                        
                        <div class="flex justify-between items-center text-xs text-gray-400">
                            <span>ID: <span x-text="thought.id"></span></span>
                            <div class="flex items-center gap-3">
                                <span x-show="thought.energy_level" class="flex items-center">
                                    ⚡ <span x-text="Math.round(thought.energy_level * 100)"></span>%
                                </span>
                                <span x-show="thought.session_id" class="font-mono text-xs" x-text="thought.session_id"></span>
                            </div>
                        </div>
                    </div>
                </template>
                
                <div x-show="thoughts.length === 0 && !loadingThoughts" class="text-center py-8 text-gray-400">
                    <div class="text-4xl mb-2">💭</div>
                    <div>Brak myśli na ten dzień</div>
                    <div class="text-sm">Adam Clay nie miał myśli w wybranym dniu</div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="text-center text-gray-400 mt-8">
            <p>🧠 Adam Clay History • Laravel {{ app()->version() }} • REST API</p>
            <p class="text-sm mt-2">Historia myśli autonomicznej AI</p>
        </footer>
    </div>

    <script>
        function thoughtsHistory() {
            return {
                // State
                availableDates: [],
                selectedDate: null,
                thoughts: [],
                dayStats: null,
                loading: false,
                loadingThoughts: false,
                currentTime: '',
                
                init() {
                    this.updateTime();
                    this.fetchAvailableDates();
                    setInterval(() => this.updateTime(), 1000);
                },
                
                updateTime() {
                    this.currentTime = new Date().toLocaleTimeString('pl-PL');
                },
                
                async fetchAvailableDates() {
                    this.loading = true;
                    try {
                        const response = await fetch('/api/thoughts/history');
                        const data = await response.json();
                        
                        if (data.success) {
                            this.availableDates = data.available_dates;
                        }
                    } catch (error) {
                        console.error('Błąd pobierania dat:', error);
                    } finally {
                        this.loading = false;
                    }
                },
                
                async selectDate(date) {
                    this.selectedDate = date;
                    this.loadingThoughts = true;
                    
                    try {
                        const response = await fetch(`/api/thoughts/history?date=${date}&per_page=100`);
                        const data = await response.json();
                        
                        if (data.success) {
                            this.thoughts = data.thoughts;
                            this.dayStats = data.day_stats;
                        }
                    } catch (error) {
                        console.error('Błąd pobierania myśli:', error);
                    } finally {
                        this.loadingThoughts = false;
                    }
                },
                
                formatDatePL(dateString) {
                    if (!dateString) return '-';
                    const date = new Date(dateString);
                    return date.toLocaleDateString('pl-PL', { 
                        weekday: 'long', 
                        year: 'numeric', 
                        month: 'long', 
                        day: 'numeric' 
                    });
                },
                
                formatTime(timestamp) {
                    if (!timestamp) return '-';
                    return new Date(timestamp).toLocaleTimeString('pl-PL');
                }
            }
        }
    </script>
</body>
</html> 