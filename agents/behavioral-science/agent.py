"""Behavioral Science Agent - Behavior Analysis and Nudges."""

import os
import json
import hashlib
import datetime
import math
import random
import itertools
from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List, Tuple, Set, Union, Sequence, Callable
from enum import Enum
from pathlib import Path


class BehavioralScienceAgent:
    """Main agent class for behavioral science operations."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        self.config = self._load_config(config_path)
        self.nudge_library: Dict[str, Dict[str, Any]] = {}
        self.behavior_profiles: Dict[str, Dict[str, Any]] = {}
        self.session_history: List[Dict[str, Any]] = []
        self.experiment_registry: Dict[str, Dict[str, Any]] = {}
        self.habit_loops: Dict[str, Dict[str, Any]] = {}
        self.incentive_systems: Dict[str, Dict[str, Any]] = {}
        self.persona_segments: Dict[str, Dict[str, Any]] = {}
        self.intervention_log: List[Dict[str, Any]] = []
        self.cognitive_biases_index: Dict[str, Dict[str, Any]] = {}
        self.feedback_data: List[Dict[str, Any]] = []
        self.pattern_cache: Dict[str, Any] = {}
        self._initialize_defaults()

    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        if config_path and Path(config_path).exists():
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {
            "default_nudge_strength": 0.5,
            "analysis_timeout": 30,
            "confidence_threshold": 0.75,
            "max_persona_segments": 10,
            "habit_loop_iterations": 21,
            "experiment_significance_level": 0.05,
            "data_retention_days": 90,
            "enable_caching": True,
            "log_level": "INFO",
            "max_history_size": 1000,
            "bias_correction_enabled": True,
            "random_seed": 42,
            "supported_biases": [
                "anchoring",
                "confirmation",
                "availability",
                "loss_aversion",
                "endowment",
                "sunk_cost",
                "bandwagon",
                "framing",
                "social_proof",
                "scarcity",
            ],
            "supported_nudge_types": [
                "default_effect",
                "social_norm",
                "commitment_device",
                "reminders",
                "simplification",
                "framing",
                "incentive_alignment",
                "peer_comparison",
            ],
            "supported_personas": [
                "impulsive_spender",
                "deliberate_planner",
                "social_adaptor",
                "risk_averse",
                "novelty_seeker",
                "price_sensitive",
                "brand_loyal",
                "convenience_driven",
            ],
            "supported_habits": [
                "purchase",
                "engagement",
                "retention",
                "onboarding",
                "checkout",
                "review",
                "referral",
                "subscription",
            ],
        }

    def _initialize_defaults(self) -> None:
        random.seed(self.config.get("random_seed", 42))
        default_personas = {
            "impulsive_spender": {
                "description": "Makes quick purchase decisions driven by emotion.",
                "triggers": ["limited_time_offer", "flash_sale", "countdown_timer"],
                "risk_factors": ["high_cart_abandonment", "low_planning"],
                "recommended_nudges": ["scarcity", "social_proof", "friction_reduction"],
            },
            "deliberate_planner": {
                "description": "Researches options thoroughly before acting.",
                "triggers": ["comparison_charts", "detailed_specs", "reviews"],
                "risk_factors": ["long_decision_cycles", "analysis_paralysis"],
                "recommended_nudges": [
                    "commitment_device",
                    "progress_tracking",
                    "simplification",
                ],
            },
            "social_adaptor": {
                "description": "Heavily influences by peers and social norms.",
                "triggers": ["peer_reviews", "social_proof", "community_ratings"],
                "risk_factors": ["bandwagon_effect", "conformity_pressure"],
                "recommended_nudges": [
                    "social_norm",
                    "peer_comparison",
                    "testimonial_highlight",
                ],
            },
            "risk_averse": {
                "description": "Avoids loss and uncertainty.",
                "triggers": ["guarantees", "warranty_info", "return_policy"],
                "risk_factors": ["status_quo_bias", "loss_aversion"],
                "recommended_nudges": [
                    "loss_aversion_framing",
                    "risk_reversal",
                    "default_safe_option",
                ],
            },
            "novelty_seeker": {
                "description": "Enjoys new experiences and products.",
                "triggers": ["new_arrivals", "trending", "early_access"],
                "risk_factors": ["impulse_buying", "brand_switching"],
                "recommended_nudges": ["scarcity", "exclusivity", "gamification"],
            },
            "price_sensitive": {
                "description": "Prioritizes cost savings and discounts.",
                "triggers": ["coupons", "price_drops", "bulk_discounts"],
                "risk_factors": ["cherry_picking", "margin_compression"],
                "recommended_nudges": [
                    "anchoring_discount",
                    "bundle_value",
                    "loyalty_points",
                ],
            },
            "brand_loyal": {
                "description": "Sticks to familiar and trusted brands.",
                "triggers": ["brand_story", "heritage", "repeat_purchase_rewards"],
                "risk_factors": ["switching_cost", "status_quo_bias"],
                "recommended_nudges": [
                    "exclusivity",
                    "membership_benefits",
                    "brand_community",
                ],
            },
            "convenience_driven": {
                "description": "Values speed and ease above all.",
                "triggers": ["express_checkout", "one_click", "auto_reorder"],
                "risk_factors": ["friction_sensitivity", "feature_blindness"],
                "recommended_nudges": [
                    "simplification",
                    "friction_reduction",
                    "auto_fill",
                ],
            },
        }
        self.persona_segments.update(default_personas)
        default_biases = {
            "anchoring": {
                "description": "Heavily influenced by the first piece of information encountered.",
                "applicable_nudges": ["price_anchoring", "reference_point_setting"],
                "risk": 0.7,
            },
            "confirmation": {
                "description": "Seeks information confirming pre-existing beliefs.",
                "applicable_nudges": ["belief_consistent_framing", "selective_evidence"],
                "risk": 0.6,
            },
            "availability": {
                "description": "Overestimates probability of events that are easily recalled.",
                "applicable_nudges": ["priming", "vivid_examples"],
                "risk": 0.5,
            },
            "loss_aversion": {
                "description": "Prefers avoiding losses to acquiring equivalent gains.",
                "applicable_nudges": [
                    "loss_framing",
                    "risk_reversal",
                    "default_safe_option",
                ],
                "risk": 0.8,
            },
            "endowment": {
                "description": "Values things more once they own them.",
                "applicable_nudges": ["free_trial", "preview", "ownership_framing"],
                "risk": 0.6,
            },
            "sunk_cost": {
                "description": "Continues a behavior due to previously invested resources.",
                "applicable_nudges": ["progress_tracking", "milestone_rewards"],
                "risk": 0.7,
            },
            "bandwagon": {
                "description": "Does something primarily because others are doing it.",
                "applicable_nudges": ["social_norm", "popularity_signals"],
                "risk": 0.6,
            },
            "framing": {
                "description": "Draws different conclusions from the same information depending on presentation.",
                "applicable_nudges": ["positive_framing", "negative_framing"],
                "risk": 0.55,
            },
            "social_proof": {
                "description": "Looks to others to determine correct behavior.",
                "applicable_nudges": ["testimonials", "user_counts", "ratings"],
                "risk": 0.5,
            },
            "scarcity": {
                "description": "Places higher value on scarce resources.",
                "applicable_nudges": ["limited_time", "limited_quantity", "countdown"],
                "risk": 0.75,
            },
        }
        self.cognitive_biases_index.update(default_biases)

    def _generate_session_id(self) -> str:
        timestamp = datetime.datetime.utcnow().isoformat()
        raw = f"{timestamp}-{random.randint(1000, 9999)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

    def analyze_behavior(self, user_id: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        if not event_data:
            raise ValueError("event_data must not be empty")
        session_id = self._generate_session_id()
        triggered_biases = []
        for bias_name, bias_info in self.cognitive_biases_index.items():
            if self._check_bias_trigger(bias_name, event_data):
                triggered_biases.append(
                    {
                        "bias": bias_name,
                        "confidence": round(random.uniform(0.5, 0.99), 4),
                        "description": bias_info["description"],
                    }
                )
        nudge_candidates = []
        for bias in triggered_biases:
            bias_name = bias["bias"]
            if bias_name in self.cognitive_biases_index:
                nudge_candidates.extend(
                    self.cognitive_biases_index[bias_name].get(
                        "applicable_nudges", []
                    )
                )
        nudge_candidates = list(set(nudge_candidates))
        recommended_nudges = []
        for persona_name, persona_info in self.persona_segments.items():
            if self._match_persona(event_data, persona_info):
                recommended_nudges.extend(persona_info.get("recommended_nudges", []))
        recommended_nudges = list(set(nudge_candidates + recommended_nudges))
        confidence = (
            round(
                sum(b["confidence"] for b in triggered_biases) / len(triggered_biases),
                4,
            )
            if triggered_biases
            else 0.0
        )
        result = {
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "triggered_biases": triggered_biases,
            "nudge_candidates": nudge_candidates,
            "recommended_nudges": recommended_nudges,
            "overall_confidence": confidence,
            "persona_matches": [],
            "risk_factors": [],
            "suggested_interventions": [],
        }
        for bias in triggered_biases:
            bias_name = bias["bias"]
            if bias_name in self.cognitive_biases_index:
                result["risk_factors"].append(
                    {
                        "bias": bias_name,
                        "risk_score": self.cognitive_biases_index[bias_name].get(
                            "risk", 0.5
                        ),
                    }
                )
        self.session_history.append(result)
        if (
            self.config.get("max_history_size")
            and len(self.session_history)
            > self.config["max_history_size"]
        ):
            self.session_history = self.session_history[-self.config["max_history_size"] :]
        return result

    def _check_bias_trigger(self, bias_name: str, event_data: Dict[str, Any]) -> bool:
        bias_triggers = {
            "anchoring": ["price_anchor_set", "initial_value_encountered"],
            "confirmation": ["belief_confirming_evidence", "filter_bubble_active"],
            "availability": ["recent_exposure", "vivid_memory_recall"],
            "loss_aversion": ["potential_loss_detected", "status_quo_preserved"],
            "endowment": ["item_touched", "trial_initiated"],
            "sunk_cost": ["progress_made", "investment_milestone"],
            "bandwagon": ["peer_action_observed", "trend_alert_triggered"],
            "framing": ["message_frame_positive", "message_frame_negative"],
            "social_proof": ["testimonial_viewed", "rating_examined", "peer_count_seen"],
            "scarcity": ["low_stock_message", "time_limit_encountered"],
        }
        triggers = bias_triggers.get(bias_name, [])
        return any(trigger in event_data.get("tags", []) for trigger in triggers)

    def _match_persona(self, event_data: Dict[str, Any], persona_info: Dict[str, Any]) -> bool:
        score = 0.0
        event_text = json.dumps(event_data).lower()
        for trigger in persona_info.get("triggers", []):
            if trigger.lower() in event_text:
                score += 1.0
        for risk_factor in persona_info.get("risk_factors", []):
            if risk_factor.replace("_", " ") in event_text:
                score += 0.5
        return score >= 1.0

    def design_nudge(
        self,
        trigger: str,
        behavior: str,
        context: Optional[Dict[str, Any]] = None,
        strength: Optional[float] = None,
        nudge_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        if strength is None:
            strength = float(self.config.get("default_nudge_strength", 0.5))
        if not 0.0 <= strength <= 1.0:
            raise ValueError("strength must be between 0.0 and 1.0")
        nudge_id = hashlib.md5(
            f"{trigger}-{behavior}-{strength}-{datetime.datetime.utcnow().isoformat()}".encode(
                "utf-8"
            )
        ).hexdigest()[:8]
        if nudge_type is None:
            nudge_type = self._select_nudge_type(behavior, context)
        nudge = {
            "nudge_id": nudge_id,
            "trigger": trigger,
            "target_behavior": behavior,
            "nudge_type": nudge_type,
            "strength": strength,
            "context": context or {},
            "created_at": datetime.datetime.utcnow().isoformat(),
            "status": "draft",
            "description": self._describe_nudge(nudge_type, trigger, behavior),
            "expected_impact": self._estimate_impact(strength, nudge_type, behavior),
            "implementation_notes": self._implementation_notes(nudge_type),
            "success_metrics": self._default_success_metrics(nudge_type, behavior),
            "related_nudges": [],
            "experiment_suggestions": self._suggest_experiments(nudge_type, behavior),
        }
        self.nudge_library[nudge_id] = nudge
        return nudge

    def _select_nudge_type(self, behavior: str, context: Optional[Dict[str, Any]]) -> str:
        behavior_preferences = {
            "purchase": ["default_effect", "incentive_alignment", "social_norm"],
            "engagement": ["reminders", "commitment_device", "social_norm"],
            "retention": ["commitment_device", "habit_loop", "incentive_alignment"],
            "onboarding": ["simplification", "default_effect", "progress_tracking"],
            "checkout": ["default_effect", "friction_reduction", "commitment_device"],
            "review": ["simple_call_to_action", "social_proof", "reminders"],
            "referral": ["incentive_alignment", "social_norm", "default_effect"],
            "subscription": ["commitment_device", "default_effect", "loss_aversion"],
        }
        candidates = behavior_preferences.get(behavior, ["default_effect"])
        return random.choice(candidates)

    def _describe_nudge(self, nudge_type: str, trigger: str, behavior: str) -> str:
        descriptions = {
            "default_effect": "Set the desired option as the pre-selected default to increase uptake.",
            "social_norm": "Highlight what others are doing to encourage conformity.",
            "commitment_device": "Encourage small upfront commitments to increase follow-through.",
            "reminders": "Send timely prompts to reduce forgetting and procrastination.",
            "simplification": "Reduce cognitive load by simplifying choices or forms.",
            "framing": "Present information in a way that emphasizes gains or losses.",
            "incentive_alignment": "Tie rewards directly to the target behavior.",
            "peer_comparison": "Show individual performance relative to peers.",
            "friction_reduction": "Remove steps or barriers to completing the target action.",
            "loss_aversion_framing": "Frame messages around what users stand to lose by not acting.",
            "risk_reversal": "Reduce perceived risk through guarantees or free trials.",
            "default_safe_option": "Use the safest choice as the default selection.",
            "scarcity": "Leverage limited availability to increase perceived value.",
            "progress_tracking": "Show progress toward a goal to motivate completion.",
            "membership_benefits": "Offer exclusive benefits to reinforce loyalty.",
            "ownership_framing": "Use language that fosters a sense of ownership.",
            "priming": "Expose users to relevant stimuli before asking for action.",
            "testimonial_highlight": "Prominently display relevant testimonials.",
            "popularity_signals": "Display popularity metrics prominently.",
            "limited_time": "Communicate time-limited availability.",
            "limited_quantity": "Communicate scarcity of available units.",
        }
        return descriptions.get(
            nudge_type,
            f"A {nudge_type} nudge triggered by '{trigger}' to encourage '{behavior}'.",
        )

    def _estimate_impact(self, strength: float, nudge_type: str, behavior: str) -> float:
        base_effectiveness = {
            "default_effect": 0.25,
            "social_norm": 0.22,
            "commitment_device": 0.18,
            "reminders": 0.15,
            "simplification": 0.13,
            "framing": 0.12,
            "incentive_alignment": 0.20,
            "peer_comparison": 0.10,
        }
        base = base_effectiveness.get(nudge_type, 0.1)
        return round(base * strength * random.uniform(0.8, 1.2), 4)

    def _implementation_notes(self, nudge_type: str) -> List[str]:
        notes = {
            "default_effect": [
                "Ensure the default is the most commonly chosen option.",
                "Allow easy opt-out to avoid reactance.",
                "Test multiple defaults across persona segments.",
            ],
            "social_norm": [
                "Use descriptive norms relevant to the user.",
                "Avoid misaligned social comparisons.",
                "Update norms dynamically based on user cohort.",
            ],
            "commitment_device": [
                "Start with small, easy commitments.",
                "Escalate commitment gradually.",
                "Pair with reminders for maximum effect.",
            ],
            "reminders": [
                "Time reminders based on typical user activity windows.",
                "Limit frequency to prevent habituation.",
                "Provide value in each reminder message.",
            ],
            "simplification": [
                "Reduce number of choices to 3-5 at decision points.",
                "Use progressive disclosure for complex flows.",
                "Highlight the recommended option.",
            ],
            "framing": [
                "Test both gain and loss frames with audience.",
                "Consider cultural context for framing effectiveness.",
                "Align frame with brand voice.",
            ],
            "incentive_alignment": [
                "Reward should be immediate and salient.",
                "Tie reward magnitude directly to behavior strength.",
                "Avoid undermining intrinsic motivation.",
            ],
            "peer_comparison": [
                "Use relevant comparison groups.",
                "Present data in accessible visual formats.",
                "Avoid demotivating comparisons for low performers.",
            ],
            "friction_reduction": [
                "Identify and eliminate non-essential steps.",
                "Pre-fill known user information.",
                "Offer express checkout lanes.",
            ],
            "loss_aversion_framing": [
                "Emphasize potential losses accurately.",
                "Pair with a clear call to action.",
                "Avoid fear-mongering or exaggeration.",
            ],
            "risk_reversal": [
                "Make guarantees clear and unconditional.",
                "Simplify the claims process.",
                "Display guarantee icons prominently.",
            ],
            "default_safe_option": [
                "Ensure safety properties are verifiable.",
                "Allow users to safely override defaults.",
                "Document rationale for default choices.",
            ],
            "scarcity": [
                "Ensure scarcity claims are truthful.",
                "Combine with personalized relevance.",
                "Test threshold effects thoroughly.",
            ],
            "progress_tracking": [
                "Show incremental progress toward milestones.",
                "Celebrate small wins.",
                "Link progress to meaningful outcomes.",
            ],
            "membership_benefits": [
                "Communicate benefits clearly and frequently.",
                "Create tiers for aspirational motivation.",
                "Ensure benefit uniqueness compared to non-members.",
            ],
            "ownership_framing": [
                "Use first-person possessive language.",
                "Let users customize or mark their territory.",
                "Pair with commitment devices.",
            ],
            "priming": [
                "Use brief, subtle exposures.",
                "Align primes with target behavior.",
                "Avoid overuse to prevent habituation.",
            ],
            "testimonial_highlight": [
                "Rotate testimonials regularly.",
                "Use diverse and relatable voices.",
                "Match testimonials to user segment.",
            ],
            "popularity_signals": [
                "Ensure popularity metrics are accurate.",
                "Update signals in near-real-time.",
                "Use rounded numbers for better engagement.",
            ],
            "limited_time": [
                "Set countdown timers for high-value offers.",
                "Use consistent terminology across channels.",
                "Resend reminders near deadline.",
            ],
            "limited_quantity": [
                "Show remaining stock or capacity.",
                "Trigger urgency at defined thresholds.",
                "Avoid false scarcity signals.",
            ],
        }
        return notes.get(nudge_type, ["Customize for your specific context."])

    def _default_success_metrics(self, nudge_type: str, behavior: str) -> List[Dict[str, Any]]:
        return [
            {
                "metric_name": "conversion_rate",
                "description": f"Percentage of users who complete '{behavior}' after nudge exposure.",
                "target": ">= baseline + 15%",
                "measurement": "experiment",
            },
            {
                "metric_name": "time_to_action",
                "description": "Median time from nudge exposure to behavior completion.",
                "target": "<= baseline - 20%",
                "measurement": "experiment",
            },
            {
                "metric_name": "reactance_rate",
                "description": "Percentage of users who dismiss or negatively respond to nudge.",
                "target": "<= 5%",
                "measurement": "survey",
            },
            {
                "metric_name": "retention_impact",
                "description": "Effect on user retention over 30 days.",
                "target": ">= stabilization",
                "measurement": "longitudinal",
            },
        ]

    def _suggest_experiments(self, nudge_type: str, behavior: str) -> List[Dict[str, Any]]:
        return [
            {
                "experiment_name": f"{nudge_type}_{behavior}_ab_test",
                "design": "A/B",
                "hypothesis": f"Users exposed to {nudge_type} will show higher {behavior} rates.",
                "success_criterion": "Treatment conversion >= control + 10% (p < 0.05)",
                "sample_size_note": "Use power analysis with baseline power = 0.8, alpha = 0.05.",
            },
            {
                "experiment_name": f"{nudge_type}_{behavior}_multivariate",
                "design": "Multivariate",
                "hypothesis": f"Nudge strength variations will show non-linear effects.",
                "success_criterion": "Identify optimal strength and segment-specific effects.",
                "sample_size_note": "Higher sample required for interaction effects.",
            },
            {
                "experiment_name": f"{nudge_type}_{behavior}_longitudinal",
                "design": "Time-series",
                "hypothesis": f"Effect will decay or grow over repeated exposure.",
                "success_criterion": "Stable or increasing conversion over 30 days.",
                "sample_size_note": "Minimum 90 daily observations per variant.",
            },
        ]

    def register_habit_loop(
        self,
        habit_name: str,
        trigger: str,
        behavior: str,
        reward: str,
        loop_strength: float = 0.5,
        cadence: str = "daily",
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not 0.0 <= loop_strength <= 1.0:
            raise ValueError("loop_strength must be between 0.0 and 1.0")
        valid_cadences = ["hourly", "daily", "weekly", "biweekly", "monthly", "variable"]
        if cadence not in valid_cadences:
            raise ValueError(f"cadence must be one of {valid_cadences}")
        loop_id = hashlib.md5(
            f"{habit_name}-{trigger}-{behavior}-{reward}".encode("utf-8")
        ).hexdigest()[:8]
        loop = {
            "loop_id": loop_id,
            "habit_name": habit_name,
            "cue": trigger,
            "routine": behavior,
            "reward": reward,
            "loop_strength": loop_strength,
            "cadence": cadence,
            "notes": notes,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "status": "active",
            "reinforcement_history": [],
            "break_attempts": 0,
            "success_count": 0,
            "current_streak": 0,
            "max_streak": 0,
            "predictions": [],
        }
        self.habit_loops[loop_id] = loop
        return loop

    def reinforce_habit(
        self,
        loop_id: str,
        reward_given: bool = True,
        reward_quality: float = 1.0,
        trigger_occurred: bool = True,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if loop_id not in self.habit_loops:
            raise KeyError(f"Habit loop {loop_id} not found")
        loop = self.habit_loops[loop_id]
        record = {
            "date": datetime.datetime.utcnow().isoformat(),
            "reward_given": reward_given,
            "reward_quality": reward_quality,
            "trigger_occurred": trigger_occurred,
            "metadata": metadata or {},
            "id": len(loop["reinforcement_history"]) + 1,
        }
        loop["reinforcement_history"].append(record)
        if trigger_occurred and reward_given:
            loop["success_count"] += 1
            loop["current_streak"] += 1
            if loop["current_streak"] > loop["max_streak"]:
                loop["max_streak"] = loop["current_streak"]
            loop["loop_strength"] = min(
                1.0, loop["loop_strength"] + (0.02 * reward_quality)
            )
        elif not trigger_occurred:
            loop["break_attempts"] += 1
            loop["current_streak"] = 0
            loop["loop_strength"] = max(0.0, loop["loop_strength"] - 0.05)
        loop["reinforcement_history"] = loop["reinforcement_history"][-100:]
        statistics = self._compute_habit_statistics(loop)
        loop["statistics"] = statistics
        return {
            "loop_id": loop_id,
            "habit_name": loop["habit_name"],
            "updated_loop_strength": round(loop["loop_strength"], 4),
            "statistics": statistics,
            "streak": loop["current_streak"],
            "status": loop["status"],
        }

    def _compute_habit_statistics(self, loop: Dict[str, Any]) -> Dict[str, Any]:
        history = loop.get("reinforcement_history", [])
        total = len(history)
        if total == 0:
            return {"total_records": 0, "success_rate": 0.0, "average_reward_quality": 0.0}
        reward_count = sum(1 for h in history if h.get("reward_given"))
        trigger_count = sum(1 for h in history if h.get("trigger_occurred"))
        avg_quality = (
            sum(h.get("reward_quality", 0.0) for h in history) / total
        )
        return {
            "total_records": total,
            "success_rate": round(reward_count / total, 4),
            "trigger_rate": round(trigger_count / total, 4),
            "average_reward_quality": round(avg_quality, 4),
            "break_attempts": loop.get("break_attempts", 0),
            "current_streak": loop.get("current_streak", 0),
            "max_streak": loop.get("max_streak", 0),
            "loop_strength": round(loop.get("loop_strength", 0.5), 4),
        }

    def create_incentive_system(
        self,
        name: str,
        target_behaviors: List[str],
        reward_type: str,
        reward_value: Union[int, float, str],
        eligibility_criteria: Optional[Dict[str, Any]] = None,
        tracking_mechanism: str = "point_based",
        expiration_days: Optional[int] = None,
    ) -> Dict[str, Any]:
        valid_reward_types = [
            "monetary",
            "points",
            "badge",
            "status",
            "access",
            "discount",
            "donation",
            "charity",
        ]
        if reward_type not in valid_reward_types:
            raise ValueError(f"reward_type must be one of {valid_reward_types}")
        if tracking_mechanism not in ["point_based", "behavior_based", "time_based", "hybrid"]:
            raise ValueError(
                "tracking_mechanism must be one of: point_based, behavior_based, time_based, hybrid"
            )
        system_id = hashlib.md5(f"{name}-{reward_type}".encode("utf-8")).hexdigest()[:8]
        system = {
            "system_id": system_id,
            "name": name,
            "target_behaviors": target_behaviors,
            "reward_type": reward_type,
            "reward_value": reward_value,
            "eligibility_criteria": eligibility_criteria or {},
            "tracking_mechanism": tracking_mechanism,
            "expiration": {
                "days": expiration_days,
                "expiration_date": (
                    (
                        datetime.datetime.utcnow()
                        + datetime.timedelta(days=expiration_days)
                    ).isoformat()
                    if expiration_days
                    else None
                ),
            },
            "created_at": datetime.datetime.utcnow().isoformat(),
            "status": "active",
            "enrollment_count": 0,
            "redemption_count": 0,
            "total_value_distributed": 0.0,
            "rules": self._generate_incentive_rules(
                reward_type, tracking_mechanism, target_behaviors
            ),
            "anti_gaming_measures": self._anti_gaming_measures(),
        }
        self.incentive_systems[system_id] = system
        return system

    def _generate_incentive_rules(
        self,
        reward_type: str,
        tracking_mechanism: str,
        target_behaviors: List[str],
    ) -> List[Dict[str, Any]]:
        rules = [
            {
                "rule_id": f"rule_{i+1}",
                "behavior": behavior,
                "points_awarded": (
                    random.randint(10, 100) if reward_type == "points" else 0
                ),
                "description": f"Award {reward_type} for completing behavior: {behavior}",
                "cooldown_hours": 0,
                "max_daily": 1,
                "is_active": True,
            }
            for i, behavior in enumerate(target_behaviors)
        ]
        rules.append(
            {
                "rule_id": "bonus_streak",
                "behavior": "consecutive_streak",
                "points_awarded": 50 if reward_type == "points" else 0,
                "description": "Bonus reward for 7-day streak",
                "cooldown_hours": 168,
                "max_daily": 1,
                "is_active": True,
            }
        )
        return rules

    def _anti_gaming_measures(self) -> Dict[str, Any]:
        return {
            "rate_limits": {
                "hourly_max": 10,
                "daily_max": 50,
                "weekly_max": 200,
            },
            "fraud_detection": {
                "pattern_analysis": True,
                "velocity_checks": True,
                "device_fingerprinting": True,
                "ip_monitoring": True,
            },
            "validation_checks": [
                "behavior_completion_verification",
                "unique_event_deduplication",
                "session_integrity_check",
            ],
            "penalties": {
                "first_offense": "warning",
                "second_offense": "points_freeze_24h",
                "third_offense": "account_review",
            },
        }

    def record_feedback(
        self,
        user_id: str,
        event_type: str,
        response_data: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not event_type:
            raise ValueError("event_type must not be empty")
        entry = {
            "feedback_id": hashlib.md5(
                f"{user_id}-{event_type}-{datetime.datetime.utcnow().isoformat()}".encode(
                    "utf-8"
                )
            ).hexdigest()[:8],
            "user_id": user_id,
            "event_type": event_type,
            "response": response_data,
            "context": context or {},
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "processed": False,
            "sentiment": self._estimate_sentiment(response_data),
            "categories": self._categorize_feedback(event_type, response_data),
        }
        self.feedback_data.append(entry)
        if (
            self.config.get("max_history_size")
            and len(self.feedback_data) > self.config["max_history_size"]
        ):
            self.feedback_data = self.feedback_data[-self.config["max_history_size"] :]
        return entry

    def _estimate_sentiment(self, response_data: Dict[str, Any]) -> str:
        text = json.dumps(response_data).lower()
        positive_words = ["great", "love", "amazing", "helpful", "easy", "perfect"]
        negative_words = ["bad", "hate", "terrible", "confusing", "annoying", "hard"]
        score = sum(1 for w in positive_words if w in text) - sum(
            1 for w in negative_words if w in text
        )
        if score > 0:
            return "positive"
        if score < 0:
            return "negative"
        return "neutral"

    def _categorize_feedback(self, event_type: str, response_data: Dict[str, Any]) -> List[str]:
        categories = []
        text = json.dumps(response_data).lower()
        if "time" in text or "slow" in text or "fast" in text:
            categories.append("speed")
        if "confusing" in text or "clear" in text or "understand" in text:
            categories.append("clarity")
        if "price" in text or "cost" in text or "expensive" in text:
            categories.append("pricing")
        if "design" in text or "ui" in text or "look" in text:
            categories.append("design")
        if "support" in text or "help" in text or "service" in text:
            categories.append("support")
        if "recommend" in text or "suggest" in text:
            categories.append("recommendation_quality")
        if not categories:
            categories.append("general")
        return categories

    def create_persona_profile(
        self,
        persona_name: str,
        traits: Dict[str, float],
        behavioral_tendencies: List[str],
        description: str = "",
    ) -> Dict[str, Any]:
        if not 0.0 <= all(t for t in traits.values() if isinstance(t, (int, float))):
            pass
        if any(t > 1.0 for t in traits.values() if isinstance(t, (int, float))):
            raise ValueError("All trait values must be between 0.0 and 1.0")
        truncated_name = persona_name.lower().replace(" ", "_").replace("-", "_")
        profile_id = hashlib.md5(truncated_name.encode("utf-8")).hexdigest()[:8]
        profile = {
            "profile_id": profile_id,
            "persona_name": persona_name,
            "traits": traits,
            "behavioral_tendencies": behavioral_tendencies,
            "description": description,
            "created_at": datetime.datetime.utcnow().isoformat(),
            "updated_at": datetime.datetime.utcnow().isoformat(),
            "sample_size": 0,
            "confidence_score": 0.0,
            "recommended_nudges": [],
            "risk_factors": [],
            "example_events": [],
        }
        recommended_nudges, risk_factors = self._derive_nudges_from_traits(
            traits, behavioral_tendencies
        )
        profile["recommended_nudges"] = recommended_nudges
        profile["risk_factors"] = risk_factors
        self.persona_segments[persona_name] = {
            "traits": traits,
            "behavioral_tendencies": behavioral_tendencies,
            "description": description,
            "recommended_nudges": recommended_nudges,
            "risk_factors": risk_factors,
        }
        return profile

    def _derive_nudges_from_traits(
        self, traits: Dict[str, float], tendencies: List[str]
    ) -> Tuple[List[str], List[str]]:
        recommended_nudges: Set[str] = set()
        risk_factors: Set[str] = set()
        if traits.get("impulsivity", 0.0) > 0.6:
            recommended_nudges.update(["friction_reduction", "commitment_device"])
            risk_factors.add("high_impulse_reactivity")
        if traits.get("price_sensitivity", 0.0) > 0.6:
            recommended_nudges.update(["anchoring_discount", "bundle_value"])
            risk_factors.add("margin_pressure")
        if traits.get("social_influence", 0.0) > 0.6:
            recommended_nudges.update(["social_norm", "peer_comparison"])
            risk_factors.add("conformity_pressure")
        if traits.get("risk_tolerance", 0.0) < 0.4:
            recommended_nudges.update(["default_safe_option", "risk_reversal"])
            risk_factors.add("status_quo_bias")
        if traits.get("novelty_seeking", 0.0) > 0.6:
            recommended_nudges.update(["scarcity", "exclusivity", "gamification"])
            risk_factors.add("impulse_buying")
        if traits.get("habit_strength", 0.0) < 0.3:
            recommended_nudges.update(["progress_tracking", "reminders", "commitment_device"])
            risk_factors.add("low_habit_retention")
        if traits.get("deliberation", 0.0) > 0.6:
            recommended_nudges.update(["simplification", "recommendation_highlight"])
            risk_factors.add("analysis_paralysis")
        if traits.get("loss_aversion", 0.0) > 0.6:
            recommended_nudges.update(["loss_aversion_framing", "default_safe_option"])
            risk_factors.add("risk_averse_reactivity")
        if "procrastination" in tendencies:
            recommended_nudges.update(["reminders", "commitment_device", "small_wins"])
        if "brand_switching" in tendencies:
            recommended_nudges.update(["membership_benefits", "exclusivity", "brand_community"])
        if "comparison_shopping" in tendencies:
            recommended_nudges.update(["comparison_charts", "unique_value_prop"])
        if "content_consumption" in tendencies:
            recommended_nudges.update(["personalized_recommendations", "infinite_scroll"])
        return list(recommended_nudges), list(risk_factors)

    def run_ab_test(
        self,
        experiment_name: str,
        control_variant: str,
        treatment_variant: str,
        power: float = 0.8,
        alpha: float = 0.05,
    ) -> Dict[str, Any]:
        if not 0.0 < power < 1.0:
            raise ValueError("power must be between 0.0 and 1.0 exclusive")
        if not 0.0 < alpha < 1.0:
            raise ValueError("alpha must be between 0.0 and 1.0 exclusive")
        experiment_id = hashlib.md5(experiment_name.encode("utf-8")).hexdigest()[:8]
        experiment = {
            "experiment_id": experiment_id,
            "name": experiment_name,
            "control_variant": control_variant,
            "treatment_variant": treatment_variant,
            "power": power,
            "alpha": alpha,
            "status": "running",
            "started_at": datetime.datetime.utcnow().isoformat(),
            "ended_at": None,
            "control_group_size": 0,
            "treatment_group_size": 0,
            "control_conversions": 0,
            "treatment_conversions": 0,
            "significance_achieved": False,
            "p_value": None,
            "effect_size": None,
            "confidence_interval": None,
            "recommended_winner": None,
            "stopping_reason": None,
            "intermediate_results": [],
            "peeking_correction_applied": False,
            "multiple_comparisons_correction": "bonferroni",
        }
        self.experiment_registry[experiment_id] = experiment
        return experiment

    def record_experiment_observation(
        self,
        experiment_id: str,
        variant: str,
        converted: bool,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if experiment_id not in self.experiment_registry:
            raise KeyError(f"Experiment {experiment_id} not found")
        experiment = self.experiment_registry[experiment_id]
        if experiment["status"] not in ["running"]:
            raise ValueError(f"Experiment {experiment_id} is not in running status")
        if variant not in [experiment["control_variant"], experiment["treatment_variant"]]:
            raise ValueError(
                f"variant must be either '{experiment['control_variant']}' or '{experiment['treatment_variant']}'"
            )
        if variant == experiment["control_variant"]:
            experiment["control_group_size"] += 1
            if converted:
                experiment["control_conversions"] += 1
        else:
            experiment["treatment_group_size"] += 1
            if converted:
                experiment["treatment_conversions"] += 1
        result = self._compute_intermediate_experiment_stats(experiment)
        experiment["intermediate_results"].append(result)
        if experiment["intermediate_results"]:
            last = experiment["intermediate_results"][-1]
            if last.get("p_value") is not None and last["p_value"] < experiment["alpha"]:
                experiment["significance_achieved"] = True
                experiment["p_value"] = last["p_value"]
                experiment["effect_size"] = last.get("effect_size")
                experiment["confidence_interval"] = last.get("confidence_interval")
                experiment["recommended_winner"] = (
                    experiment["treatment_variant"]
                    if last.get("treatment_rate", 0) > last.get("control_rate", 0)
                    else experiment["control_variant"]
                )
                experiment["status"] = "concluded"
                experiment["ended_at"] = datetime.datetime.utcnow().isoformat()
        return result

    def _compute_intermediate_experiment_stats(
        self, experiment: Dict[str, Any]
    ) -> Dict[str, Any]:
        n1 = max(experiment["treatment_group_size"], 1)
        n2 = max(experiment["control_group_size"], 1)
        x1 = experiment["treatment_conversions"]
        x2 = experiment["control_conversions"]
        p1 = x1 / n1
        p2 = x2 / n2
        pooled_p = (x1 + x2) / (n1 + n2)
        se = math.sqrt(pooled_p * (1 - pooled_p) * (1 / n1 + 1 / n2))
        z = (
            (p1 - p2) / se
            if se > 0
            else 0.0
        )
        p_value = 2 * (1 - self._normal_cdf(abs(z)))
        effect_size = (p1 - p2) / math.sqrt(pooled_p * (1 - pooled_p)) if pooled_p * (1 - pooled_p) > 0 else 0.0
        z_critical = self._normal_ppf(1 - experiment["alpha"] / 2)
        margin = z_critical * se
        ci_lower = (p1 - p2) - margin
        ci_upper = (p1 - p2) + margin
        power = 1 - self._normal_cdf(
            z_critical - abs(z) * math.sqrt(
                (n1 * n2) / (n1 if n1 > 0 else 1 + n2 if n2 > 0 else 1)
            )
        )
        return {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "control_rate": round(p2, 4),
            "treatment_rate": round(p1, 4),
            "absolute_difference": round(p1 - p2, 4),
            "relative_lift": round((p1 - p2) / p2, 4) if p2 > 0 else 0.0,
            "p_value": round(p_value, 6),
            "effect_size_cohens_h": round(effect_size, 4),
            "confidence_interval_95": [round(ci_lower, 4), round(ci_upper, 4)],
            "control_n": n1,
            "treatment_n": n2,
            "power": round(power, 4),
            "significance_achieved": p_value < experiment["alpha"],
        }

    def _normal_cdf(self, x: float) -> float:
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))

    def _normal_ppf(self, p: float) -> float:
        if p <= 0 or p >= 1:
            raise ValueError("p must be between 0 and 1 exclusive")
        return math.sqrt(2) * self._erfcinv(2 * (1 - p))

    def _erfcinv(self, y: float) -> float:
        if y <= 0:
            raise ValueError("y must be positive")
        approximation = math.sqrt(
            -math.log(0.5 * y * math.sqrt(math.pi)) - math.log(2)
        )
        return approximation

    def build_user_journey(
        self,
        user_id: str,
        journey_name: str,
        stages: List[Dict[str, Any]],
        start_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        if not stages:
            raise ValueError("stages list must not be empty")
        journey_id = hashlib.md5(
            f"{user_id}-{journey_name}".encode("utf-8")
        ).hexdigest()[:8]
        journey = {
            "journey_id": journey_id,
            "user_id": user_id,
            "journey_name": journey_name,
            "stages": stages,
            "start_date": start_date or datetime.datetime.utcnow().isoformat(),
            "end_date": None,
            "current_stage_index": 0,
            "is_completed": False,
            "stage_transitions": [],
            "behavioral_insights": [],
            "nudge_placements": [],
            "completion_rate": 0.0,
            "drop_off_points": [],
        }
        return journey

    def evaluate_journey_stage(
        self,
        journey: Dict[str, Any],
        user_event: Dict[str, Any],
    ) -> Tuple[Dict[str, Any], Optional[str]]:
        current_index = journey.get("current_stage_index", 0)
        stages = journey.get("stages", [])
        if current_index >= len(stages):
            return {"message": "Journey already completed"}, None
        current_stage = stages[current_index]
        next_stage_needed = current_stage.get("required_events", [])
        matched = any(
            event_key in user_event for event_key in next_stage_needed
        )
        if matched:
            transition = {
                "from_stage": current_index,
                "to_stage": min(current_index + 1, len(stages) - 1),
                "timestamp": datetime.datetime.utcnow().isoformat(),
                "trigger_event": user_event,
            }
            journey["stage_transitions"].append(transition)
            journey["current_stage_index"] = min(
                current_index + 1, len(stages) - 1
            )
            if journey["current_stage_index"] >= len(stages) - 1:
                journey["is_completed"] = True
                journey["end_date"] = datetime.datetime.utcnow().isoformat()
            drop_offs = [t["from_stage"] for t in journey["stage_transitions"]]
            stage_counts: Dict[int, int] = {}
            for idx in drop_offs:
                stage_counts[idx] = stage_counts.get(idx, 0) + 1
            if stage_counts:
                max_drop = max(stage_counts, key=stage_counts.get)
                journey["drop_off_points"] = [
                    {"stage_index": idx, "drop_count": count}
                    for idx, count in sorted(stage_counts.items(), key=lambda x: x[1], reverse=True)
                ]
            return {
                "journey_id": journey.get("journey_id"),
                "advanced": True,
                "new_stage_index": journey["current_stage_index"],
                "is_completed": journey["is_completed"],
            }, current_stage.get("nudge_hint")
        return {"journey_id": journey.get("journey_id"), "advanced": False}, None

    def compute_journey_completion(self, journey: Dict[str, Any]) -> Dict[str, Any]:
        stages = journey.get("stages", [])
        total = len(stages)
        if total == 0:
            return {"completion_rate": 0.0, "completed_stages": 0, "total_stages": 0}
        completed = journey.get("current_stage_index", 0)
        if journey.get("is_completed"):
            completed = total
        completion_rate = round(completed / total, 4) if total else 0.0
        journey["completion_rate"] = completion_rate
        drop_offs = journey.get("drop_off_points", [])
        critical_drop = (
            drop_offs[0]["stage_index"] if drop_offs else None
        )
        insight = (
            f"Primary attrition at stage {critical_drop + 1} of {total}."
            if critical_drop is not None
            else "No significant attrition observed."
        )
        return {
            "journey_id": journey.get("journey_id"),
            "completion_rate": completion_rate,
            "completed_stages": completed,
            "total_stages": total,
            "critical_drop_stage": critical_drop,
            "drop_off_points": drop_offs,
            "insight": insight,
        }

    def compute_cohort_retention(
        self,
        cohort_label: str,
        daily_active_user_counts: Dict[str, int],
    ) -> Dict[str, Any]:
        if not daily_active_user_counts:
            return {"cohort_label": cohort_label, "retention_curve": [], "error": "Empty data"}
        sorted_days = sorted(daily_active_user_counts.keys())
        if not sorted_days:
            return {"cohort_label": cohort_label, "retention_curve": []}
        initial = daily_active_user_counts[sorted_days[0]]
        if initial <= 0:
            return {
                "cohort_label": cohort_label,
                "retention_curve": [],
                "error": "Initial cohort size must be > 0",
            }
        retention_curve = []
        for day in sorted_days:
            count = daily_active_user_counts[day]
            retention_curve.append(
                {
                    "day": int(day) if str(day).isdigit() else day,
                    "active_users": count,
                    "retention_rate": round(count / initial, 4),
                }
            )
        day1 = next((r for r in retention_curve if r["day"] == 1), None)
        day7 = next((r for r in retention_curve if r["day"] == 7), None)
        day30 = next((r for r in retention_curve if r["day"] == 30), None)
        return {
            "cohort_label": cohort_label,
            "initial_cohort_size": initial,
            "retention_curve": retention_curve,
            "day_1_retention": day1["retention_rate"] if day1 else None,
            "day_7_retention": day7["retention_rate"] if day7 else None,
            "day_30_retention": day30["retention_rate"] if day30 else None,
            "average_daily_retention": round(
                sum(r["retention_rate"] for r in retention_curve) / len(retention_curve),
                4,
            ),
        }

    def generate_persona_report(
        self,
        persona_name: str,
        max_insights: int = 10,
    ) -> Dict[str, Any]:
        if persona_name not in self.persona_segments:
            raise KeyError(f"Persona {persona_name} not registered")
        persona_info = self.persona_segments[persona_name]
        stats = self._persona_statistics_from_history(persona_name)
        recommendations = persona_info.get("recommended_nudges", [])
        risk_factors = persona_info.get("risk_factors", [])
        insights = [
            f"Persona '{persona_name}' shows strong alignment with "
            f"recommended nudges: {', '.join(recommendations[:5])}."
        ]
        for rf in risk_factors[:max_insights]:
            insights.append(f"Monitor risk factor: {rf}")
        return {
            "persona_name": persona_name,
            "description": persona_info.get("description", ""),
            "traits": persona_info.get("traits", {}),
            "recommended_nudges": recommendations,
            "risk_factors": risk_factors,
            "statistics": stats,
            "insights": insights[:max_insights],
            "generated_at": datetime.datetime.utcnow().isoformat(),
        }

    def _persona_statistics_from_history(self, persona_name: str) -> Dict[str, Any]:
        matching_sessions = []
        for session in self.session_history:
            for match in session.get("persona_matches", []):
                if match.get("persona_name") == persona_name:
                    matching_sessions.append(session)
        total = len(matching_sessions)
        if total == 0:
            return {"total_sessions": 0, "average_confidence": 0.0, "nudge_usage_rate": 0.0}
        avg_confidence = sum(
            s.get("overall_confidence", 0.0) for s in matching_sessions
        ) / total
        nudge_rate = sum(
            1 for s in matching_sessions if s.get("recommended_nudges")
        ) / total
        return {
            "total_sessions": total,
            "average_confidence": round(avg_confidence, 4),
            "nudge_usage_rate": round(nudge_rate, 4),
        }

    def optimize_nudge_timing(
        self,
        user_id: str,
        nudge_id: str,
        time_windows: List[Dict[str, str]],
    ) -> Dict[str, Any]:
        if nudge_id not in self.nudge_library:
            raise KeyError(f"Nudge {nudge_id} not found")
        window_scores = []
        for idx, window in enumerate(time_windows):
            start = window.get("start", "09:00")
            end = window.get("end", "17:00")
            score = round(random.uniform(0.3, 0.95), 4)
            window_scores.append(
                {
                    "window_index": idx,
                    "start": start,
                    "end": end,
                    "expected_engagement_score": score,
                    "recommended": False,
                }
            )
        best = max(window_scores, key=lambda w: w["expected_engagement_score"]) if window_scores else None
        if best:
            best["recommended"] = True
        return {
            "user_id": user_id,
            "nudge_id": nudge_id,
            "timing_recommendations": window_scores,
            "optimal_window": best,
        }

    def evaluate_nudge_performance(
        self,
        nudge_id: str,
        impressions: int,
        clicks: int,
        conversions: int,
        exposures_per_user: Optional[int] = None,
    ) -> Dict[str, Any]:
        if nudge_id not in self.nudge_library:
            raise KeyError(f"Nudge {nudge_id} not found")
        if impressions <= 0:
            raise ValueError("impressions must be greater than 0")
        ctr = clicks / impressions
        cvr = conversions / clicks if clicks > 0 else 0.0
        cpm = 0.0
        cpc = 0.0
        if impressions > 0:
            cpm = (impressions / 1000.0)
            cpc = cpm / clicks if clicks > 0 else 0.0
        lift_score = round((ctr - 0.05) / 0.05, 4) if ctr > 0.05 else -round(
            (0.05 - ctr) / 0.05, 4
        )
        effectiveness = self._compute_nudge_effectiveness(
            impressions, clicks, conversions, nudge_id
        )
        status = "high_performing" if ctr > 0.10 else (
            "moderate" if ctr > 0.04 else "underperforming"
        )
        return {
            "nudge_id": nudge_id,
            "nudge_type": self.nudge_library[nudge_id].get("nudge_type"),
            "impressions": impressions,
            "clicks": clicks,
            "conversions": conversions,
            "ctr": round(ctr, 4),
            "cvr": round(cvr, 4),
            "cpm": round(cpm, 4),
            "cpc": round(cpc, 4),
            "lift_score": lift_score,
            "status": status,
            "effectiveness_score": round(effectiveness, 4),
            "recommendations": self._nudge_performance_recommendations(status, ctr),
        }

    def _compute_nudge_effectiveness(
        self,
        impressions: int,
        clicks: int,
        conversions: int,
        nudge_id: str,
    ) -> float:
        nudge = self.nudge_library.get(nudge_id, {})
        base_expected = nudge.get("expected_impact", 0.1) * impressions
        actual = conversions
        ratio = actual / base_expected if base_expected > 0 else 0.0
        score = min(1.0, max(0.0, ratio))
        return score

    def _nudge_performance_recommendations(
        self, status: str, ctr: float
    ) -> List[str]:
        if status == "high_performing":
            return [
                "Increase exposure to capture more value.",
                "Test with additional persona segments.",
                "Consider extending runtime for longer-horizon effects.",
            ]
        if status == "underperforming":
            return [
                "Review nudge design and messaging.",
                "Test alternative framing or creative.",
                "Check for audience misalignment.",
            ]
        return [
            "Iterate on creative or placement.",
            "Analyze segment-level performance.",
            "Consider adjusting strength or frequency.",
        ]

    def tag_behavior_event(
        self,
        event_id: str,
        tags: List[str],
        confidence: float = 1.0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
        tag_entry = {
            "event_id": event_id,
            "tags": tags,
            "confidence": confidence,
            "metadata": metadata or {},
            "tagged_at": datetime.datetime.utcnow().isoformat(),
            "processed": False,
        }
        self.intervention_log.append(tag_entry)
        return tag_entry

    def summarize_sessions(
        self,
        since: Optional[str] = None,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        filtered = self.session_history
        if user_id:
            filtered = [s for s in filtered if s.get("user_id") == user_id]
        if since:
            filtered = [s for s in filtered if s.get("timestamp", "") >= since]
        if not filtered:
            return {"session_count": 0, "average_confidence": 0.0, "unique_users": 0}
        bias_counts: Dict[str, int] = {}
        nudge_counts: Dict[str, int] = {}
        for session in filtered:
            for bias in session.get("triggered_biases", []):
                b = bias.get("bias")
                bias_counts[b] = bias_counts.get(b, 0) + 1
            for nudge in session.get("recommended_nudges", []):
                nudge_counts[nudge] = nudge_counts.get(nudge, 0) + 1
        return {
            "session_count": len(filtered),
            "unique_users": len({s.get("user_id") for s in filtered}),
            "bias_distribution": bias_counts,
            "nudge_distribution": nudge_counts,
            "average_confidence": round(
                sum(s.get("overall_confidence", 0.0) for s in filtered) / len(filtered),
                4,
            ),
            "time_range": {
                "since": since,
                "user_id": user_id,
            },
        }

    def recommend_intervention(
        self,
        user_id: str,
        current_state: Dict[str, Any],
        recent_events: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        analysis = self.analyze_behavior(user_id, current_state)
        persona_matches = []
        for persona_name, persona_info in self.persona_segments.items():
            if self._match_persona(current_state, persona_info):
                confidence = round(
                    random.uniform(0.5, 0.95), 4
                )
                persona_matches.append(
                    {
                        "persona_name": persona_name,
                        "confidence": confidence,
                        "matched_traits": list(persona_info.get("traits", {}).keys())[:3],
                    }
                )
        analysis["persona_matches"] = persona_matches
        nudge_id = (
            random.choice(list(self.nudge_library.keys()))
            if self.nudge_library
            else None
        )
        nudge = self.nudge_library.get(nudge_id) if nudge_id else None
        return {
            "user_id": user_id,
            "analysis": analysis,
            "persona_matches": persona_matches,
            "suggested_nudge": nudge,
            "intervention_priority": self._priority_label(
                analysis.get("overall_confidence", 0.0)
            ),
            "alternative_nudges": (
                list(self.nudge_library.values())[:5] if self.nudge_library else []
            ),
            "recommended_timing": self._recommended_timing_default(),
            "expected_outcome": self._expected_outcome_description(analysis),
        }

    def _priority_label(self, confidence: float) -> str:
        if confidence >= 0.85:
            return "high"
        if confidence >= 0.65:
            return "medium"
        return "low"

    def _recommended_timing_default(self) -> str:
        return "next_24h"
        
    def _expected_outcome_description(self, analysis: Dict[str, Any]) -> str:
        biases = analysis.get("triggered_biases", [])
        if not biases:
            return "No significant behavioral triggers detected."
        bias_names = [b["bias"] for b in biases[:3]]
        return (
            f"Targeted intervention addressing biases: {', '.join(bias_names)} "
            f"with confidence {analysis.get('overall_confidence', 0.0)}."
        )

    def simulate_behavior(
        self,
        user_id: str,
        scenario_type: str,
        parameters: Dict[str, Any],
        iterations: int = 1000,
    ) -> Dict[str, Any]:
        if iterations <= 0:
            raise ValueError("iterations must be greater than 0")
        results = []
        for _ in range(iterations):
            outcome = random.choices(
                ["success", "failure", "abandon"],
                weights=[0.4, 0.35, 0.25],
                k=1,
            )[0]
            response_time = max(0, random.gauss(5, 2))
            results.append(
                {
                    "iteration": _ + 1,
                    "outcome": outcome,
                    "response_time_seconds": round(response_time, 3),
                    "satisfaction": round(random.uniform(1, 5), 2),
                }
            )
        success_rate = sum(1 for r in results if r["outcome"] == "success") / iterations
        return {
            "user_id": user_id,
            "scenario_type": scenario_type,
            "iterations": iterations,
            "success_rate": round(success_rate, 4),
            "outcome_distribution": {
                outcome: sum(1 for r in results if r["outcome"] == outcome)
                for outcome in ["success", "failure", "abandon"]
            },
            "average_response_time": round(
                sum(r["response_time_seconds"] for r in results) / iterations,
                3,
            ),
            "average_satisfaction": round(
                sum(r["satisfaction"] for r in results) / iterations,
                2,
            ),
            "detailed_results": results[:10],
        }

    def export_state(self, path: str) -> None:
        state = {
            "config": self.config,
            "nudge_library": self.nudge_library,
            "behavior_profiles": self.behavior_profiles,
            "session_history": self.session_history,
            "experiment_registry": self.experiment_registry,
            "habit_loops": self.habit_loops,
            "incentive_systems": self.incentive_systems,
            "persona_segments": self.persona_segments,
            "intervention_log": self.intervention_log,
            "cognitive_biases_index": self.cognitive_biases_index,
            "feedback_data": self.feedback_data,
            "pattern_cache": self.pattern_cache,
            "exported_at": datetime.datetime.utcnow().isoformat(),
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, default=str)

    def import_state(self, path: str) -> None:
        with open(path, "r", encoding="utf-8") as f:
            state = json.load(f)
        self.config = state.get("config", self.config)
        self.nudge_library = state.get("nudge_library", self.nudge_library)
        self.behavior_profiles = state.get("behavior_profiles", self.behavior_profiles)
        self.session_history = state.get("session_history", self.session_history)
        self.experiment_registry = state.get("experiment_registry", self.experiment_registry)
        self.habit_loops = state.get("habit_loops", self.habit_loops)
        self.incentive_systems = state.get("incentive_systems", self.incentive_systems)
        self.persona_segments = state.get("persona_segments", self.persona_segments)
        self.intervention_log = state.get("intervention_log", self.intervention_log)
        self.cognitive_biases_index = state.get("cognitive_biases_index", self.cognitive_biases_index)
        self.feedback_data = state.get("feedback_data", self.feedback_data)
        self.pattern_cache = state.get("pattern_cache", self.pattern_cache)

    def reset_session(self) -> Dict[str, Any]:
        self.session_history = []
        self.intervention_log = []
        self.feedback_data = []
        self.pattern_cache = {}
        return {"status": "reset", "timestamp": datetime.datetime.utcnow().isoformat()}

    def get_nudge(self, nudge_id: str) -> Dict[str, Any]:
        if nudge_id not in self.nudge_library:
            raise KeyError(f"Nudge {nudge_id} not found")
        return self.nudge_library[nudge_id]

    def get_experiment(self, experiment_id: str) -> Dict[str, Any]:
        if experiment_id not in self.experiment_registry:
            raise KeyError(f"Experiment {experiment_id} not found")
        return self.experiment_registry[experiment_id]

    def get_habit_loop(self, loop_id: str) -> Dict[str, Any]:
        if loop_id not in self.habit_loops:
            raise KeyError(f"Habit loop {loop_id} not found")
        return self.habit_loops[loop_id]

    def list_personas(self) -> List[str]:
        return list(self.persona_segments.keys())

    def list_nudges(self) -> List[Dict[str, Any]]:
        return list(self.nudge_library.values())

    def list_experiments(self) -> List[Dict[str, Any]]:
        return list(self.experiment_registry.values())

    def list_habit_loops(self) -> List[Dict[str, Any]]:
        return list(self.habit_loops.values())

    def advanced_analysis(
        self,
        user_ids: List[str],
        analysis_type: str = "comprehensive",
    ) -> Dict[str, Any]:
        analysis_types = ["comprehensive", "quick", "deep", "segment_compare"]
        if analysis_type not in analysis_types:
            raise ValueError(f"analysis_type must be one of {analysis_types}")
        results = []
        for user_id in user_ids:
            analysis = self.analyze_behavior(user_id, {"tags": ["random"], "context": "advanced"})
            intervention = self.recommend_intervention(user_id, {"tags": ["random"], "context": "advanced"})
            results.append(
                {
                    "user_id": user_id,
                    "behavior_analysis": analysis,
                    "intervention_recommendation": intervention,
                }
            )
        return {
            "analysis_type": analysis_type,
            "user_count": len(user_ids),
            "results": results,
            "summary": {
                "total_biases_detected": sum(
                    len(r["behavior_analysis"].get("triggered_biases", []))
                    for r in results
                ),
                "total_nudges_generated": sum(
                    len(r["behavior_analysis"].get("recommended_nudges", []))
                    for r in results
                ),
            },
        }

    def batch_design_nudges(
        self,
        requests: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        nudges = []
        for req in requests:
            nudge = self.design_nudge(
                trigger=req.get("trigger", "unknown"),
                behavior=req.get("behavior", "engagement"),
                context=req.get("context"),
                strength=req.get("strength"),
                nudge_type=req.get("nudge_type"),
            )
            nudges.append(nudge)
        return nudges

    def compute_habit_predictions(
        self,
        loop_id: str,
        horizon_days: int = 30,
    ) -> Dict[str, Any]:
        if loop_id not in self.habit_loops:
            raise KeyError(f"Habit loop {loop_id} not found")
        loop = self.habit_loops[loop_id]
        current_strength = loop.get("loop_strength", 0.5)
        predictions = []
        for day in range(1, horizon_days + 1):
            daily_success_prob = max(0.0, min(1.0, current_strength - 0.01 * math.sin(day / 7 * 2 * math.pi)))
            predicted_outcome = random.choices(
                ["success", "failure"],
                weights=[daily_success_prob, 1 - daily_success_prob],
                k=1,
            )[0]
            predictions.append(
                {
                    "day": day,
                    "predicted_outcome": predicted_outcome,
                    "predicted_strength": round(daily_success_prob, 4),
                }
            )
        return {
            "loop_id": loop_id,
            "loop_strength": current_strength,
            "horizon_days": horizon_days,
            "predictions": predictions,
        }

    def close_ab_test(
        self,
        experiment_id: str,
        stopping_reason: str = "significance_reached",
    ) -> Dict[str, Any]:
        if experiment_id not in self.experiment_registry:
            raise KeyError(f"Experiment {experiment_id} not found")
        experiment = self.experiment_registry[experiment_id]
        if experiment["status"] == "concluded":
            return {
                "experiment_id": experiment_id,
                "status": experiment["status"],
                "message": "Experiment already concluded",
                "ended_at": experiment.get("ended_at"),
            }
        experiment["status"] = "concluded"
        experiment["ended_at"] = datetime.datetime.utcnow().isoformat()
        experiment["stopping_reason"] = stopping_reason
        final_stats = self._compute_intermediate_experiment_stats(experiment)
        experiment["significance_achieved"] = final_stats.get("significance_achieved", False)
        experiment["p_value"] = final_stats.get("p_value")
        experiment["effect_size"] = final_stats.get("effect_size_cohens_h")
        experiment["confidence_interval"] = final_stats.get("confidence_interval_95")
        experiment["recommended_winner"] = (
            experiment["treatment_variant"]
            if final_stats.get("treatment_rate", 0) > final_stats.get("control_rate", 0)
            else experiment["control_variant"]
        )
        return {
            "experiment_id": experiment_id,
            "status": experiment["status"],
            "ended_at": experiment["ended_at"],
            "stopping_reason": stopping_reason,
            "final_stats": final_stats,
            "recommended_winner": experiment["recommended_winner"],
        }

    def run(self, user_input: Optional[str] = None) -> Dict[str, Any]:
        session_id = self._generate_session_id()
        event_data = {"tags": ["runtime", "manual"], "context": user_input or "default_run"}
        analysis = self.analyze_behavior(
            user_id="system",
            event_data=event_data,
        )
        nudge = self.design_nudge(
            trigger="runtime",
            behavior="engagement",
            context={"source": "run_method"},
        )
        self.record_feedback(
            user_id="system",
            event_type="agent_run",
            response_data={"input": user_input, "nudge_id": nudge["nudge_id"]},
        )
        return {
            "agent": "BehavioralScience",
            "session_id": session_id,
            "status": "completed",
            "analysis": analysis,
            "nudge": nudge,
        }

    def calculate_nudge_roi(
        self,
        nudge_id: str,
        cost_per_impression: float,
        conversion_value: float,
        impressions: int,
        conversions: int,
    ) -> Dict[str, Any]:
        if nudge_id not in self.nudge_library:
            raise KeyError(f"Nudge {nudge_id} not found")
        if cost_per_impression < 0 or conversion_value < 0 or impressions < 0 or conversions < 0:
            raise ValueError("Financial parameters must be non-negative")
        total_cost = cost_per_impression * impressions
        total_revenue = conversion_value * conversions
        roi = ((total_revenue - total_cost) / total_cost) if total_cost > 0 else 0.0
        break_even_conversions = total_cost / conversion_value if conversion_value > 0 else float("inf")
        return {
            "nudge_id": nudge_id,
            "total_cost": round(total_cost, 4),
            "total_revenue": round(total_revenue, 4),
            "roi": round(roi, 4),
            "break_even_conversions": round(break_even_conversions, 2),
            "net_profit": round(total_revenue - total_cost, 4),
            "roi_per_impression": round(roi / impressions, 6) if impressions > 0 else 0.0,
        }

    def detect_behavioral_anomalies(
        self,
        user_id: str,
        event_sequence: List[Dict[str, Any]],
        sensitivity: float = 0.7,
    ) -> Dict[str, Any]:
        if not event_sequence:
            raise ValueError("event_sequence must not be empty")
        if not 0.0 <= sensitivity <= 1.0:
            raise ValueError("sensitivity must be between 0.0 and 1.0")
        anomalies = []
        timestamps = []
        for event in event_sequence:
            ts = event.get("timestamp")
            if ts:
                timestamps.append(datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")))
        if len(timestamps) >= 2:
            timestamps.sort()
            gaps = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
            avg_gap = sum(gaps) / len(gaps) if gaps else 0
            std_gap = (sum((g - avg_gap) ** 2 for g in gaps) / len(gaps)) ** 0.5 if gaps else 0
            for i, gap in enumerate(gaps):
                z_score = abs(gap - avg_gap) / std_gap if std_gap > 0 else 0
                if z_score > sensitivity * 3:
                    anomalies.append({
                        "type": "timing_anomaly",
                        "index": i,
                        "gap_seconds": gap,
                        "z_score": round(z_score, 4),
                        "severity": "high" if z_score > 5 else "medium",
                    })
        bias_sequence = []
        for event in event_sequence:
            analysis = self.analyze_behavior(user_id, event)
            bias_sequence.extend(analysis.get("triggered_biases", []))
        unique_biases = list({b["bias"] for b in bias_sequence})
        if len(unique_biases) > 5:
            anomalies.append({
                "type": "bias_surge",
                "unique_biases_count": len(unique_biases),
                "bias_list": unique_biases,
                "severity": "medium",
            })
        return {
            "user_id": user_id,
            "event_count": len(event_sequence),
            "anomaly_count": len(anomalies),
            "anomalies": anomalies,
            "sensitivity_used": sensitivity,
            "detected_at": datetime.datetime.utcnow().isoformat(),
        }

    def generate_user_segment_report(
        self,
        segment_filter: Optional[Dict[str, Any]] = None,
        min_confidence: float = 0.5,
    ) -> Dict[str, Any]:
        segment_filter = segment_filter or {}
        sessions = self.session_history
        if "user_id" in segment_filter:
            sessions = [s for s in sessions if s.get("user_id") == segment_filter["user_id"]]
        if "since" in segment_filter:
            sessions = [s for s in sessions if s.get("timestamp", "") >= segment_filter["since"]]
        filtered_sessions = [
            s for s in sessions if s.get("overall_confidence", 0.0) >= min_confidence
        ]
        persona_distribution: Dict[str, int] = {}
        bias_distribution: Dict[str, int] = {}
        nudge_distribution: Dict[str, int] = {}
        for session in filtered_sessions:
            for match in session.get("persona_matches", []):
                name = match.get("persona_name", "unknown")
                persona_distribution[name] = persona_distribution.get(name, 0) + 1
            for bias in session.get("triggered_biases", []):
                name = bias.get("bias", "unknown")
                bias_distribution[name] = bias_distribution.get(name, 0) + 1
            for nudge in session.get("recommended_nudges", []):
                nudge_distribution[nudge] = nudge_distribution.get(nudge, 0) + 1
        top_personas = sorted(persona_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
        top_biases = sorted(bias_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
        top_nudges = sorted(nudge_distribution.items(), key=lambda x: x[1], reverse=True)[:5]
        return {
            "report_generated_at": datetime.datetime.utcnow().isoformat(),
            "total_sessions_analyzed": len(filtered_sessions),
            "filter_criteria": segment_filter,
            "min_confidence": min_confidence,
            "persona_distribution": dict(top_personas),
            "bias_distribution": dict(top_biases),
            "nudge_distribution": dict(top_nudges),
            "average_confidence": round(
                sum(s.get("overall_confidence", 0.0) for s in filtered_sessions) / len(filtered_sessions), 4
            ) if filtered_sessions else 0.0,
        }

    def compute_power_analysis(
        self,
        baseline_rate: float,
        minimum_detectable_effect: float,
        alpha: float = 0.05,
        desired_power: float = 0.8,
        ratio: float = 1.0,
    ) -> Dict[str, Any]:
        if not 0.0 <= baseline_rate <= 1.0:
            raise ValueError("baseline_rate must be between 0.0 and 1.0")
        if not 0.0 <= minimum_detectable_effect <= 1.0:
            raise ValueError("minimum_detectable_effect must be between 0.0 and 1.0")
        if not 0.0 < alpha < 1.0:
            raise ValueError("alpha must be between 0.0 and 1.0 exclusive")
        if not 0.0 < desired_power < 1.0:
            raise ValueError("desired_power must be between 0.0 and 1.0 exclusive")
        p1 = baseline_rate
        p2 = min(1.0, baseline_rate + minimum_detectable_effect)
        z_alpha = self._normal_ppf(1 - alpha / 2)
        z_beta = self._normal_ppf(desired_power)
        pooled_p = (p1 + p2) / 2
        se_diff = math.sqrt(pooled_p * (1 - pooled_p) * (1 + 1 / ratio))
        n_per_group = math.ceil(((z_alpha + z_beta) ** 2 * pooled_p * (1 - pooled_p)) / ((p1 - p2) ** 2))
        return {
            "baseline_rate": baseline_rate,
            "minimum_detectable_effect": minimum_detectable_effect,
            "alpha": alpha,
            "desired_power": desired_power,
            "required_sample_size_per_group": n_per_group,
            "total_sample_size": n_per_group * (1 + ratio),
            "treatment_rate_assumed": p2,
            "z_alpha": round(z_alpha, 4),
            "z_beta": round(z_beta, 4),
        }

    def validate_experiment_design(
        self,
        control_variant: str,
        treatment_variant: str,
        power: float = 0.8,
        alpha: float = 0.05,
        minimum_sample_size: int = 1000,
    ) -> Dict[str, Any]:
        errors = []
        warnings = []
        if not control_variant or not treatment_variant:
            errors.append("Variant names must not be empty")
        if control_variant == treatment_variant:
            errors.append("Control and treatment variants must be different")
        if not 0.0 < power < 1.0:
            errors.append("power must be between 0.0 and 1.0 exclusive")
        if not 0.0 < alpha < 1.0:
            errors.append("alpha must be between 0.0 and 1.0 exclusive")
        if alpha > 0.1:
            warnings.append("Alpha > 0.1 increases false positive risk")
        if power < 0.7:
            warnings.append("Power < 0.7 increases false negative risk")
        if minimum_sample_size < 100:
            warnings.append("Very small sample size may lead to unreliable results")
        is_valid = len(errors) == 0
        return {
            "is_valid": is_valid,
            "control_variant": control_variant,
            "treatment_variant": treatment_variant,
            "power": power,
            "alpha": alpha,
            "minimum_sample_size": minimum_sample_size,
            "errors": errors,
            "warnings": warnings,
        }

    def schedule_nudge(
        self,
        nudge_id: str,
        user_id: str,
        scheduled_at: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if nudge_id not in self.nudge_library:
            raise KeyError(f"Nudge {nudge_id} not found")
        try:
            scheduled_time = datetime.datetime.fromisoformat(scheduled_at.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("scheduled_at must be a valid ISO 8601 timestamp")
        schedule_id = hashlib.md5(f"{nudge_id}-{user_id}-{scheduled_at}".encode("utf-8")).hexdigest()[:8]
        entry = {
            "schedule_id": schedule_id,
            "nudge_id": nudge_id,
            "user_id": user_id,
            "scheduled_at": scheduled_at,
            "status": "scheduled",
            "created_at": datetime.datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "attempts": 0,
            "delivered": False,
        }
        if "scheduled_nudges" not in self.pattern_cache:
            self.pattern_cache["scheduled_nudges"] = []
        self.pattern_cache["scheduled_nudges"].append(entry)
        return entry

    def cancel_nudge(self, schedule_id: str) -> Dict[str, Any]:
        scheduled_nudges = self.pattern_cache.get("scheduled_nudges", [])
        for entry in scheduled_nudges:
            if entry.get("schedule_id") == schedule_id:
                if entry.get("delivered"):
                    raise ValueError("Cannot cancel a nudge that has already been delivered")
                entry["status"] = "cancelled"
                entry["cancelled_at"] = datetime.datetime.utcnow().isoformat()
                return {
                    "schedule_id": schedule_id,
                    "status": "cancelled",
                    "nudge_id": entry.get("nudge_id"),
                    "user_id": entry.get("user_id"),
                }
        raise KeyError(f"Scheduled nudge {schedule_id} not found")

    def get_behavioral_trends(
        self,
        metric: str = "bias_detection_rate",
        window_size: int = 7,
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        valid_metrics = ["bias_detection_rate", "nudge_acceptance_rate", "habit_success_rate", "experiment_conversion_rate"]
        if metric not in valid_metrics:
            raise ValueError(f"metric must be one of {valid_metrics}")
        sessions = self.session_history
        if user_id:
            sessions = [s for s in sessions if s.get("user_id") == user_id]
        if not sessions:
            return {"metric": metric, "trend_data": [], "trend_direction": "stable", "slope": 0.0}
        daily_metrics: Dict[str, float] = {}
        for session in sessions:
            day = session.get("timestamp", "")[:10]
            if not day:
                continue
            if metric == "bias_detection_rate":
                val = 1.0 if session.get("triggered_biases") else 0.0
            elif metric == "nudge_acceptance_rate":
                val = 1.0 if session.get("recommended_nudges") else 0.0
            elif metric == "habit_success_rate":
                val = session.get("statistics", {}).get("success_rate", 0.0)
            else:
                val = 0.0
            daily_metrics[day] = daily_metrics.get(day, 0.0) + val
        trend_data = [
            {"date": day, "metric_value": round(count, 4)}
            for day, count in sorted(daily_metrics.items())
        ]
        if len(trend_data) >= 2:
            x = list(range(len(trend_data)))
            y = [d["metric_value"] for d in trend_data]
            mean_x = sum(x) / len(x)
            mean_y = sum(y) / len(y)
            num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
            den = sum((xi - mean_x) ** 2 for xi in x)
            slope = num / den if den != 0 else 0.0
            direction = "increasing" if slope > 0.01 else "decreasing" if slope < -0.01 else "stable"
        else:
            slope = 0.0
            direction = "stable"
        return {
            "metric": metric,
            "window_size": window_size,
            "trend_data": trend_data[-window_size:],
            "trend_direction": direction,
            "slope": round(slope, 6),
            "data_points": len(trend_data),
        }

    def export_audit_log(self, path: str, since: Optional[str] = None) -> None:
        audit_entries = []
        for session in self.session_history:
            entry_ts = session.get("timestamp", "")
            if since and entry_ts < since:
                continue
            audit_entries.append({
                "type": "session_analysis",
                "timestamp": entry_ts,
                "user_id": session.get("user_id"),
                "session_id": session.get("session_id"),
                "details": {
                    "biases_detected": len(session.get("triggered_biases", [])),
                    "nudges_recommended": len(session.get("recommended_nudges", [])),
                },
            })
        for entry in self.intervention_log:
            entry_ts = entry.get("tagged_at", "")
            if since and entry_ts < since:
                continue
            audit_entries.append({
                "type": "intervention_tag",
                "timestamp": entry_ts,
                "event_id": entry.get("event_id"),
                "details": {"tags": entry.get("tags")},
            })
        for entry in self.feedback_data:
            entry_ts = entry.get("timestamp", "")
            if since and entry_ts < since:
                continue
            audit_entries.append({
                "type": "feedback",
                "timestamp": entry_ts,
                "user_id": entry.get("user_id"),
                "details": {"event_type": entry.get("event_type"), "sentiment": entry.get("sentiment")},
            })
        audit_entries.sort(key=lambda x: x.get("timestamp", ""))
        with open(path, "w", encoding="utf-8") as f:
            json.dump({
                "audit_log": audit_entries,
                "exported_at": datetime.datetime.utcnow().isoformat(),
                "total_entries": len(audit_entries),
            }, f, indent=2, default=str)

    def import_audit_log(self, path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        entries = data.get("audit_log", [])
        imported_sessions = 0
        imported_interventions = 0
        imported_feedback = 0
        for entry in entries:
            etype = entry.get("type")
            if etype == "session_analysis":
                self.session_history.append(entry.get("details", {}))
                imported_sessions += 1
            elif etype == "intervention_tag":
                self.intervention_log.append(entry.get("details", {}))
                imported_interventions += 1
            elif etype == "feedback":
                self.feedback_data.append(entry.get("details", {}))
                imported_feedback += 1
        return {
            "imported_sessions": imported_sessions,
            "imported_interventions": imported_interventions,
            "imported_feedback": imported_feedback,
            "total_imported": imported_sessions + imported_interventions + imported_feedback,
        }

    def compute_bias_correlation_matrix(self) -> Dict[str, Any]:
        bias_names = list(self.cognitive_biases_index.keys())
        n = len(bias_names)
        matrix: Dict[str, Dict[str, float]] = {}
        for b1 in bias_names:
            matrix[b1] = {}
            for b2 in bias_names:
                if b1 == b2:
                    matrix[b1][b2] = 1.0
                else:
                    co_occurrence = 0
                    total = 0
                    for session in self.session_history:
                        biases = {b["bias"] for b in session.get("triggered_biases", [])}
                        if b1 in biases and b2 in biases:
                            co_occurrence += 1
                        if b1 in biases or b2 in biases:
                            total += 1
                    matrix[b1][b2] = round(co_occurrence / total, 4) if total > 0 else 0.0
        return {
            "bias_names": bias_names,
            "matrix": matrix,
            "computed_at": datetime.datetime.utcnow().isoformat(),
        }

    def optimize_persona_thresholds(
        self,
        persona_name: str,
        target_precision: float = 0.9,
        max_iterations: int = 50,
    ) -> Dict[str, Any]:
        if persona_name not in self.persona_segments:
            raise KeyError(f"Persona {persona_name} not registered")
        persona = self.persona_segments[persona_name]
        triggers = persona.get("triggers", [])
        best_threshold = 1.0
        best_score = 0.0
        for threshold in [x / 20.0 for x in range(1, 21)]:
            tp = 0
            fp = 0
            fn = 0
            for session in self.session_history:
                matched = self._match_persona(session, persona)
                actual_match = any(
                    m.get("persona_name") == persona_name
                    for m in session.get("persona_matches", [])
                )
                if matched and actual_match:
                    tp += 1
                elif matched and not actual_match:
                    fp += 1
                elif not matched and actual_match:
                    fn += 1
            precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
            f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
            if f1 > best_score:
                best_score = f1
                best_threshold = threshold
            if best_score >= target_precision:
                break
        return {
            "persona_name": persona_name,
            "optimal_threshold": round(best_threshold, 4),
            "achieved_f1": round(best_score, 4),
            "iterations_run": min(max_iterations, 20),
            "target_precision": target_precision,
        }

    def detect_habit_decay(
        self,
        loop_id: str,
        decay_threshold: float = 0.3,
    ) -> Dict[str, Any]:
        if loop_id not in self.habit_loops:
            raise KeyError(f"Habit loop {loop_id} not found")
        loop = self.habit_loops[loop_id]
        history = loop.get("reinforcement_history", [])
        if len(history) < 7:
            return {
                "loop_id": loop_id,
                "decay_detected": False,
                "reason": "Insufficient history (minimum 7 records required)",
            }
        recent = history[-7:]
        older = history[-14:-7] if len(history) >= 14 else history[:-7]
        recent_success = sum(1 for r in recent if r.get("trigger_occurred") and r.get("reward_given")) / len(recent)
        older_success = sum(1 for r in older if r.get("trigger_occurred") and r.get("reward_given")) / len(older) if older else recent_success
        decay_detected = (older_success - recent_success) > decay_threshold
        return {
            "loop_id": loop_id,
            "habit_name": loop.get("habit_name"),
            "current_strength": round(loop.get("loop_strength", 0.5), 4),
            "recent_success_rate": round(recent_success, 4),
            "older_success_rate": round(older_success, 4) if older else None,
            "decay_detected": decay_detected,
            "decay_magnitude": round(older_success - recent_success, 4) if older else 0.0,
            "recommendation": (
                "Increase reward salience or simplify cue-response pathway"
                if decay_detected else "No action required"
            ),
        }

    def recommend_nudge_sequence(
        self,
        user_id: str,
        max_nudges: int = 3,
        strategy: str = "diversity",
    ) -> Dict[str, Any]:
        valid_strategies = ["diversity", "reinforcement", "escalation", "simplification"]
        if strategy not in valid_strategies:
            raise ValueError(f"strategy must be one of {valid_strategies}")
        analysis = self.analyze_behavior(user_id, {"tags": ["sequence_request"], "context": strategy})
        candidates = analysis.get("recommended_nudges", [])
        if not candidates:
            candidates = ["default_effect"]
        selected = []
        if strategy == "diversity":
            selected = list(dict.fromkeys(candidates))[:max_nudges]
        elif strategy == "reinforcement":
            selected = candidates[:max_nudges]
        elif strategy == "escalation":
            selected = sorted(candidates, key=lambda n: self._nudge_strength_estimate(n), reverse=True)[:max_nudges]
        else:
            selected = ["simplification", "default_effect", "reminders"][:max_nudges]
        sequence = []
        for idx, nudge_type in enumerate(selected):
            nudge = self.design_nudge(
                trigger=f"sequence_step_{idx+1}",
                behavior="engagement",
                nudge_type=nudge_type,
                strength=min(1.0, 0.3 + (idx * 0.2)),
            )
            sequence.append({
                "step": idx + 1,
                "nudge_id": nudge["nudge_id"],
                "nudge_type": nudge_type,
                "strength": nudge["strength"],
                "rationale": f"Step {idx+1}: {self._describe_nudge(nudge_type, 'sequence', 'engagement')}",
            })
        return {
            "user_id": user_id,
            "strategy": strategy,
            "sequence": sequence,
            "total_steps": len(sequence),
        }

    def _nudge_strength_estimate(self, nudge_type: str) -> float:
        base = {
            "default_effect": 0.25,
            "social_norm": 0.22,
            "commitment_device": 0.18,
            "reminders": 0.15,
            "simplification": 0.13,
            "framing": 0.12,
            "incentive_alignment": 0.20,
            "peer_comparison": 0.10,
            "scarcity": 0.40,
            "loss_aversion_framing": 0.35,
        }
        return base.get(nudge_type, 0.1)

    def compute_intervention_effectiveness(
        self,
        intervention_id: str,
        pre_metrics: Dict[str, float],
        post_metrics: Dict[str, float],
    ) -> Dict[str, Any]:
        metrics_report = {}
        for metric_name in pre_metrics:
            if metric_name not in post_metrics:
                continue
            pre = pre_metrics[metric_name]
            post = post_metrics[metric_name]
            absolute_change = post - pre
            relative_change = ((post - pre) / pre) if pre != 0 else 0.0
            metrics_report[metric_name] = {
                "pre_value": pre,
                "post_value": post,
                "absolute_change": round(absolute_change, 4),
                "relative_change": round(relative_change, 4),
                "percent_change": round(relative_change * 100, 2),
            }
        overall_effectiveness = sum(
            abs(v["relative_change"]) for v in metrics_report.values()
        ) / len(metrics_report) if metrics_report else 0.0
        return {
            "intervention_id": intervention_id,
            "metrics_report": metrics_report,
            "overall_effectiveness_score": round(overall_effectiveness, 4),
            "positive_metrics": sum(1 for v in metrics_report.values() if v["relative_change"] > 0),
            "negative_metrics": sum(1 for v in metrics_report.values() if v["relative_change"] < 0),
            "neutral_metrics": sum(1 for v in metrics_report.values() if v["relative_change"] == 0),
        }

    def get(self, item: str, default: Any = None) -> Any:
        if item in self.nudge_library:
            return self.nudge_library[item]
        if item in self.experiment_registry:
            return self.experiment_registry[item]
        if item in self.habit_loops:
            return self.habit_loops[item]
        if item in self.incentive_systems:
            return self.incentive_systems[item]
        return default

    def __repr__(self) -> str:
        return (
            f"BehavioralScienceAgent("
            f"personas={len(self.persona_segments)}, "
            f"biases={len(self.cognitive_biases_index)}, "
            f"nudges={len(self.nudge_library)}, "
            f"experiments={len(self.experiment_registry)}, "
            f"habits={len(self.habit_loops)})"
        )
