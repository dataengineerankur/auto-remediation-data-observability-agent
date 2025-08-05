"""Helper for interacting with the Groq LLM via LangChain.

This module provides a simple interface for sending prompts to the
Groq Llama3 model using LangChain. It reads the API key from the
``GROQ_API_KEY`` environment variable. If the key is missing,
``ValueError`` is raised.
"""

from __future__ import annotations

import os
from typing import Any

# Attempt to import Groq from a couple of possible locations. If all
# imports fail we set ``Groq`` to ``None`` so the rest of the module can
# handle missing dependencies gracefully.
try:
    # Prefer the community Groq wrapper if available (newer LangChain)
    from langchain_community.llms import Groq  # type: ignore
except Exception:
    try:
        # Fall back to the built‑in LangChain Groq wrapper
        from langchain.llms import groq as Groq  # type: ignore
    except Exception:
        Groq = None  # type: ignore


def get_llm(**kwargs: Any) -> Groq:
    """Instantiate and return a Groq LLM.

    This helper tries to instantiate the Groq integration from
    ``langchain_community`` first (recommended) and falls back to the
    built‑in ``langchain.llms.groq`` wrapper. Keyword arguments are
    forwarded directly to the underlying constructor. When no explicit
    ``api_key`` is provided, the function reads the key from the
    ``GROQ_API_KEY`` environment variable.

    Args:
        **kwargs: Additional arguments accepted by the Groq constructor.

    Returns:
        An instance of the Groq LLM client.

    Raises:
        ValueError: If no API key is supplied via kwargs or the
            ``GROQ_API_KEY`` environment variable.
    """
    api_key = kwargs.pop("api_key", None) or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY environment variable must be set to use the LLM."
        )
    if Groq is None:
        raise ImportError(
            "Neither langchain_community.llms.Groq nor langchain.llms.groq could "
            "be imported. Please install the appropriate LangChain packages."
        )
    # Construct the LLM instance. The alias ``Groq`` refers either to
    # langchain_community.llms.Groq or langchain.llms.groq.Groq depending
    # on which import succeeded above.
    return Groq(api_key=api_key, **kwargs)  # type: ignore


def call_llm(prompt: str, **kwargs: Any) -> str:
    """Send a prompt to the LLM and return its response as a string.

    The function builds an LLM instance on demand and invokes it with
    the provided prompt. If the underlying call raises an exception
    (for example due to network connectivity issues or missing
    dependencies), the exception is caught and a fallback message is
    returned. This makes local development smoother when the Groq API
    cannot be reached.

    Args:
        prompt: The prompt string to send to the model.
        **kwargs: Additional parameters such as ``temperature`` or ``max_tokens``.

    Returns:
        The generated text from the model, or a simulated response if the
        LLM cannot be contacted.
    """
    try:
        if Groq is None:
            raise ImportError
        llm = get_llm(**kwargs)
        # Use ``invoke`` if available (newer API), otherwise fall back to
        # ``predict`` on older LangChain versions.
        if hasattr(llm, "invoke"):
            return llm.invoke(prompt)  # type: ignore
        return llm.predict(prompt)  # type: ignore
    except Exception:
        # Provide a deterministic fallback response for local execution
        # Do not echo the full prompt to avoid verbose output. Instead return
        # a concise simulated response that indicates the LLM could not be
        # reached. This keeps CLI output readable while still signalling
        # that a real call would occur here.
        return (
            "[LLM unavailable] Simulated response: unable to call Groq. "
            "Install the required packages and set the GROQ_API_KEY to use the LLM."
        )
