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

/**
 * ✅ KOMPLETNE API ENDPOINTY:
 * 
 * GET  /api/hello      - test połączenia
 * GET  /api/status     - status systemu Adam Clay
 * POST /api/thoughts   - zapisz nową myśl
 * POST /api/sessions   - tworzy sesję świadomości
 * PUT  /api/sessions/{id} - aktualizuje sesję  
 * POST /api/memories   - zapisz significant memory
 * POST /api/activity   - log aktywności web
 */ 