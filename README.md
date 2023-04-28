# NightOwl - manager
This is the deployment of the [NightOwl project](https://github.com/francesco-re-1107/NightOwl).

# Run
```bash
docker build -t nightowl .
docker run -d -p 7070:7070 --name nightowl nightowl
```

# Env variables
| Variable | Description | Default |
|----------|-------------|---------|
| `STREAM_URL` | Video stream to analyze (compatible with OpenCV) | `MANDATORY` |
| `MOVING_AVG_WINDOW` | Size of the moving average window | `10` |
| `TRIGGER_THRESHOLD` | Threshold for triggering the system | `1.9` |
| `COOLDOWN_TIME` | Duration of the cooldown, in seconds | `1200` |
| `ONNX_MODEL_URL` | URL of the ONNX model to download | `SEMI-MANDATORY` |
| `TORCHSCRIPT_MODEL_URL` | URL of the pytorch compiled model to download | `SEMI-MANDATORY` |
