"""Configuration settings for the BQ vs Databricks Debate App."""
import os

# Model configuration
DEFAULT_MODEL = os.getenv("DEBATE_MODEL", "gemini-3.7-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Server configuration
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# Debate engine defaults
DEFAULT_ROUNDS = 2
MAX_ROUNDS = 4

# Financial & Infrastructure Benchmark Constants
DEFAULT_DBU_PRICE_USD = 0.40          # Blended enterprise DBU rate
DEFAULT_VM_INFRA_MARKUP = 1.35        # Hyperscaler VM/Compute cost multiplier (~35% of DBU spend)
AVERAGE_ALL_PURPOSE_IDLE_PCT = 0.35   # Standard idle time on interactive clusters
DELTA_MAINTENANCE_TAX_RATIO = 0.18    # Typical spend proportion on OPTIMIZE/VACUUM/ZORDER
ESTIMATED_BIGQUERY_SAVINGS_PCT = 0.45 # Expected TCO savings with BigQuery Editions + Spend CUDs
ENGINEER_HOURLY_RATE_USD = 175.0      # Senior Data Engineer / Consultant hourly billing rate
STORAGE_WRITE_API_GB_COST = 0.025     # BigQuery Storage Write API cost per GB
BI_ENGINE_RAM_GB_MONTHLY_COST = 30.36 # BigQuery BI Engine RAM cost per GB/month
