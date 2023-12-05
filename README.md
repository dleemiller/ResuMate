# ResuMate
Your resume's best mate

## Configuration
The following parameters can be configured setting environment variables, or by creating a `.env` file in the same directory as the Flask app:
- `RESUMATE_SECRET_KEY` _(required)_: Secret key for the Flask server
- `OPENAI_API_KEY` _(required)_: API key for accessing the OpenAI API
- `RESUMATE_CACHE_DIR` _(default: `cache`): Directory that will be used for cached content
