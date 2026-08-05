import React, { useState, useRef, useEffect } from "react";
import { X, Send, Loader2, GitBranch, FileCode, Trash2 } from "lucide-react";
import { Label } from "./Typography";
import { cn } from "../lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { sendChatMessage } from "../services/api";

export const ChatInterface = ({ isOpen, onClose, repoName, repositoryId }) => {
  const activeId = repositoryId || repoName;
  const storageKey = `compass_chat_${activeId || 'default'}`;
 
  const [messages, setMessages] = useState(() => {
    if (!repoName) return [];
    const saved = localStorage.getItem(storageKey);
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {
        console.error("Failed to parse saved chat history", e);
      }
    }
    return [
      {
        role: "assistant",
        text: `Compass initialized for **${repoName}**. Ask me about the architecture, key functions, dependencies, or workflow logic within this repository.`,
      },
    ];
  });

  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (activeId && messages.length > 0) {
      localStorage.setItem(storageKey, JSON.stringify(messages));
    }
  }, [messages, activeId, storageKey]);

  // Re-initialize message state if repository switches
  useEffect(() => {
    if (repoName) {
      const saved = localStorage.getItem(storageKey);
      if (saved) {
        try {
          setMessages(JSON.parse(saved));
          return;
        } catch (e) {
          console.error(e);
        }
      }
      setMessages([
        {
          role: "assistant",
          text: `Compass initialized for **${repoName}**. Ask me about the architecture, key functions, dependencies, or workflow logic within this repository.`,
        },
      ]);
    }
  }, [repoName, storageKey]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isOpen]);

  const clearChatHistory = () => {
    if (activeId) {
      localStorage.removeItem(storageKey);
      setMessages([
        {
          role: "assistant",
          text: `Compass initialized for **${repoName}**. Ask me about the architecture, key functions, dependencies, or workflow logic within this repository.`,
        },
      ]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: userMessage }]);
    setIsLoading(true);

    try {
      const data = await sendChatMessage(activeId, userMessage);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: data.answer || data.response,
          filesAnalyzed: data.citations || data.filesAnalyzed,
        },
      ]);
    } catch (error) {
      const errorMessage =
        error.response?.data?.detail ||
        error.response?.data?.error ||
        error.message;
      setMessages((prev) => [
        ...prev,
        {
          role: "system",
          text: `Error: ${errorMessage}. Ensure your backend server is connected.`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.98, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.98, y: 20 }}
          transition={{ duration: 0.25, ease: [0.25, 0, 0, 1] }}
          className="fixed inset-0 md:inset-auto md:bottom-6 md:right-6 w-full md:w-[680px] h-[100dvh] md:h-[650px] md:max-h-[85vh] z-[9999] bg-black border-0 md:border md:border-zinc-800 flex flex-col shadow-2xl rounded-none text-white selection:bg-[#5568fe] selection:text-white overflow-hidden"
        >
          {/* Header */}
          <div className="border-b border-zinc-900 p-4 flex justify-between items-center bg-zinc-950/90 backdrop-blur-md">
            <div className="flex items-center gap-3 min-w-0 pr-2">
              <GitBranch className="w-5 h-5 text-[#5568fe] shrink-0" />
              <div className="truncate">
                <Label className="text-[#5568fe] block text-[10px] font-mono tracking-widest uppercase font-bold">
                  Compass Intelligence
                </Label>
                <h3 className="text-sm md:text-base font-sans font-bold tracking-tight text-white truncate">
                  {repoName}
                </h3>
              </div>
            </div>

            <div className="flex items-center gap-1 shrink-0">
              <button
                onClick={clearChatHistory}
                title="Clear Chat History"
                className="text-zinc-500 hover:text-red-400 transition-colors p-2 focus:outline-none cursor-pointer"
              >
                <Trash2 strokeWidth={1.5} className="w-4 h-4" />
              </button>
              <button
                onClick={onClose}
                className="text-zinc-500 hover:text-white transition-colors p-2 focus:outline-none cursor-pointer"
              >
                <X strokeWidth={1.5} className="w-5 h-5" />
              </button>
            </div>
          </div>

          {/* Messages Feed */}
          <div className="flex-1 overflow-y-auto p-4 space-y-6 bg-black">
            {messages.map((msg, i) => (
              <div
                key={i}
                className={cn(
                  "flex flex-col",
                  msg.role === "user" ? "items-end" : "items-start"
                )}
              >
                <div
                  className={cn(
                    "max-w-[92%] sm:max-w-[85%] p-4 text-sm md:text-base font-sans prose prose-invert w-full overflow-hidden whitespace-normal break-words rounded-none",
                    msg.role === "user"
                      ? "bg-[#5568fe] text-white prose-p:text-white prose-headings:text-white prose-strong:text-white"
                      : msg.role === "system"
                        ? "bg-red-950/40 text-red-400 border border-red-900/60"
                        : "bg-zinc-950 text-zinc-200 border border-zinc-800"
                  )}
                >
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      p: ({ node, ...props }) => (
                        <p
                          className="mb-3 last:mb-0 leading-relaxed text-sm md:text-base"
                          {...props}
                        />
                      ),
                      h1: ({ node, ...props }) => (
                        <h1
                          className="text-lg md:text-xl font-bold mb-3 mt-4 first:mt-0 text-white"
                          {...props}
                        />
                      ),
                      h2: ({ node, ...props }) => (
                        <h2
                          className="text-base md:text-lg font-bold mb-2 mt-3 first:mt-0 text-white"
                          {...props}
                        />
                      ),
                      ul: ({ node, ...props }) => (
                        <ul
                          className="list-disc pl-5 mb-3 space-y-1 text-sm"
                          {...props}
                        />
                      ),
                      ol: ({ node, ...props }) => (
                        <ol
                          className="list-decimal pl-5 mb-3 space-y-1 text-sm"
                          {...props}
                        />
                      ),
                      li: ({ node, ...props }) => (
                        <li className="mb-1" {...props} />
                      ),
                      code: ({ node, inline, ...props }) =>
                        inline ? (
                          <code
                            className="bg-zinc-900 px-1.5 py-0.5 text-xs font-mono text-[#5568fe] rounded-none border border-zinc-800"
                            {...props}
                          />
                        ) : (
                          <div className="overflow-x-auto bg-zinc-900/90 my-3 border border-zinc-800 w-full">
                            <code
                              className="block p-3 text-xs font-mono text-left whitespace-pre text-zinc-200"
                              {...props}
                            />
                          </div>
                        ),
                    }}
                  >
                    {msg.text}
                  </ReactMarkdown>

                  {msg.filesAnalyzed && (
                    <div className="mt-3 pt-3 border-t border-zinc-800/80 flex items-center gap-2 text-xs font-mono text-zinc-500">
                      <FileCode className="w-3.5 h-3.5 text-[#5568fe]" />
                      <span>Context extracted from key codebase modules</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="flex items-start">
                <div className="bg-zinc-950 text-zinc-300 border border-zinc-800 p-4 flex items-center gap-3">
                  <Loader2 className="w-4 h-4 animate-spin text-[#5568fe]" />
                  <span className="text-xs font-mono tracking-wider">
                    Parsing AST & Repository Context...
                  </span>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Box */}
          <div className="p-4 border-t border-zinc-900 bg-black">
            <form
              onSubmit={handleSubmit}
              className="relative flex items-center"
            >
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask about components, architectural design, API routes..."
                className="w-full bg-zinc-950 border border-zinc-800 text-white placeholder:text-zinc-600 h-12 pl-4 pr-12 focus:outline-none focus:border-[#5568fe] transition-colors font-sans text-sm rounded-none"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="absolute right-2 top-2 bottom-2 w-8 flex items-center justify-center text-[#5568fe] hover:text-[#7887ff] disabled:opacity-40 transition-colors cursor-pointer"
              >
                <Send className="w-4 h-4" strokeWidth={1.5} />
              </button>
            </form>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
