"""Planning agent node."""
from src.core.state import DSAState, PlannerContext
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)


def _build_llm():
    """Build the configured local or hosted chat model."""
    provider = settings.llm_provider.lower()
    if provider == "ollama":
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.llm_model,
            base_url=settings.ollama_base_url,
        )
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        if not settings.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required when LLM_PROVIDER=openai. "
                "Set LLM_PROVIDER=ollama to use a local Ollama model."
            )
        return ChatOpenAI(model=settings.llm_model, api_key=settings.openai_api_key)
    raise RuntimeError(
        f"Unsupported LLM_PROVIDER={settings.llm_provider!r}. "
        "Choose 'ollama' or 'openai'."
    )


async def planner_node(state: DSAState) -> dict:
    """Analyzes data and creates an execution plan using an LLM."""
    state.update_status("planning", "planner")
    state.append_log("Generating execution plan via LLM.")
    
    llm = _build_llm()
    
    # Simplified LLM prompt for demonstration
    # Updated to use dataset_schema instead of schema
    prompt = f"Analyze this schema and suggest a plan: {state.dataset_metadata.dataset_schema}"
    response = await llm.ainvoke(prompt)
    content = getattr(response, "content", "")
    reasoning = (
        content
        if isinstance(content, str) and content
        else "Local model returned no planning explanation."
    )
    
    plan = PlannerContext(
        target_column="col2",
        confidence=0.85,
        reasoning=reasoning,
        suggested_models=["RandomForest", "XGBoost"],
        preprocessing_steps=["impute_missing", "label_encode"]
    )
    
    state.metadata["next_agent"] = "explorer"
    return {"planner_context": plan}
