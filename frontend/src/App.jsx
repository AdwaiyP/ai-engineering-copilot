import { useState } from "react";

import {
    Bot,
    Check,
    CheckCircle2,
    Code2,
    FileCode2,
    FolderGit2,
    FolderSearch,
    Loader2,
    Search,
    Send,
    Sparkles,
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
    indexGitHubRepository,
    chatWithAgent,
} from "./services/api";

import "./App.css";


function App() {
    const [repositoryUrl, setRepositoryUrl] = useState("");
    const [indexedRepository, setIndexedRepository] = useState("");
    const [chunkCount, setChunkCount] = useState(null);

    const [question, setQuestion] = useState("");
    const [messages, setMessages] = useState([]);

    const [indexing, setIndexing] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");


    async function handleIndexRepository() {
        if (!repositoryUrl.trim() || indexing) return;

        setError("");
        setIndexing(true);

        try {
            const data = await indexGitHubRepository(
                repositoryUrl.trim()
            );

            setIndexedRepository(data.repository);
            setChunkCount(data.chunks);

            setMessages([]);
            setQuestion("");

        } catch (err) {
            setError(err.message);

        } finally {
            setIndexing(false);
        }
    }


    async function handleSubmit(event) {
        event.preventDefault();

        if (
            !question.trim() ||
            !indexedRepository ||
            loading
        ) {
            return;
        }

        const currentQuestion = question.trim();

        setQuestion("");
        setError("");

        setMessages((previous) => [
            ...previous,
            {
                role: "user",
                content: currentQuestion,
            },
        ]);

        setLoading(true);

        try {
            const data = await chatWithAgent(
                currentQuestion
            );

            setMessages((previous) => [
                ...previous,
                {
                    role: "assistant",
                    content: data.answer,
                    toolsUsed: data.tools_used || [],
                },
            ]);

        } catch (err) {
            setError(err.message);

        } finally {
            setLoading(false);
        }
    }


    function getToolTitle(toolName) {
        switch (toolName) {
            case "search_code":
                return "Searched code";

            case "read_file":
                return "Read file";

            case "list_files":
                return "Inspected repository";

            default:
                return toolName;
        }
    }


    function getToolDescription(tool) {
        if (tool.tool === "search_code") {
            return (
                tool.arguments?.query ||
                "Semantic repository search"
            );
        }

        if (tool.tool === "read_file") {
            const path =
                tool.arguments?.file_path || "File";

            const start =
                tool.arguments?.start_line;

            const end =
                tool.arguments?.end_line;

            if (start && end) {
                return `${path} · Lines ${start}–${end}`;
            }

            return path;
        }

        if (tool.tool === "list_files") {
            return "Explored repository structure";
        }

        return "Repository investigation";
    }


    function getToolIcon(toolName) {
        switch (toolName) {
            case "search_code":
                return <Search size={15} />;

            case "list_files":
                return <FolderSearch size={15} />;

            default:
                return <FileCode2 size={15} />;
        }
    }


    return (
        <div className="app-shell">

            {/* Sidebar */}

            <aside className="sidebar">

                <div className="brand">

                    <div className="brand-mark">
                        <Code2 size={21} />
                    </div>

                    <div>
                        <h1>CodePilot</h1>
                        <p>AI Engineering Copilot</p>
                    </div>

                </div>


                <div className="sidebar-divider" />


                <section className="repo-section">

                    <div className="section-heading">
                        <span>Repository</span>
                        <FolderGit2 size={15} />
                    </div>


                    <div className="repo-input">

                    <FolderGit2 size={17} />

                        <input
                            value={repositoryUrl}
                            onChange={(event) =>
                                setRepositoryUrl(
                                    event.target.value
                                )
                            }
                            placeholder="github.com/user/repository"
                            disabled={indexing}
                        />

                    </div>


                    <button
                        className="index-button"
                        onClick={handleIndexRepository}
                        disabled={
                            indexing ||
                            !repositoryUrl.trim()
                        }
                    >

                        {indexing ? (
                            <>
                                <Loader2
                                    size={16}
                                    className="spinner"
                                />
                                Cloning & indexing
                            </>
                        ) : (
                            <>
                                <FolderGit2 size={16} />
                                Index repository
                            </>
                        )}

                    </button>

                </section>


                {indexedRepository && (

                    <div className="repo-card">

                        <div className="repo-card-top">

                            <div className="repo-icon">
                                <FolderGit2 size={17} />
                            </div>

                            <div>
                                <strong>
                                    {indexedRepository}
                                </strong>

                                <span>
                                    GitHub repository
                                </span>
                            </div>

                        </div>


                        <div className="repo-meta">

                            <div>
                                <CheckCircle2 size={14} />
                                Indexed
                            </div>

                            <span>
                                {chunkCount} chunks
                            </span>

                        </div>

                    </div>

                )}


                <div className="sidebar-note">

                    <div className="note-pin" />

                    <Sparkles size={17} />

                    <strong>
                        Agent workspace
                    </strong>

                    <p>
                        CodePilot can search, inspect and
                        reason across your repository using
                        semantic retrieval and agent tools.
                    </p>

                </div>


                <div className="sidebar-footer">

                    <div className="online-dot" />

                    <span>
                        Groq · FAISS · FastAPI
                    </span>

                </div>

            </aside>


            {/* Main Workspace */}

            <main className="workspace">

                <header className="topbar">

                    <div>

                        <div className="breadcrumb">

                            <span>Workspace</span>

                            <span>/</span>

                            <strong>
                                {indexedRepository ||
                                    "No repository"}
                            </strong>

                        </div>

                        <h2>
                            Repository Intelligence
                        </h2>

                    </div>


                    <div className="agent-status">

                        <div className="online-dot" />

                        Agent online

                    </div>

                </header>


                <section className="conversation">

                    {messages.length === 0 ? (

                        <div className="welcome">

                            <div className="welcome-icon">
                                <Bot size={29} />
                            </div>


                            <div className="welcome-label">
                                AI-NATIVE CODE INTELLIGENCE
                            </div>


                            <h2>
                                Understand any codebase.
                                <br />
                                Ask like a teammate.
                            </h2>


                            <p className="welcome-copy">
                                Connect a public GitHub repository.
                                CodePilot searches relevant code,
                                reads files and reasons across the
                                project before answering.
                            </p>


                            <div className="yellow-note">

                                <div className="note-pin" />

                                <span className="note-label">
                                    TRY ASKING
                                </span>

                                <strong>
                                    What should I investigate?
                                </strong>

                                <p>
                                    Start with architecture,
                                    implementation details,
                                    bugs or production improvements.
                                </p>

                            </div>


                            <div className="prompt-grid">

                                <button
                                    disabled={!indexedRepository}
                                    onClick={() =>
                                        setQuestion(
                                            "Explain the architecture of this project."
                                        )
                                    }
                                >
                                    <Code2 size={17} />

                                    <div>
                                        <strong>
                                            Explain architecture
                                        </strong>

                                        <span>
                                            Understand components
                                            and data flow
                                        </span>
                                    </div>
                                </button>


                                <button
                                    disabled={!indexedRepository}
                                    onClick={() =>
                                        setQuestion(
                                            "How is semantic search implemented in this project?"
                                        )
                                    }
                                >
                                    <Search size={17} />

                                    <div>
                                        <strong>
                                            Trace implementation
                                        </strong>

                                        <span>
                                            Follow important code
                                            paths
                                        </span>
                                    </div>
                                </button>


                                <button
                                    disabled={!indexedRepository}
                                    onClick={() =>
                                        setQuestion(
                                            "Find potential problems in this codebase and suggest improvements."
                                        )
                                    }
                                >
                                    <Sparkles size={17} />

                                    <div>
                                        <strong>
                                            Review the codebase
                                        </strong>

                                        <span>
                                            Find issues and
                                            improvements
                                        </span>
                                    </div>
                                </button>

                            </div>

                        </div>

                    ) : (

                        <div className="messages">

                            {messages.map(
                                (message, index) => (

                                    <article
                                        key={index}
                                        className={`message ${message.role}`}
                                    >

                                        <div className="message-avatar">

                                            {message.role ===
                                            "assistant" ? (
                                                <Bot size={18} />
                                            ) : (
                                                <span>You</span>
                                            )}

                                        </div>


                                        <div className="message-body">

                                            <div className="message-author">
                                                {message.role ===
                                                "assistant"
                                                    ? "CodePilot"
                                                    : "You"}
                                            </div>


                                            {message.role ===
                                                "assistant" &&
                                                message.toolsUsed
                                                    ?.length > 0 && (

                                                <div className="agent-trace">

                                                    <div className="trace-header">

                                                        <div>
                                                            <Sparkles
                                                                size={14}
                                                            />

                                                            Agent activity
                                                        </div>

                                                        <span>
                                                            {
                                                                message
                                                                    .toolsUsed
                                                                    .length
                                                            }{" "}
                                                            actions
                                                        </span>

                                                    </div>


                                                    <div className="trace-list">

                                                        {message.toolsUsed.map(
                                                            (
                                                                tool,
                                                                toolIndex
                                                            ) => (

                                                                <div
                                                                    className="trace-item"
                                                                    key={
                                                                        toolIndex
                                                                    }
                                                                >

                                                                    <div className="trace-check">
                                                                        <Check
                                                                            size={
                                                                                12
                                                                            }
                                                                        />
                                                                    </div>

                                                                    <div className="trace-icon">
                                                                        {getToolIcon(
                                                                            tool.tool
                                                                        )}
                                                                    </div>

                                                                    <div>
                                                                        <strong>
                                                                            {getToolTitle(
                                                                                tool.tool
                                                                            )}
                                                                        </strong>

                                                                        <span>
                                                                            {getToolDescription(
                                                                                tool
                                                                            )}
                                                                        </span>
                                                                    </div>

                                                                </div>

                                                            )
                                                        )}

                                                    </div>

                                                </div>

                                            )}


                                            <div className="message-content">

                                                {message.role ===
                                                "assistant" ? (

                                                    <ReactMarkdown
                                                        remarkPlugins={[
                                                            remarkGfm,
                                                        ]}
                                                    >
                                                        {
                                                            message.content
                                                        }
                                                    </ReactMarkdown>

                                                ) : (

                                                    <p>
                                                        {message.content}
                                                    </p>

                                                )}

                                            </div>

                                        </div>

                                    </article>

                                )
                            )}


                            {loading && (

                                <article className="message assistant">

                                    <div className="message-avatar">
                                        <Bot size={18} />
                                    </div>


                                    <div className="message-body">

                                        <div className="message-author">
                                            CodePilot
                                        </div>


                                        <div className="thinking-card">

                                            <Loader2
                                                size={17}
                                                className="spinner"
                                            />

                                            <div>
                                                <strong>
                                                    Investigating
                                                    repository
                                                </strong>

                                                <span>
                                                    Searching and
                                                    inspecting
                                                    relevant code...
                                                </span>
                                            </div>

                                        </div>

                                    </div>

                                </article>

                            )}

                        </div>

                    )}

                </section>


                {error && (

                    <div className="error-banner">
                        {error}
                    </div>

                )}


                <div className="composer-wrapper">

                    <form
                        className="composer"
                        onSubmit={handleSubmit}
                    >

                        <Bot size={19} />

                        <input
                            value={question}
                            onChange={(event) =>
                                setQuestion(
                                    event.target.value
                                )
                            }
                            placeholder={
                                indexedRepository
                                    ? "Ask CodePilot about this repository..."
                                    : "Index a GitHub repository to begin..."
                            }
                            disabled={
                                !indexedRepository ||
                                loading
                            }
                        />


                        <button
                            type="submit"
                            aria-label="Send"
                            disabled={
                                !indexedRepository ||
                                !question.trim() ||
                                loading
                            }
                        >

                            {loading ? (
                                <Loader2
                                    size={18}
                                    className="spinner"
                                />
                            ) : (
                                <Send size={18} />
                            )}

                        </button>

                    </form>


                    <p className="composer-caption">
                        CodePilot can make mistakes. Verify
                        important code before making changes.
                    </p>

                </div>

            </main>

        </div>
    );
}


export default App;