
import React, { useState, useRef, useEffect } from "react";
import { Bot, X, Send, User } from "lucide-react";
import "./AIAdvisor.css";

const API_BASE_URL = "http://127.0.0.1:8000";

// Guest mode for now. Login integration will be added later.
const USER_ID = null;

const DEFAULT_SUGGESTIONS = [
  "What government schemes are available for students?",
  "What schemes support women entrepreneurs?",
  "What government benefits are available for farmers?",
  "How can I apply for government schemes?",
];

function AIAdvisor() {
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState(DEFAULT_SUGGESTIONS);

  const messagesEndRef = useRef(null);

  // Load suggested questions from FastAPI
  useEffect(() => {
    const loadSuggestions = async () => {
      try {
        const response = await fetch(
          `${API_BASE_URL}/api/chat/suggestions`
        );

        if (!response.ok) {
          throw new Error("Unable to load suggestions");
        }

        const data = await response.json();

        if (
          Array.isArray(data.suggestions) &&
          data.suggestions.length > 0
        ) {
          setSuggestions(data.suggestions);
        }
      } catch (error) {
        console.error("Suggestions API Error:", error);
      }
    };

    loadSuggestions();
  }, []);

  // Automatically scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, isLoading]);

  // Send message to FastAPI
  const handleSend = async (text = message) => {
    const userMessage = text.trim();

    if (!userMessage || isLoading) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: userMessage },
    ]);

    setMessage("");
    setIsLoading(true);

    try {
      // Send the previous six messages as conversation context
      const conversationHistory = messages.slice(-6);

      const response = await fetch(`${API_BASE_URL}/api/chat/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: USER_ID,
          message: userMessage,
          conversation_history: conversationHistory,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to get an AI response."
        );
      }

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response,
        },
      ]);
    } catch (error) {
      console.error("Chat API Error:", error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "I'm unable to connect to the AI Advisor right now. Please check that the backend is running and try again.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-[9999] flex flex-col items-end gap-4">

      {/* Chat Window */}
      {isOpen && (
        <div
          className="
            ai-advisor-enter
            w-[500px]
            max-w-[calc(100vw-32px)]
            h-[560px]
            max-h-[calc(100vh-110px)]
            bg-white
            rounded-2xl
            shadow-2xl
            border border-gray-200
            flex flex-col
            overflow-hidden
          "
        >
          {/* Header */}
          <div className="flex items-center justify-between p-5 border-b border-gray-100 shrink-0">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-xl bg-[#EE6200] text-white flex items-center justify-center">
                <Bot size={26} />
              </div>

              <div>
                <h3 className="text-[17px] font-semibold text-gray-900">
                  AI Scheme Advisor
                </h3>
                <p className="text-sm text-gray-500">
                  Your Government Scheme Assistant
                </p>
              </div>
            </div>

            <button
              onClick={() => setIsOpen(false)}
              className="p-2 rounded-lg text-gray-500 hover:bg-gray-100 transition"
              aria-label="Close AI Advisor"
            >
              <X size={22} />
            </button>
          </div>

          {/* Chat Body */}
          <div className="flex-1 overflow-y-auto p-5 space-y-5">

            {/* Welcome Screen */}
            {messages.length === 0 && (
              <div className="flex flex-col items-center text-center pt-3 pb-2">
                <div className="w-16 h-16 rounded-2xl bg-[#EE6200]/10 text-[#EE6200] flex items-center justify-center mb-4">
                  <Bot size={34} />
                </div>

                <h2 className="text-xl font-semibold text-gray-900 mb-2">
                  How can I help you?
                </h2>

                <p className="text-sm text-gray-500 mb-5">
                  Choose a question or type your own.
                </p>

                {/* Suggested Questions */}
                <div className="w-full space-y-2.5">
                  {suggestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => handleSend(question)}
                      disabled={isLoading}
                      className="
                        w-full text-left
                        text-sm text-gray-700
                        border border-gray-200
                        rounded-xl
                        px-4 py-3
                        hover:border-[#EE6200]
                        hover:bg-[#FFF7ED]
                        disabled:opacity-50
                        transition
                      "
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Conversation Messages */}
            {messages.map((msg, index) => (
              <div
                key={index}
                className={`flex items-start gap-2.5 ${
                  msg.role === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 shrink-0 rounded-full bg-[#FFF7ED] text-[#EE6200] flex items-center justify-center">
                    <Bot size={18} />
                  </div>
                )}

                <div
                  className={`
                    max-w-[85%]
                    px-4 py-3
                    rounded-2xl
                    text-sm
                    leading-relaxed
                    whitespace-pre-wrap
                    break-words
                    ${
                      msg.role === "user"
                        ? "bg-[#EE6200] text-white rounded-br-sm"
                        : "bg-gray-100 text-gray-800 rounded-bl-sm"
                    }
                  `}
                >
                  {msg.content}
                </div>

                {msg.role === "user" && (
                  <div className="w-8 h-8 shrink-0 rounded-full bg-[#FFF7ED] text-[#EE6200] flex items-center justify-center">
                    <User size={18} />
                  </div>
                )}
              </div>
            ))}

            {/* Loading Indicator */}
            {isLoading && (
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-full bg-[#FFF7ED] text-[#EE6200] flex items-center justify-center">
                  <Bot size={18} />
                </div>

                <div className="bg-gray-100 rounded-2xl rounded-bl-sm px-4 py-3 flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="p-4 border-t border-gray-100 shrink-0">
            <div className="flex items-center gap-2.5">
              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleSend();
                }}
                placeholder="Type your question here..."
                className="
                  flex-1 min-w-0
                  h-12 px-4
                  rounded-xl
                  border border-gray-200
                  text-sm text-gray-800
                  outline-none
                  focus:border-[#EE6200]
                  focus:ring-2 focus:ring-[#EE6200]/10
                  transition
                "
              />

              <button
                onClick={() => handleSend()}
                disabled={!message.trim() || isLoading}
                className="
                  w-12 h-12 shrink-0
                  rounded-xl
                  bg-[#EE6200]
                  text-white
                  flex items-center justify-center
                  hover:bg-[#CC5200]
                  disabled:opacity-50
                  disabled:cursor-not-allowed
                  transition
                "
                aria-label="Send message"
              >
                <Send size={19} />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Floating AI Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="
          w-[58px] h-[58px]
          rounded-full
          bg-[#EE6200]
          text-white
          shadow-lg
          flex items-center justify-center
          hover:bg-[#CC5200]
          hover:scale-105
          transition-all duration-200
        "
        aria-label={isOpen ? "Close AI Advisor" : "Open AI Advisor"}
      >
        {isOpen ? <X size={27} /> : <Bot size={29} />}
      </button>
    </div>
  );
}

export default AIAdvisor;
