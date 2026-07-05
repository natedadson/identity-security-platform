package main

import (
	"context"
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	fmt.Println("🚀 Starting Identity Scanner (Standalone)...")
	fmt.Println("ℹ️  This is a demo version with mock data")

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		<-sigChan
		fmt.Println("\n📴 Shutting down...")
		cancel()
		os.Exit(0)
	}()

	// Simulate scanning
	fmt.Println("\n📊 Simulating identity scan...")
	users := []string{
		"admin-user",
		"developer-1",
		"service-account-prod",
		"readonly-user",
		"service-account-dev",
		"manager-user",
		"api-user",
		"audit-user",
		"deploy-user",
		"monitoring-user",
	}

	results := map[string]string{
		"admin-user":            "HIGH - Admin privileges",
		"service-account-prod":  "HIGH - Never used, active keys",
		"developer-1":           "MEDIUM - 15 permissions",
		"service-account-dev":   "MEDIUM - 10 permissions",
		"readonly-user":         "LOW - Read only access",
		"manager-user":          "MEDIUM - 8 permissions",
		"api-user":              "LOW - API only access",
		"audit-user":            "LOW - Audit logs only",
		"deploy-user":           "MEDIUM - Deployment permissions",
		"monitoring-user":       "LOW - Monitoring only",
	}

	for i, user := range users {
		select {
		case <-ctx.Done():
			fmt.Println("\n👋 Goodbye!")
			return
		default:
			time.Sleep(500 * time.Millisecond)
			risk := results[user]
			emoji := "🟢"
			if risk[:4] == "HIGH" {
				emoji = "🔴"
			} else if risk[:6] == "MEDIUM" {
				emoji = "🟡"
			}
			fmt.Printf("[%d/10] %s %s - %s\n", i+1, emoji, user, risk)
		}
	}

	fmt.Println("\n✅ Scan completed!")
	fmt.Println("\n📊 Summary:")
	fmt.Println("  🔴 High Risk: 2 identities")
	fmt.Println("  🟡 Medium Risk: 4 identities")
	fmt.Println("  🟢 Low Risk: 4 identities")
	fmt.Println("\n📝 Recommendations:")
	fmt.Println("  1. Remove unused permissions from admin-user")
	fmt.Println("  2. Disable inactive service-account-prod")
	fmt.Println("  3. Enable MFA on all accounts")
	fmt.Println("\n👋 Press Ctrl+C to exit")

	<-ctx.Done()
	fmt.Println("👋 Goodbye!")
}
