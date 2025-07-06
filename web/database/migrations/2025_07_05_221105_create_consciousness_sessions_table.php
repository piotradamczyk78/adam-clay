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
        Schema::create('consciousness_sessions', function (Blueprint $table) {
            $table->string('id', 100)->primary();
            $table->timestamp('started_at')->default(now());
            $table->timestamp('ended_at')->nullable();
            $table->integer('total_thoughts')->default(0);
            $table->decimal('total_cost', 10, 6)->default(0.000000);
            $table->string('final_mood', 50)->nullable();
            $table->decimal('final_energy', 3, 2)->nullable();
            $table->enum('status', ['active', 'paused', 'stopped'])->default('active');
            
            $table->index('started_at');
            $table->index('status');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('consciousness_sessions');
    }
};
