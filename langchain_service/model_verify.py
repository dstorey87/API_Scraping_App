from huggingface_hub import HfApi, HfHubError
from dotenv import load_dotenv
import os
import logging
from datetime import datetime, timedelta
import pytz
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ModelCriteria:
    def __init__(self):
        self.text_requirements = {
            "min_downloads": 50000,
            "max_memory": 8,  # GB for GTX 1080 Ti
            "required_terms": ["mistral", "instruct"],
            "required_tags": [
                "text-generation",
                "transformers"
            ],
            "min_score": 60
        }

class ModelScorer:
    @staticmethod
    def calculate_score(model, requirements: Dict) -> Dict:
        score = 0.0
        details = {}

        # Download score (30 points)
        download_ratio = model.downloads / requirements["min_downloads"]
        details["download_score"] = min(download_ratio * 15, 30)
        score += details["download_score"]

        # Tag matching (25 points)
        tags = set(getattr(model, 'tags', []))
        required_tags = set(requirements["required_tags"])
        tag_matches = len(tags.intersection(required_tags))
        details["tag_score"] = (tag_matches / len(required_tags)) * 25
        score += details["tag_score"]

        # Recency (20 points)
        days_old = (datetime.now(pytz.UTC) - model.created_at).days
        details["recency_score"] = max(0, (90 - days_old) / 90 * 20)
        score += details["recency_score"]

        # Community engagement (15 points)
        likes_score = min(model.likes / 1000 * 7.5, 15)
        details["engagement_score"] = likes_score
        score += details["engagement_score"]

        # Memory efficiency (10 points)
        memory_info = next((tag for tag in tags if "bit" in tag.lower()), None)
        if memory_info and ("4bit" in memory_info or "8bit" in memory_info):
            details["memory_score"] = 10
            score += 10

        return {"total": score, "details": details}

class ModelVerifier:
    def __init__(self):
        load_dotenv()
        self.api = HfApi(token=os.getenv("HUGGINGFACE_API_TOKEN"))
        self.criteria = ModelCriteria()
        self.cutoff_date = datetime.now(pytz.UTC) - timedelta(days=90)

    def search_mistral_models(self) -> List[Dict]:
        """Search for Mistral models."""
        try:
            models = self.api.list_models(
                search="mistral",
                sort="downloads",
                direction=-1
            )
            # Use %-formatting instead of f-strings in logging
            logger.info("Found %d models", len(models))
            return self._process_models(models)
        except HfHubError as e:
            logger.error("API error: %s", str(e))
            return []

    def _process_models(self, models):
        qualified_models = []
        for model in models:
            if not hasattr(model, 'created_at'):
                continue

            # Basic qualification check
            if (model.created_at >= self.cutoff_date and
                any(term in model.modelId.lower() for term in self.criteria.text_requirements["required_terms"])):

                score = self.calculate_score(model)
                if score >= self.criteria.text_requirements["min_score"]:
                    qualified_models.append({
                        "id": model.modelId,
                        "score": score,
                        "downloads": model.downloads,
                        "created": model.created_at.strftime("%Y-%m-%d"),
                        "tags": getattr(model, 'tags', []),
                        "pipeline": getattr(model, 'pipeline_tag', 'unknown')
                    })

        return sorted(qualified_models, key=lambda x: x["score"], reverse=True)

    def calculate_score(self, model) -> float:
        score = 0.0
        req = self.criteria.text_requirements

        # Download score (max 40)
        downloads_ratio = model.downloads / req["min_downloads"]
        score += min(downloads_ratio * 20, 40)

        # Recency score (max 30)
        days_old = (datetime.now(pytz.UTC) - model.created_at).days
        score += max(0, (90 - days_old) / 90 * 30)

        # Tag matching (max 30)
        if hasattr(model, 'tags'):
            matches = sum(1 for tag in req["required_tags"] if tag in model.tags)
            score += (matches / len(req["required_tags"])) * 30

        return score

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    verifier = ModelVerifier()

    print("\n=== Top Mistral Models Analysis ===\n")
    models = verifier.search_mistral_models()

    for i, model in enumerate(models, 1):
        print(f"{i}. {model['id']}")
        print(f"   Score: {model['score']:.1f}/100")
        print(f"   Downloads: {model['downloads']:,}")
        print(f"   Created: {model['created']}")
        if model['tags']:
            print(f"   Tags: {', '.join(model['tags'])}")
        print(f"   Pipeline: {model['pipeline']}")
        print("-" * 50)

# Update config/model_config.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class ModelConfig:
    name: str
    max_memory: Dict[int, str]
    quantization: bool = True
    model_type: str = "vision"
    use_8bit: bool = True
    description: str = ""

MODEL_CONFIGS = {
    # Primary Vision Model - Most downloads, good size for GTX 1080 Ti
    "vision_base": ModelConfig(
        name="meta-llama/Llama-3.2-11B-Vision-Instruct",
        max_memory={0: "10GB"},
        model_type="vision",
        description="Primary vision model (2.2M+ downloads)"
    ),

    # Vision Model Quantized - For memory efficiency
    "vision_optimized": ModelConfig(
        name="unsloth/Llama-3.2-11B-Vision-Instruct-unsloth-bnb-4bit",
        max_memory={0: "6GB"},
        model_type="vision",
        description="4-bit quantized vision model"
    ),

    # Alternative Vision Model - Non-Llama option
    "vision_alt": ModelConfig(
        name="microsoft/Phi-3.5-vision-instruct",
        max_memory={0: "8GB"},
        model_type="vision",
        description="Microsoft Phi vision model (700K+ downloads)"
    )
}