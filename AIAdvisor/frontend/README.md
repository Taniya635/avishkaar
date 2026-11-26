# AI Advisor Widget

A reusable floating AI Government Scheme Advisor built with React, JavaScript, Tailwind CSS v4 and Lucide React. It connects to a FastAPI backend to provide AI-powered government scheme guidance using Gemini.

## Folder Structure

```text
frontend/
├── AIAdvisor.jsx
├── AIAdvisor.css
└── README.md
```

## Technologies Used

- React 19
- JavaScript
- Tailwind CSS v4
- Lucide React
- FastAPI
- Google Gemini API

## Widget Features

- Floating AI button fixed at the bottom-right.
- Expandable chat window.
- Responsive chat interface.
- Chat window dimensions: 500 × 560 px.
- Floating button dimensions: 58 × 58 px.
- Readable chat messages and suggested questions.
- User and AI chat bubbles.
- Loading animation while generating responses.
- Automatic scrolling to the latest message.
- Dynamic suggested questions from the backend.
- Conversation context using the previous six messages.
- Guest-user support.
- Orange and cream theme.

## Frontend Dependencies

The host React project must have `lucide-react` installed.

```bash
npm install lucide-react
```

Tailwind CSS v4 must also be configured in the host React project.

## Frontend Integration

1. Copy the frontend component files into your React project's components directory.

```text
src/
└── components/
    └── AIAdvisor/
        ├── AIAdvisor.jsx
        └── AIAdvisor.css
```

2. Import the component:

```jsx
import AIAdvisor from "./components/AIAdvisor/AIAdvisor";
```

3. Render it inside the main application component:

```jsx
function App() {
  return (
    <>
      {/* Other application components */}

      <AIAdvisor />
    </>
  );
}

export default App;
```

## Backend Integration

The widget communicates with the FastAPI backend.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/chat/` | Send messages and receive AI responses |
| GET | `/api/chat/suggestions` | Retrieve suggested questions |

### Backend Requirements

- FastAPI
- Uvicorn
- Google Gemini API integration
- Python dependencies listed in `requirements.txt`

### Backend URL

The current development configuration uses:

```text
http://127.0.0.1:8000
```

Update `API_BASE_URL` in `AIAdvisor.jsx` when connecting to a deployed backend.

### CORS Configuration

The FastAPI backend must allow requests from the host React application's origin.

### Request Format

```json
{
  "user_id": null,
  "message": "What government schemes are available for students?",
  "conversation_history": []
}
```

### Response Format

```json
{
  "user_id": null,
  "message": "What government schemes are available for students?",
  "response": "AI-generated response..."
}
```

## Current Authentication Status

The widget currently operates in guest mode using `user_id: null`.

Integration with the host application's authentication and user profile system can be added separately.

## Important Notes

- The FastAPI backend must be running for AI responses to work.
- The Gemini API key must be configured securely in the backend environment.
- Never expose the Gemini API key in frontend code.
- Conversation history is maintained in React component state during the current page session.
- The current backend URL is configured for local development and must be changed for deployment.
