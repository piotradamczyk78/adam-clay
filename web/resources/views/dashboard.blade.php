<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🧠 Adam Clay - Live Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <meta http-equiv="refresh" content="30">
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
                
                init() {
                    this.updateTime();
                    this.fetchData();
                    setInterval(() => this.updateTime(), 1000);
                    setInterval(() => this.fetchData(), 10000); // Refresh co 10s
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
                }
            }
        }
    </script>
</body>
</html> 