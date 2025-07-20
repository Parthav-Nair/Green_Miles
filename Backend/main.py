from fastapi import FastAPI
from Backend.routes import predict_hv # Always import HV router as it's the current focus
import logging # Import logging module for warnings/errors

# Setup basic logging if not already configured by main script (e.g., in evaluate_models.py)
if not logging.getLogger().handlers:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# Conditionally import EV router
ev_router_available = False
try:
    from Backend.routes import predict_ev
    ev_router_available = True
    logging.info("EV router found and will be included.")
except ImportError as e:
    logging.warning(f"EV router not found or has import issues ({e}). EV endpoint will not be available.")
except Exception as e:
    logging.error(f"An unexpected error occurred while trying to import EV router: {e}. EV endpoint will not be available.")


app = FastAPI(
    title="EV + HV Range Predictor",
    version="2.0"
)

# Always include HV router
app.include_router(predict_hv.router)

# Conditionally include EV router only if its imports were successful
if ev_router_available:
    app.include_router(predict_ev.router)
else:
    logging.info("EV router was not available and thus not included in FastAPI app.") # Changed to info for less verbosity