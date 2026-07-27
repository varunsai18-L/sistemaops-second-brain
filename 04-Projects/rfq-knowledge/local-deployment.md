# Local Deployment Notes

Prepared by: Palak Nagar

## Services

- Python 3.11+
- MongoDB Community or Enterprise
- Ollama with the configured local model
- Graphviz, if Graphviz diagrams are used later

## Offline Operation

As per the proposal, the application should be able to run locally after all required dependencies and models are installed. Any external API integration should be avoided unless the team approves it.

## Local Runtime Checklist

- MongoDB is reachable at `MONGODB_URI`.
- Ollama is reachable at `OLLAMA_BASE_URL`.
- The model in `OLLAMA_MODEL` is pulled locally.
- Upload and output directories exist and are excluded from Git.
- Test RFQs use dummy or approved sample content.
