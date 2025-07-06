<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;
use Illuminate\Validation\Rule;
use App\Http\Controllers\Api\AdamClayApiController;
use App\Http\Controllers\Api\TestController;

/**
 * 🔌 API Routes dla komunikacji z Adam Clay Python backend
 * 
 * Wszystkie endpointy dostępne pod prefixem /api/
 */

// 🔍 Test endpoint (prosty closure)
Route::get('/test', function () {
    return 'DZIAŁA!';
});

// 🔍 Test endpoint (prosty closure)
Route::get('/hello', function () {
    return response()->json([
        'success' => true,
        'message' => 'Adam Clay Laravel API DZIAŁA!',
        'timestamp' => now(),
        'server' => 'Laravel',
        'version' => app()->version(),
        'database_status' => 'connected'
    ]);
});

// 💭 POST /api/thoughts - przyjmuje myśl z Adam Clay Python
Route::post('/thoughts', function (Request $request) {
    // Walidacja
    $validated = $request->validate([
        'timestamp' => 'required|date',
        'content' => 'required|string|max:10000',
        'thought_type' => ['required', Rule::in(['autonomous', 'reactive', 'business', 'philosophical'])],
        'cost_usd' => 'nullable|numeric|min:0',
        'mood' => ['nullable', Rule::in(['excited', 'focused', 'curious', 'concerned', 'optimistic', 'neutral'])],
        'energy_level' => 'nullable|numeric|between:0,1',
        'context' => 'nullable|array',
        'is_significant' => 'nullable|boolean',
        'session_id' => 'nullable|string|max:255'
    ]);
    
    try {
        // Konwersja timestamp do formatu MySQL
        $mysqlTimestamp = date('Y-m-d H:i:s', strtotime($validated['timestamp']));
        
        // Zapisanie do bazy myśli przez surowe SQL
        DB::table('thoughts')->insert([
            'timestamp' => $mysqlTimestamp,
            'content' => $validated['content'], 
            'thought_type' => $validated['thought_type'],
            'cost_usd' => $validated['cost_usd'] ?? 0,
            'mood' => $validated['mood'],
            'energy_level' => $validated['energy_level'],
            'context' => json_encode($validated['context'] ?? []),
            'is_significant' => $validated['is_significant'] ?? false,
            'session_id' => $validated['session_id']
        ]);
        
        // Log aktywności web
        DB::table('web_activity_log')->insert([
            'timestamp' => now(),
            'activity_type' => 'thought',
            'activity_title' => 'Nowa myśl',
            'activity_description' => Str::limit($validated['content'], 100),
            'activity_data' => json_encode([
                'type' => $validated['thought_type'],
                'mood' => $validated['mood'],
                'session_id' => $validated['session_id']
            ])
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Thought saved successfully'
        ], 201);
        
    } catch (\Exception $e) {
        return response()->json([
            'error' => 'Failed to save thought',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 📊 GET /api/status - status systemu Adam Clay
Route::get('/status', function () {
    try {
        // Aktualna sesja
        $currentSession = DB::table('consciousness_sessions')
            ->where('status', 'active')
            ->orderBy('started_at', 'desc')
            ->first();
            
        // Ostatnia myśl
        $lastThought = DB::table('thoughts')
            ->orderBy('timestamp', 'desc')
            ->first();
            
        // Statystyki dzisiejsze
        $todayThoughts = DB::table('thoughts')
            ->whereDate('timestamp', today())
            ->count();
            
        $todayCost = DB::table('thoughts')
            ->whereDate('timestamp', today())
            ->sum('cost_usd');
        
        return response()->json([
            'success' => true,
            'status' => [
                'current_session' => $currentSession ? [
                    'id' => $currentSession->id,
                    'started_at' => $currentSession->started_at,
                    'total_thoughts' => $currentSession->total_thoughts,
                    'total_cost' => $currentSession->total_cost
                ] : null,
                'last_thought' => $lastThought ? [
                    'id' => $lastThought->id,
                    'timestamp' => $lastThought->timestamp,
                    'type' => $lastThought->thought_type
                ] : null,
                'today_stats' => [
                    'thoughts' => $todayThoughts,
                    'cost' => round($todayCost, 4)
                ],
                'system_time' => now(),
                'database_status' => 'connected'
            ]
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to get status',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🧠 POST /api/sessions - tworzy nową sesję świadomości
Route::post('/sessions', function (Request $request) {
    $validated = $request->validate([
        'session_id' => 'required|string|max:255',
        'started_at' => 'required|date',
        'status' => 'nullable|string|max:50'
    ]);
    
    try {
        DB::table('consciousness_sessions')->insert([
            'id' => $validated['session_id'],
            'started_at' => date('Y-m-d H:i:s', strtotime($validated['started_at'])),
            'status' => $validated['status'] ?? 'active',
            'total_thoughts' => 0,
            'total_cost' => 0
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Consciousness session created',
            'session_id' => $validated['session_id']
        ], 201);
        
    } catch (\Exception $e) {
        return response()->json([
            'error' => 'Failed to create session',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 📊 PUT /api/sessions/{sessionId} - aktualizuje sesję
Route::put('/sessions/{sessionId}', function (Request $request, $sessionId) {
    $validated = $request->validate([
        'total_thoughts' => 'nullable|integer|min:0',
        'total_cost' => 'nullable|numeric|min:0',
        'status' => 'nullable|string|max:50'
    ]);
    
    try {
        $updateData = [];
        
        if (isset($validated['total_thoughts'])) {
            $updateData['total_thoughts'] = $validated['total_thoughts'];
        }
        if (isset($validated['total_cost'])) {
            $updateData['total_cost'] = $validated['total_cost'];
        }
        if (isset($validated['status'])) {
            $updateData['status'] = $validated['status'];
        }
        
        if (!empty($updateData)) {
            DB::table('consciousness_sessions')
                ->where('id', $sessionId)
                ->update($updateData);
        }
        
        return response()->json([
            'success' => true,
            'message' => 'Session updated successfully'
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'error' => 'Failed to update session',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🎯 POST /api/memories - zapisuje significant memory
Route::post('/memories', function (Request $request) {
    $validated = $request->validate([
        'memory_text' => 'required|string|max:1000',
        'category' => 'nullable|string|in:business,learning,insight,strategy,error,success,other',
        'timestamp' => 'required|date'
    ]);
    
    try {
        DB::table('significant_memories')->insert([
            'memory_date' => date('Y-m-d', strtotime($validated['timestamp'])),
            'memory_text' => $validated['memory_text'],
            'category' => $validated['category'] ?? 'other',
            'importance_score' => 0.8, // Default importance
            'created_at' => now()
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Significant memory saved'
        ], 201);
        
    } catch (\Exception $e) {
        return response()->json([
            'error' => 'Failed to save memory',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 📱 POST /api/activity - loguje aktywność web
Route::post('/activity', function (Request $request) {
    $validated = $request->validate([
        'activity_type' => 'required|string|in:thought,question_sent,question_answered,session_start,session_end,memory_created',
        'activity_title' => 'required|string|max:255',
        'activity_description' => 'nullable|string|max:1000',
        'activity_data' => 'nullable|array',
        'timestamp' => 'required|date'
    ]);
    
    try {
        DB::table('web_activity_log')->insert([
            'timestamp' => date('Y-m-d H:i:s', strtotime($validated['timestamp'])),
            'activity_type' => $validated['activity_type'],
            'activity_title' => $validated['activity_title'],
            'activity_description' => $validated['activity_description'],
            'activity_data' => json_encode($validated['activity_data'] ?? []),
            'is_displayed' => 1
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Activity logged successfully'
        ], 201);
        
    } catch (\Exception $e) {
        return response()->json([
            'error' => 'Failed to log activity',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 📧 POST /api/email-questions - zapisuje pytanie email z Python
Route::post('/email-questions', function (Request $request) {
    $validated = $request->validate([
        'id' => 'required|string|max:255',
        'content' => 'required|string|max:10000',
        'priority' => ['required', Rule::in(['CRITICAL', 'IMPORTANT', 'INFORMATIVE', 'OPTIMIZATION'])],
        'status' => 'nullable|string|in:pending,sent,answered,failed',
        'context' => 'nullable|array',
        'blocks_execution' => 'nullable|boolean',
        'created_at' => 'required|date'
    ]);
    
    try {
        // Sprawdź czy pytanie już istnieje
        $existing = DB::table('email_questions')->where('id', $validated['id'])->first();
        
        if ($existing) {
            return response()->json([
                'success' => false,
                'message' => 'Question with this ID already exists',
                'question_id' => $validated['id']
            ], 409);
        }
        
        // Zapisz pytanie do bazy
        DB::table('email_questions')->insert([
            'id' => $validated['id'],
            'content' => $validated['content'],
            'priority' => $validated['priority'],
            'status' => $validated['status'] ?? 'pending',
            'context' => json_encode($validated['context'] ?? []),
            'blocks_execution' => $validated['blocks_execution'] ?? false,
            'created_at' => date('Y-m-d H:i:s', strtotime($validated['created_at']))
        ]);
        
        // Log aktywności
        DB::table('web_activity_log')->insert([
            'timestamp' => now(),
            'activity_type' => 'question_sent',
            'activity_title' => 'Nowe pytanie email',
            'activity_description' => Str::limit($validated['content'], 100),
            'activity_data' => json_encode([
                'question_id' => $validated['id'],
                'priority' => $validated['priority'],
                'blocks_execution' => $validated['blocks_execution'] ?? false
            ])
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Email question saved successfully',
            'question_id' => $validated['id']
        ], 201);
        
    } catch (\Exception $e) {
        return response()->json([
            'error' => 'Failed to save email question',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🎮 POST /api/consciousness/start - uruchamia Adam Clay
Route::post('/consciousness/start', function () {
    // Zwiększ limit czasu wykonania
    set_time_limit(15);
    
    try {
        // Sprawdź czy już działa z timeout
        $pid = shell_exec("timeout 3 pgrep -f 'python3 main.py' 2>/dev/null");
        if ($pid) {
            return response()->json([
                'success' => false,
                'message' => 'Adam Clay consciousness is already running',
                'pid' => trim($pid)
            ], 400);
        }
        
        // 🆕 AUTOMATYCZNE TWORZENIE SESJI jeśli nie ma aktywnej
        $activeSession = DB::table('consciousness_sessions')
            ->whereIn('status', ['active', 'paused'])
            ->orderBy('started_at', 'desc')
            ->first();
            
        if (!$activeSession) {
            // Utwórz nową sesję automatycznie
            $newSessionId = 'session-' . date('Ymd-His') . '-' . substr(uniqid(), -4);
            
            DB::table('consciousness_sessions')->insert([
                'id' => $newSessionId,
                'started_at' => now(),
                'status' => 'active',
                'total_thoughts' => 0,
                'total_cost' => 0
            ]);
            
            // Log utworzenia sesji
            DB::table('web_activity_log')->insert([
                'timestamp' => now(),
                'activity_type' => 'session_start',
                'activity_title' => 'Auto-created consciousness session',
                'activity_description' => 'New session created automatically during consciousness start',
                'activity_data' => json_encode(['session_id' => $newSessionId, 'auto_created' => true]),
                'is_displayed' => 1
            ]);
        }
        
        // Uruchom consciousness w tle - użyj bezpośrednio python z venv
        $corePath = base_path('../core');
        $pythonPath = $corePath . '/adam_clay_env/bin/python3';
        $logPath = base_path('../data/logs/consciousness.log');
        
        $command = "cd '$corePath' && nohup '$pythonPath' main.py >> '$logPath' 2>&1 & echo $!";
        $newPid = shell_exec($command);
        
        if ($newPid) {
            // Log aktywności
            DB::table('web_activity_log')->insert([
                'timestamp' => now(),
                'activity_type' => 'session_start',
                'activity_title' => 'Adam Clay consciousness started',
                'activity_description' => 'Consciousness started from web dashboard',
                'activity_data' => json_encode(['pid' => trim($newPid)]),
                'is_displayed' => 1
            ]);
            
            return response()->json([
                'success' => true,
                'message' => 'Adam Clay consciousness started successfully',
                'pid' => trim($newPid),
                'session_created' => !$activeSession
            ]);
        } else {
            return response()->json([
                'success' => false,
                'message' => 'Failed to start Adam Clay consciousness'
            ], 500);
        }
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to start consciousness',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🛑 POST /api/consciousness/stop - zatrzymuje Adam Clay  
Route::post('/consciousness/stop', function () {
    // Zwiększ limit czasu wykonania
    set_time_limit(10);
    
    try {
        // Znajdź PID z timeout
        $pid = shell_exec("timeout 3 pgrep -f 'python3 main.py' 2>/dev/null");
        
        if (!$pid) {
            return response()->json([
                'success' => false,
                'message' => 'Adam Clay consciousness is not running'
            ], 400);
        }
        
        // Zatrzymaj proces z timeout
        $result = shell_exec("timeout 5 pkill -f 'python3 main.py' 2>/dev/null");
        
        // Log aktywności
        DB::table('web_activity_log')->insert([
            'timestamp' => now(),
            'activity_type' => 'session_end',
            'activity_title' => 'Adam Clay consciousness stopped',
            'activity_description' => 'Consciousness stopped from web dashboard', 
            'activity_data' => json_encode(['previous_pid' => trim($pid)]),
            'is_displayed' => 1
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Adam Clay consciousness stopped successfully',
            'previous_pid' => trim($pid)
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to stop consciousness',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🔍 GET /api/consciousness/status - status procesu consciousness
Route::get('/consciousness/status', function () {
    // Zwiększ limit czasu wykonania
    set_time_limit(10);
    
    try {
        // Użyj timeout dla shell_exec
        $pid = shell_exec("timeout 3 pgrep -f 'python3 main.py' 2>/dev/null");
        $isRunning = !empty(trim($pid));
        
        $status = [
            'is_running' => $isRunning,
            'pid' => $isRunning ? trim($pid) : null,
            'uptime' => null,
            'last_log_line' => null
        ];
        
        if ($isRunning) {
            // Sprawdź uptime procesu z timeout
            $uptimeCmd = "timeout 2 ps -o etime= -p " . trim($pid) . " 2>/dev/null | xargs";
            $uptime = shell_exec($uptimeCmd);
            $status['uptime'] = trim($uptime) ?: null;
            
            // Ostatnia linia z logu z timeout
            $logPath = base_path('../data/logs/consciousness.log');
            if (file_exists($logPath)) {
                $lastLine = shell_exec("timeout 2 tail -1 '$logPath' 2>/dev/null");
                $status['last_log_line'] = trim($lastLine) ?: null;
            }
        }
        
        return response()->json([
            'success' => true,
            'consciousness' => $status
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to get consciousness status',
            'message' => $e->getMessage()
        ], 500);
    }
});

// ⏸️ POST /api/consciousness/pause - zawiesza myślenie Adam Clay
Route::post('/consciousness/pause', function () {
    try {
        // Znajdź aktywną sesję
        $activeSession = DB::table('consciousness_sessions')
            ->where('status', 'active')
            ->orderBy('started_at', 'desc')
            ->first();
            
        if (!$activeSession) {
            return response()->json([
                'success' => false,
                'message' => 'Brak aktywnej sesji do wstrzymania'
            ], 400);
        }
        
        // Zmień status na 'paused'
        DB::table('consciousness_sessions')
            ->where('id', $activeSession->id)
            ->update(['status' => 'paused']);
            
        // Log aktywności
        DB::table('web_activity_log')->insert([
            'timestamp' => now(),
            'activity_type' => 'session_end',
            'activity_title' => 'Adam Clay thinking paused',
            'activity_description' => 'Consciousness thinking paused from web dashboard',
            'activity_data' => json_encode(['session_id' => $activeSession->id, 'action' => 'pause']),
            'is_displayed' => 1
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Adam Clay thinking paused successfully',
            'session_id' => $activeSession->id,
            'action' => 'paused'
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to pause consciousness',
            'message' => $e->getMessage()
        ], 500);
    }
});

// ▶️ POST /api/consciousness/resume - wznawia myślenie Adam Clay
Route::post('/consciousness/resume', function () {
    try {
        // Znajdź wstrzymaną sesję
        $pausedSession = DB::table('consciousness_sessions')
            ->where('status', 'paused')
            ->orderBy('started_at', 'desc')
            ->first();
            
        if (!$pausedSession) {
            return response()->json([
                'success' => false,
                'message' => 'Brak wstrzymanej sesji do wznowienia'
            ], 400);
        }
        
        // Zmień status z powrotem na 'active'
        DB::table('consciousness_sessions')
            ->where('id', $pausedSession->id)
            ->update(['status' => 'active']);
            
        // Log aktywności
        DB::table('web_activity_log')->insert([
            'timestamp' => now(),
            'activity_type' => 'session_start',
            'activity_title' => 'Adam Clay thinking resumed',
            'activity_description' => 'Consciousness thinking resumed from web dashboard',
            'activity_data' => json_encode(['session_id' => $pausedSession->id, 'action' => 'resume']),
            'is_displayed' => 1
        ]);
        
        return response()->json([
            'success' => true,
            'message' => 'Adam Clay thinking resumed successfully',
            'session_id' => $pausedSession->id,
            'action' => 'resumed'
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to resume consciousness',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🔍 GET /api/consciousness/thinking-status - status myślenia (uwzględnia bazę + email blocking)
Route::get('/consciousness/thinking-status', function () {
    try {
        // Odczytaj konfigurację Adam Clay
        $configPath = base_path('../core/config.json');
        $blockingConfig = null;
        
        if (file_exists($configPath)) {
            $config = json_decode(file_get_contents($configPath), true);
            $blockingConfig = $config['communication']['email']['blocking_questions'] ?? null;
        }
        
        // Domyślne wartości jeśli brak konfiguracji
        $blockingEnabled = $blockingConfig['enabled'] ?? true;
        $blockOnPriorities = $blockingConfig['block_on_priorities'] ?? ['CRITICAL'];
        $blockAllQuestions = $blockingConfig['block_all_questions'] ?? false;
        
        // Sprawdź status aktualnej sesji w bazie
        $currentSession = DB::table('consciousness_sessions')
            ->whereIn('status', ['active', 'paused'])
            ->orderBy('started_at', 'desc')
            ->first();
            
        if (!$currentSession) {
            // 🔍 Sprawdź czy proces consciousness działa (może być w fazie startowania)
            $pid = shell_exec("pgrep -f 'python3 main.py'");
            $isProcessRunning = !empty(trim($pid));
            
            if ($isProcessRunning) {
                // Proces działa ale nie ma sesji - prawdopodobnie się właśnie uruchamia
                return response()->json([
                    'success' => true,
                    'thinking_status' => [
                        'is_thinking' => true,
                        'session_status' => 'starting',
                        'message' => 'Adam Clay się uruchamia - sesja zostanie utworzona wkrótce',
                        'blocking_reason' => null,
                        'process_pid' => trim($pid)
                    ]
                ]);
            } else {
                // Ani proces ani sesja - system zatrzymany
                return response()->json([
                    'success' => true,
                    'thinking_status' => [
                        'is_thinking' => false,
                        'session_status' => 'stopped',
                        'message' => 'Adam Clay nie jest uruchomiony',
                        'blocking_reason' => null,
                        'help_message' => 'Kliknij "Start" aby uruchomić consciousness'
                    ]
                ]);
            }
        }
        
        // Sprawdź czy jest zablokowany przez email question - użyj konfiguracji
        $blockingQuestionQuery = DB::table('email_questions')
            ->whereIn('status', ['pending', 'sent'])  // Sprawdź zarówno pending jak i sent
            ->where('blocks_execution', true)
            ->whereNull('answered_at')  // Tylko nieudzielone odpowiedzi
            ->orderBy('created_at', 'desc');
            
        // Jeśli nie blokuje wszystkich pytań, filtruj po priorytetach z konfiguracji
        if (!$blockAllQuestions && $blockingEnabled) {
            $blockingQuestionQuery->whereIn('priority', $blockOnPriorities);
        }
        
        $blockingQuestion = $blockingQuestionQuery->first();
        
        // Determine final thinking status
        $isThinking = true;
        $sessionStatus = $currentSession->status;
        $message = 'Adam Clay myśli aktywnie';
        $blockingReason = null;
        
        if ($blockingQuestion && $blockingEnabled) {
            // Blocked by email question based on configuration
            $isThinking = false;
            $sessionStatus = 'blocked_by_email';
            $priority = $blockingQuestion->priority;
            $message = "Myślenie zablokowane przez pytanie email ({$priority})";
            $blockingReason = 'email_question_blocking';
        } elseif ($currentSession->status === 'paused') {
            // Paused via dashboard
            $isThinking = false;
            $sessionStatus = 'paused';
            $message = 'Myślenie wstrzymane przez dashboard';
            $blockingReason = 'web_dashboard_pause';
        }
        
        return response()->json([
            'success' => true,
            'thinking_status' => [
                'is_thinking' => $isThinking,
                'session_status' => $sessionStatus,
                'session_id' => $currentSession->id,
                'started_at' => $currentSession->started_at,
                'total_thoughts' => $currentSession->total_thoughts,
                'message' => $message,
                'blocking_reason' => $blockingReason,
                'blocking_question' => $blockingQuestion ? [
                    'id' => $blockingQuestion->id,
                    'content' => substr($blockingQuestion->content, 0, 100) . '...',
                    'priority' => $blockingQuestion->priority,
                    'created_at' => $blockingQuestion->created_at
                ] : null,
                'blocking_config' => [
                    'enabled' => $blockingEnabled,
                    'block_on_priorities' => $blockOnPriorities,
                    'block_all_questions' => $blockAllQuestions
                ]
            ]
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to get thinking status',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 💭 GET /api/thoughts/recent - najnowsze myśli (live feed)
Route::get('/thoughts/recent', function (Request $request) {
    try {
        $limit = $request->get('limit', 10);
        $since = $request->get('since'); // timestamp - pobierz myśli od tego czasu
        
        $query = DB::table('thoughts')
            ->select('id', 'timestamp', 'content', 'thought_type', 'cost_usd', 'mood', 'energy_level', 'session_id')
            ->orderBy('timestamp', 'desc')
            ->limit($limit);
            
        if ($since) {
            $query->where('timestamp', '>', $since);
        }
        
        $thoughts = $query->get();
        
        return response()->json([
            'success' => true,
            'thoughts' => $thoughts,
            'count' => count($thoughts),
            'server_time' => now()
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to get recent thoughts',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 📚 GET /api/thoughts/history - historia myśli z podziałem na daty
Route::get('/thoughts/history', function (Request $request) {
    try {
        $date = $request->get('date'); // format: Y-m-d
        $page = max(1, $request->get('page', 1));
        $perPage = min(50, max(5, $request->get('per_page', 20)));
        
        // Jeśli brak daty, pokaż dostępne daty
        if (!$date) {
            $availableDates = DB::table('thoughts')
                ->selectRaw('DATE(timestamp) as date, COUNT(*) as count, SUM(cost_usd) as total_cost')
                ->groupByRaw('DATE(timestamp)')
                ->orderByRaw('DATE(timestamp) DESC')
                ->get();
                
            return response()->json([
                'success' => true,
                'available_dates' => $availableDates
            ]);
        }
        
        // Pobierz myśli z konkretnej daty
        $offset = ($page - 1) * $perPage;
        
        $thoughts = DB::table('thoughts')
            ->select('id', 'timestamp', 'content', 'thought_type', 'cost_usd', 'mood', 'energy_level', 'session_id')
            ->whereDate('timestamp', $date)
            ->orderBy('timestamp', 'desc')
            ->offset($offset)
            ->limit($perPage)
            ->get();
            
        $totalCount = DB::table('thoughts')->whereDate('timestamp', $date)->count();
        $totalPages = ceil($totalCount / $perPage);
        
        // Statystyki dnia
        $dayStats = DB::table('thoughts')
            ->selectRaw('COUNT(*) as total_thoughts, SUM(cost_usd) as total_cost, AVG(energy_level) as avg_energy')
            ->whereDate('timestamp', $date)
            ->first();
        
        return response()->json([
            'success' => true,
            'date' => $date,
            'thoughts' => $thoughts,
            'pagination' => [
                'current_page' => $page,
                'per_page' => $perPage,
                'total' => $totalCount,
                'total_pages' => $totalPages,
                'has_next' => $page < $totalPages,
                'has_prev' => $page > 1
            ],
            'day_stats' => $dayStats
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to get thoughts history',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🧠 POST /api/memories/significant - zapisuje znaczące wspomnienie  
Route::post('/memories/significant', function (Request $request) {
    $validated = $request->validate([
        'memory_text' => 'required|string|max:2000',
        'memory_date' => 'required|date',
        'category' => ['required', Rule::in(['business', 'learning', 'insight', 'strategy', 'error', 'success', 'other'])],
        'importance_score' => 'required|numeric|between:0,9.99',
        'related_thought_id' => 'nullable|integer'
    ]);
    
    try {
        $memoryId = DB::table('significant_memories')->insertGetId([
            'memory_text' => $validated['memory_text'],
            'memory_date' => $validated['memory_date'],
            'category' => $validated['category'],
            'importance_score' => $validated['importance_score'],
            'related_thought_id' => $validated['related_thought_id'],
            'created_at' => now()
        ]);
        
        return response()->json([
            'success' => true,
            'memory_id' => $memoryId,
            'message' => 'Significant memory saved'
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to save memory',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🧠 GET /api/memories/significant - pobiera znaczące wspomnienia
Route::get('/memories/significant', function (Request $request) {
    $limit = min(50, max(1, $request->get('limit', 20)));
    $category = $request->get('category');
    $minImportance = $request->get('min_importance', 0);
    
    try {
        $query = DB::table('significant_memories')
            ->select('id', 'memory_text', 'memory_date', 'category', 'importance_score', 'created_at')
            ->where('importance_score', '>=', $minImportance)
            ->orderBy('importance_score', 'desc')
            ->orderBy('created_at', 'desc')
            ->limit($limit);
            
        if ($category) {
            $query->where('category', $category);
        }
        
        $memories = $query->get();
        
        return response()->json([
            'success' => true,
            'memories' => $memories,
            'count' => count($memories)
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to get memories',
            'message' => $e->getMessage()
        ], 500);
    }
});

// 🧠 POST /api/patterns/learned - zapisuje nauczony wzorzec
Route::post('/patterns/learned', function (Request $request) {
    $validated = $request->validate([
        'pattern_name' => 'required|string|max:200',
        'pattern_data' => 'required|array',
        'pattern_type' => ['required', Rule::in(['behavioral', 'cost_optimization', 'communication', 'business', 'other'])],
        'confidence_score' => 'required|numeric|between:0,9.99'
    ]);
    
    try {
        $patternId = DB::table('learned_patterns')->insertGetId([
            'pattern_name' => $validated['pattern_name'],
            'pattern_data' => json_encode($validated['pattern_data']),
            'pattern_type' => $validated['pattern_type'],
            'confidence_score' => $validated['confidence_score'],
            'usage_count' => 0,
            'created_at' => now(),
            'updated_at' => now()
        ]);
        
        return response()->json([
            'success' => true,
            'pattern_id' => $patternId,
            'message' => 'Learned pattern saved'
        ]);
        
    } catch (\Exception $e) {
        return response()->json([
            'success' => false,
            'error' => 'Failed to save pattern',
            'message' => $e->getMessage()
        ], 500);
    }
});

/**
 * ✅ KOMPLETNE API ENDPOINTY:
 * 
 * GET  /api/hello                    - test połączenia
 * GET  /api/status                   - status systemu Adam Clay
 * POST /api/thoughts                 - zapisz nową myśl
 * POST /api/sessions                 - tworzy sesję świadomości
 * PUT  /api/sessions/{id}            - aktualizuje sesję  
 * POST /api/memories                 - zapisz significant memory
 * POST /api/activity                 - log aktywności web
 * 
 * 🎮 CONSCIOUSNESS CONTROL:
 * POST /api/consciousness/start      - uruchamia Adam Clay process
 * POST /api/consciousness/stop       - zatrzymuje Adam Clay process
 * GET  /api/consciousness/status     - status procesu consciousness
 * 
 * 🧠 THINKING CONTROL:
 * POST /api/consciousness/pause      - zawiesza myślenie (przez bazę)
 * POST /api/consciousness/resume     - wznawia myślenie (przez bazę)
 * GET  /api/consciousness/thinking-status - status myślenia (nie procesu)
 * 
 * 💭 THOUGHTS DATA:
 * GET  /api/thoughts/recent          - najnowsze myśli (live feed)
 * GET  /api/thoughts/history         - historia myśli z podziałem na daty
 */ 