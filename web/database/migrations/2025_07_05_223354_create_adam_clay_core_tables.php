<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        // 💭 TABELA: thoughts - wszystkie myśli Adam Clay
        Schema::create('thoughts', function (Blueprint $table) {
            $table->id();
            $table->dateTime('timestamp');
            $table->text('content');
            $table->enum('thought_type', ['autonomous', 'reactive', 'business', 'philosophical']);
            $table->decimal('cost_usd', 10, 6)->default(0.000000);
            $table->string('mood', 50)->nullable();
            $table->decimal('energy_level', 3, 2)->nullable();
            $table->json('context')->nullable();
            $table->boolean('is_significant')->default(false);
            $table->string('session_id', 100)->nullable();
            $table->timestamp('created_at')->default(now());
            
            $table->index('timestamp');
            $table->index('thought_type');
            $table->index('is_significant');
            $table->index('session_id');
        });

        // 📧 TABELA: email_questions - pytania do użytkownika
        Schema::create('email_questions', function (Blueprint $table) {
            $table->string('id', 100)->primary();
            $table->text('content');
            $table->enum('priority', ['CRITICAL', 'IMPORTANT', 'INFORMATIVE', 'OPTIMIZATION']);
            $table->enum('status', ['pending', 'sent', 'answered', 'failed'])->default('pending');
            $table->json('context')->nullable();
            $table->timestamp('created_at')->default(now());
            $table->timestamp('sent_at')->nullable();
            $table->timestamp('answered_at')->nullable();
            $table->text('response')->nullable();
            $table->boolean('blocks_execution')->default(false);
            
            $table->index('priority');
            $table->index('status');
            $table->index('blocks_execution');
        });

        // 💬 TABELA: user_questions - pytania od użytkownika
        Schema::create('user_questions', function (Blueprint $table) {
            $table->string('id', 100)->primary();
            $table->text('content');
            $table->json('context')->nullable();
            $table->enum('status', ['pending', 'processing', 'answered', 'needs_thinking'])->default('pending');
            $table->text('answer')->nullable();
            $table->boolean('needs_more_thinking')->default(false);
            $table->timestamp('created_at')->default(now());
            $table->timestamp('answered_at')->nullable();
            $table->decimal('cost_usd', 10, 6)->default(0.000000);
            
            $table->index('status');
            $table->index('created_at');
        });

        // 🎯 TABELA: significant_memories - ważne wspomnienia
        Schema::create('significant_memories', function (Blueprint $table) {
            $table->id();
            $table->text('memory_text');
            $table->date('memory_date');
            $table->enum('category', ['business', 'learning', 'insight', 'strategy', 'error', 'success', 'other'])->default('other');
            $table->decimal('importance_score', 3, 2)->default(1.00);
            $table->unsignedBigInteger('related_thought_id')->nullable();
            $table->timestamp('created_at')->default(now());
            
            $table->foreign('related_thought_id')->references('id')->on('thoughts')->onDelete('set null');
            $table->index('memory_date');
            $table->index('category');
            $table->index('importance_score');
        });

        // 📊 TABELA: system_stats - statystyki systemu
        Schema::create('system_stats', function (Blueprint $table) {
            $table->id();
            $table->date('stat_date')->unique();
            $table->integer('total_thoughts_today')->default(0);
            $table->decimal('total_cost_today', 10, 6)->default(0.000000);
            $table->integer('significant_memories_created')->default(0);
            $table->integer('questions_asked')->default(0);
            $table->integer('questions_answered')->default(0);
            $table->string('average_mood', 50)->nullable();
            $table->decimal('average_energy', 3, 2)->nullable();
            $table->decimal('uptime_hours', 5, 2)->default(0.00);
            $table->timestamp('created_at')->default(now());
            $table->timestamp('updated_at')->default(now());
            
            $table->index('stat_date');
        });

        // 📝 TABELA: learned_patterns - wzorce i doświadczenia
        Schema::create('learned_patterns', function (Blueprint $table) {
            $table->id();
            $table->string('pattern_name', 200)->unique();
            $table->json('pattern_data');
            $table->enum('pattern_type', ['behavioral', 'cost_optimization', 'communication', 'business', 'other'])->default('other');
            $table->decimal('confidence_score', 3, 2)->default(1.00);
            $table->integer('usage_count')->default(0);
            $table->timestamp('last_used_at')->nullable();
            $table->timestamp('created_at')->default(now());
            $table->timestamp('updated_at')->default(now());
            
            $table->index('pattern_type');
            $table->index('confidence_score');
        });

        // 📱 TABELA: web_activity_log - aktywność dla strony web
        Schema::create('web_activity_log', function (Blueprint $table) {
            $table->id();
            $table->enum('activity_type', ['thought', 'question_sent', 'question_answered', 'session_start', 'session_end', 'memory_created']);
            $table->string('activity_title', 255);
            $table->text('activity_description')->nullable();
            $table->json('activity_data')->nullable();
            $table->timestamp('timestamp')->default(now());
            $table->boolean('is_displayed')->default(true);
            
            $table->index('timestamp');
            $table->index('activity_type');
            $table->index('is_displayed');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('web_activity_log');
        Schema::dropIfExists('learned_patterns');
        Schema::dropIfExists('system_stats');
        Schema::dropIfExists('significant_memories');
        Schema::dropIfExists('user_questions');
        Schema::dropIfExists('email_questions');
        Schema::dropIfExists('thoughts');
    }
};
