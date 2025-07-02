<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DashboardController;

// 🧪 Test route closure  
Route::get('/test-dashboard', function () {
    return view('dashboard');
});

// 🧪 Simple test
Route::get('/test', function () {
    return view('test');
});

// 🏠 Główny dashboard Adam Clay - multiple friendly URLs
Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard.main');
Route::get('/console', [DashboardController::class, 'index'])->name('dashboard.console');
Route::get('/monitor', [DashboardController::class, 'index'])->name('dashboard.monitor');
Route::get('/consciousness', [DashboardController::class, 'index'])->name('dashboard.consciousness');

// 📊 API endpoints dla dashboard (AJAX calls)
Route::prefix('dashboard')->group(function () {
    Route::get('/live-data', [DashboardController::class, 'liveData'])->name('dashboard.live-data');
    Route::get('/thoughts', [DashboardController::class, 'recentThoughts'])->name('dashboard.thoughts');
    Route::get('/stats', [DashboardController::class, 'stats'])->name('dashboard.stats');
});
