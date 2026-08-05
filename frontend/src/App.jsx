import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Terminal,
  Loader2,
  CheckCircle2,
  Code2,
  FileText,
  MessageSquare,
  AlertCircle,
} from "lucide-react";
import { H1, Body } from "./components/Typography";
import { useDirectionalReveal } from "./lib/utils";
import { ChatInterface } from "./components/ChatInterface";
import { LandingPage } from "./components/LandingPage";
import {
  ingestRepository,
  getTaskStatus,
  getRepositoryDetails,
} from "./services/api";

function App() {
  const [isChatOpen, setIsChatOpen] = useState(false);
 
  const [selectedRepo, setSelectedRepo] = useState(
    () => localStorage.getItem("compass_selectedRepo") || "",
  );
  const [customRepoInput, setCustomRepoInput] = useState(
    () => localStorage.getItem("compass_selectedRepo") || "",
  );
  const [taskId, setTaskId] = useState(
    () => localStorage.getItem("compass_taskId") || null,
  );
  const [isIngesting, setIsIngesting] = useState(false);
  const [statusInfo, setStatusInfo] = useState({
    progress: 0,
    status: "",
    ready: false,
    error: null,
  });
  const [repoDetails, setRepoDetails] = useState(() => {
    const saved = localStorage.getItem("compass_repoDetails");
    return saved ? JSON.parse(saved) : null;
  });

  const { ref: exploreRef, animate: exploreAnimate } =
    useDirectionalReveal("-50px");

  // Sync states to local storage
  useEffect(() => {
    if (selectedRepo)
      localStorage.setItem("compass_selectedRepo", selectedRepo);
    if (taskId) localStorage.setItem("compass_taskId", taskId);
    if (repoDetails)
      localStorage.setItem("compass_repoDetails", JSON.stringify(repoDetails));
  }, [selectedRepo, taskId, repoDetails]);
 
  const clearTaskStorage = () => {
    localStorage.removeItem("compass_taskId");
    localStorage.removeItem("compass_repoDetails");
    setTaskId(null);
    setRepoDetails(null);
  };

  // Handle repository ingestion
  const handleIngest = async (repoTarget) => {
    if (!repoTarget || isIngesting) return;

    const formattedUrl = repoTarget.startsWith("http")
      ? repoTarget
      : `https://github.com/${repoTarget}`;

    setSelectedRepo(repoTarget);
    setIsIngesting(true);
    clearTaskStorage();
    setStatusInfo({
      progress: 0,
      status: "Initiating backend analysis...",
      ready: false,
      error: null,
    });

    try {
      const res = await ingestRepository(formattedUrl);
      if (res?.task_id) {
        setTaskId(res.task_id);
      } else {
        throw new Error(res?.error || "Failed to retrieve task ID.");
      }
    } catch (err) {
      console.error("Ingestion Error:", err);
      setIsIngesting(false);
      setStatusInfo({
        progress: 0,
        status: "Failed",
        ready: false,
        error:
          err.response?.data?.detail ||
          err.message ||
          "Failed to initiate repository ingestion. Verify your backend server connection.",
      });
    }
  };

  // Poll task status endpoint  
  useEffect(() => {
    if (!taskId || statusInfo.ready || statusInfo.error) return;

    const interval = setInterval(async () => {
      try {
        const data = await getTaskStatus(taskId);
 
        if (
          data.status?.toLowerCase() === "failed" ||
          data.status?.toLowerCase() === "error" ||
          data.error
        ) {
          clearInterval(interval);
          setIsIngesting(false);
          clearTaskStorage();
          setStatusInfo({
            progress: 0,
            status: "FAILED",
            ready: false,
            error:
              data.error ||
              data.detail ||
              "Repository ingestion failed on server.",
          });
          return;
        }
 
        setStatusInfo({
          progress: typeof data.progress === "number" ? data.progress : 0,
          status: data.status || "Processing AST...",
          ready: Boolean(data.ready),
          error: null,
        });
 
        if (data.ready) {
          clearInterval(interval);
          setIsIngesting(false);
          fetchRepoDetails(taskId);
        }
      } catch (err) {
        console.warn(
          "Task expired or backend error (404/500). Clearing stale storage.",
          err,
        );
        clearInterval(interval);
        setIsIngesting(false);
        clearTaskStorage();
        setStatusInfo({
          progress: 0,
          status: "FAILED",
          ready: false,
          error:
            err.response?.data?.detail ||
            "Task expired or connection lost with server.",
        });
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [taskId, statusInfo.ready, statusInfo.error]);

  const fetchRepoDetails = async (id) => {
    try {
      const details = await getRepositoryDetails(id);
      setRepoDetails(details);
    } catch (err) {
      console.error("Failed to fetch repository details", err);
    }
  };

  const handleCustomSubmit = (e) => {
    e.preventDefault();
    if (customRepoInput.trim()) {
      handleIngest(customRepoInput.trim());
    }
  };

  return (
    <div className="min-h-screen bg-black text-white relative selection:bg-[#5568fe] selection:text-white">
      {/* Hero Section */}
      <LandingPage onSearchRepo={(repo) => handleIngest(repo)} />

      {/* Main Analysis Section */}
      <motion.section
        id="explore-section"
        ref={exploreRef}
        initial="hiddenBelow"
        animate={exploreAnimate}
        variants={{
          hiddenAbove: { opacity: 0, y: -40 },
          hiddenBelow: { opacity: 0, y: 40 },
          visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 0.5, ease: [0.25, 0, 0, 1] },
          },
        }}
        className="min-h-screen w-full mt-10 bg-black text-white flex flex-col justify-center items-center px-6 md:px-16 py-16 border-b border-zinc-900 overflow-hidden"
      >
        <div className="w-full max-w-4xl mx-auto flex flex-col items-center text-center my-auto">
          <div className="flex flex-col items-center text-center space-y-4 mb-10">
            <H1 className="text-6xl sm:text-7xl md:text-8xl lg:text-[7rem] font-black tracking-tighter text-white leading-[0.9]">
              Repositories<span className="text-[#5568fe]">:</span>
            </H1>

            <Body className="text-zinc-400 max-w-xl text-base sm:text-lg font-normal leading-relaxed">
              Enter a repository URL to analyze architecture and chat directly
              with source context.
            </Body>
          </div>

          {/* Form Input Container */}
          <form
            onSubmit={handleCustomSubmit}
            className="w-full max-w-2xl mx-auto mb-8"
          >
            <div className="group relative bg-black border border-zinc-800/80 p-6 sm:p-8 space-y-4 text-left overflow-hidden">
              <div className="absolute top-0 left-0 h-[3px] w-12 bg-[#5568fe] group-hover:w-full transition-all duration-500 ease-in-out" />

              <div className="flex items-center justify-between pt-1">
                <span className="text-zinc-500 font-mono text-xs uppercase tracking-wider font-bold flex items-center gap-2">
                  <span className="text-[#5568fe] font-mono font-bold">
                    &gt;_
                  </span>
                  REPOSITORY TARGET
                </span>
                {isIngesting && (
                  <span className="text-[#5568fe] font-mono text-xs uppercase tracking-wider font-bold animate-pulse">
                    ANALYZING...
                  </span>
                )}
              </div>

              <div className="flex flex-col sm:flex-row items-stretch gap-3">
                <div className="relative flex-1 flex items-center bg-zinc-950 border border-zinc-800 focus-within:border-[#5568fe] transition-colors">
                  <input
                    type="text"
                    value={customRepoInput || ""}
                    onChange={(e) => setCustomRepoInput(e.target.value)}
                    placeholder="https://github.com/honojs/hono"
                    disabled={isIngesting}
                    className="w-full bg-transparent text-white placeholder:text-zinc-600 px-4 py-3 focus:outline-none font-mono text-xs sm:text-sm tracking-tight rounded-none disabled:opacity-50"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isIngesting || !customRepoInput?.trim()}
                  className="h-11 sm:h-auto px-6 bg-[#5568fe] hover:bg-[#4353d8] active:bg-[#3b4abf] text-white font-mono text-xs uppercase tracking-wider font-bold disabled:opacity-40 transition-all cursor-pointer rounded-none border-none flex items-center justify-center gap-2 whitespace-nowrap shrink-0"
                >
                  {isIngesting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>PARSING...</span>
                    </>
                  ) : (
                    <span>ANALYZE</span>
                  )}
                </button>
              </div>
            </div>
          </form>

          {/* Progress Indicator */}
          {isIngesting && (
            <div className="w-full max-w-2xl bg-black border border-zinc-800/80 p-6 text-left mb-8 space-y-3">
              <div className="flex justify-between text-xs font-mono uppercase tracking-wider">
                <span className="text-[#5568fe]">
                  {statusInfo.status || "Processing AST..."}
                </span>
                <span className="text-zinc-400">{statusInfo.progress}%</span>
              </div>
              <div className="w-full bg-zinc-900 h-1 overflow-hidden">
                <div
                  className="bg-[#5568fe] h-full transition-all duration-300"
                  style={{ width: `${statusInfo.progress}%` }}
                />
              </div>
            </div>
          )}

          {/* Error Display Card */}
          {statusInfo.error && !isIngesting && (
            <div className="w-full max-w-2xl bg-red-950/20 border border-red-900/60 p-6 text-left mb-8 space-y-2">
              <div className="flex items-center gap-2 text-red-400 font-mono text-xs font-bold uppercase tracking-wider">
                <AlertCircle className="w-4 h-4 shrink-0 text-red-400" />
                <span>ANALYSIS FAILED</span>
              </div>
              <p className="text-xs font-mono text-red-300/90 leading-relaxed">
                {statusInfo.error}
              </p>
            </div>
          )}

          {/* Ingestion Ready Card */}
          {repoDetails && !isIngesting && (
            <div className="w-full max-w-2xl bg-black border border-zinc-800/80 p-6 sm:p-8 text-left space-y-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 text-emerald-400 text-xs font-mono font-bold uppercase tracking-wider">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  <span>INGESTION READY</span>
                </div>
                <button
                  onClick={() => setIsChatOpen(true)}
                  className="bg-[#5568fe] hover:bg-[#4353d8] text-white text-xs font-mono uppercase tracking-wider font-bold px-5 py-2.5 transition-all flex items-center gap-2 rounded-none cursor-pointer"
                >
                  <MessageSquare className="w-4 h-4 stroke-[2]" />
                  <span>OPEN CHAT</span>
                </button>
              </div>

              <p className="text-xs sm:text-sm text-zinc-300 font-mono leading-relaxed">
                Repository{" "}
                <span className="text-white font-bold">{selectedRepo}</span>{" "}
                containing {repoDetails.total_files} indexed source code files
                across languages: {repoDetails.languages?.join(", ")}.
              </p>

              <div className="grid grid-cols-2 gap-6 border-t border-zinc-900 pt-6 text-xs font-mono">
                <div className="space-y-2">
                  <span className="text-zinc-500 flex items-center gap-1.5 uppercase tracking-wider">
                    <Code2 className="w-3.5 h-3.5 text-[#5568fe]" /> Languages
                  </span>
                  <p className="text-zinc-200 font-bold">
                    {repoDetails.languages?.join(", ") || "N/A"}
                  </p>
                </div>
                <div className="space-y-2">
                  <span className="text-zinc-500 flex items-center gap-1.5 uppercase tracking-wider">
                    <FileText className="w-3.5 h-3.5 text-[#5568fe]" /> Total
                    Files
                  </span>
                  <p className="text-zinc-200 font-bold">
                    {repoDetails.total_files}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </motion.section>

      {/* Floating Chat Interface */}
      <ChatInterface
        isOpen={isChatOpen}
        onClose={() => setIsChatOpen(false)}
        repoName={selectedRepo || ""}
        repositoryId={taskId}
      />
    </div>
  );
}

export default App;
