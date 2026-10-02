const API_BASE_URL =
    import.meta.env.VITE_API_BASE_URL ||
    "http://127.0.0.1:8000/api";


export async function indexRepository(repositoryPath) {
    const response = await fetch(`${API_BASE_URL}/index`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            repository_path: repositoryPath,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to index repository");
    }

    return response.json();
}


export async function chatWithRepository(query, topK = 5) {
    const response = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            query: query,
            top_k: topK,
        }),
    });

    if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to generate response");
    }

    return response.json();
}

export async function indexGitHubRepository(githubUrl) {

    const response = await fetch(
        `${API_BASE_URL}/index/github`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
            },

            body: JSON.stringify({
                github_url: githubUrl,
            }),
        }
    );

    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail ||
            "Failed to index GitHub repository"
        );
    }

    return response.json();
}

export async function chatWithAgent(query) {
    const response = await fetch(
        `${API_BASE_URL}/agent/chat`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                query,
                top_k: 5,
            }),
        }
    );

    if (!response.ok) {
        const error = await response.json();

        throw new Error(
            error.detail || "Agent request failed"
        );
    }

    return response.json();
}