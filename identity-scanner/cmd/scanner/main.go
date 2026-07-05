package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"
	
	"github.com/natedadson/identity-security-platform/identity-scanner/internal/config"
	"github.com/natedadson/identity-security-platform/identity-scanner/internal/logger"
	"github.com/natedadson/identity-security-platform/identity-scanner/internal/scanner"
)

func main() {
	fmt.Println("🚀 Starting Identity Scanner...")
	
	// Load configuration
	cfg, err := config.LoadConfig()
	if err != nil {
		fmt.Printf("❌ Failed to load config: %v\n", err)
		os.Exit(1)
	}
	
	// Initialize logger
	logger := logger.NewLogger(cfg.LogLevel)
	
	// Create context for graceful shutdown
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()
	
	// Handle shutdown signals
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	
	go func() {
		<-sigChan
		fmt.Println("\n📴 Received shutdown signal, cleaning up...")
		cancel()
		time.Sleep(2 * time.Second)
		fmt.Println("✅ Cleanup complete")
		os.Exit(0)
	}()
	
	// Initialize scanner
	scanner := scanner.NewScanner(cfg, logger)
	
	// Start scanning
	logger.Info(ctx, "Starting identity scan...")
	
	// Run scan with worker pool
	if err := scanner.ScanWithWorkerPool(ctx); err != nil {
		logger.Error(ctx, "Scan failed", "error", err)
		os.Exit(1)
	}
	
	logger.Info(ctx, "Scan completed successfully!")
	fmt.Println("✅ Scanner finished successfully!")
	
	// Keep running until context is cancelled
	<-ctx.Done()
	fmt.Println("👋 Goodbye!")
}
