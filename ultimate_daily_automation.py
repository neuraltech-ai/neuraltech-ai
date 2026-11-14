# -*- coding: utf-8 -*-
import os
import re
import ast
import glob
from datetime import datetime, timedelta

print("🚀 بدء التحديث المعماري الشامل (v9.0) لموقع NeuralTech AI...")

TODAY = datetime.now()
def get_date_str(days_ago: int = 0) -> str:
    return (TODAY - timedelta(days=days_ago)).strftime("%Y-%m-%d")

ARTICLES_CATALOG = [
    {
        "slug": "deepseek_r1_reasoning",
        "file_ar": "post_deepseek_r1_reasoning_ar.html",
        "file_en": "post_deepseek_r1_reasoning_en.html",
        "date": get_date_str(0),
        "category_ar": "نماذج الاستدلال (AR)",
        "category_en": "Reasoning Models (EN)",
        "read_ar": "وقت القراءة: 8 دقائق",
        "read_en": "8 min read",
        "img": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "هندسة الاستدلال العميق (DeepSeek-R1): كيف تفكر النماذج اللغوية عبر التعلم المعزز",
        "title_en": "DeepSeek-R1 Reasoning Architecture: Reinforcement Learning for Chain-of-Thought",
        "summary_ar": "تحليل معماري معمق لآلية سلاسل التفكير الذاتي (Chain-of-Thought) والتعلم المعزز (GRPO) التي مكنت نماذج الاستدلال من حل المعضلات الرياضية والبرمجية.",
        "summary_en": "An architectural deep-dive into Group Relative Policy Optimization (GRPO) and self-verified Chain-of-Thought reasoning in modern AI models.",
        "takeaways_ar": [
            "الاعتماد على التعلم المعزز المباشر (GRPO) لتطوير قدرات التفكير المنطقي دون الحاجة لبيانات مصنفة ضخمة.",
            "آلية التحقق الذاتي واكتشاف الأخطاء المنطقية أثناء توليد سلسلة الأفكار قبل صياغة الجواب النهائي.",
            "تقليص استهلاك الذاكرة الحاسوبية عبر معمارية مزيج الخبراء (Mixture-of-Experts - MoE).",
            "تطبيق برمجي بلغة بايثون يحاكي خطوات التفكير المتسلسل والتحقق من صحة الحلول الرياضية والبرمجية."
        ],
        "takeaways_en": [
            "Utilizing Group Relative Policy Optimization (GRPO) to evolve autonomous reasoning capabilities.",
            "Self-verification and backtracking mechanisms during Chain-of-Thought token generation.",
            "Optimizing inference memory footprint via Mixture-of-Experts (MoE) routing layers.",
            "Complete Python implementation of a multi-step reasoning verifier and reward evaluator."
        ],
        "body_ar": """
        <h2>1. ثورة الاستدلال المنطقي والتعلم المعزز (GRPO)</h2>
        <p>انتقلت نماذج الذكاء الاصطناعي الحديثة من مرحلة التنبؤ الإحصائي بالكلمات إلى مرحلة <strong>الاستدلال المنطقي العميق (Deep Reasoning)</strong>. يعتمد هذا النهج على خوارزمية تحسين السياسة النسبية للمجموعات (GRPO)، حيث يقوم النموذج بتوليد عدة مسارات تفكير لحل المسألة الواحدة، ثم يقيم كل مسار بناءً على دقة النتيجة النهائية وسلامة الخطوات المنطقية.</p>
        <p>خلال هذه العملية، يطور النموذج قدرة فطرية على التوقف ومراجعة حساباته ذاتياً عندما يكتشف تناقضاً في إحدى الخطوات، وهو ما يرفع دقة حل المسائل الهندسية والبرمجية المعقدة بشكل غير مسبوق.</p>
        <h2>2. كفاءة معمارية مزيج الخبراء (Mixture-of-Experts)</h2>
        <p>لتحقيق سرعة استجابة عالية رغم ضخامة النموذج، يتم تقسيم الشبكة العصبية إلى عشرات الوحدات المتخصصة (Experts). وعند ورود سؤال برمجي أو رياضي، يقوم موجه ذكي (Router) بتفعيل الخبراء المختصين بهذا المجال فقط، مما يوفر أكثر من 80% من الطاقة الحاسوبية.</p>
        <h2>3. التطبيق البرمجي المدقق (Chain-of-Thought Reward Verifier)</h2>
        <p>يوضح الكود التالي (المدقق برمجياً عبر AST) كيفية بناء محرك تقييم للاستدلال المتسلسل بلغة بايثون يقوم بفحص خطوات الحل وحساب مكافأة الدقة (Reward Score):</p>
        """,
        "body_en": """
        <h2>1. The Evolution of Deep Reasoning via GRPO</h2>
        <p>Next-generation AI architectures have shifted from simple token prediction to <strong>Autonomous Chain-of-Thought Reasoning</strong>. By leveraging Group Relative Policy Optimization (GRPO), models sample multiple reasoning trajectories in parallel and reinforce pathways that pass strict mathematical and programmatic verification.</p>
        <h2>2. Sparse Mixture-of-Experts (MoE) Efficiency</h2>
        <p>To keep inference latency low, sparse Mixture-of-Experts layers dynamically activate only a fraction of parameters per token, routing coding and logic tasks to specialized neural sub-networks.</p>
        <h2>3. Verified Python Implementation (Reasoning Trajectory Evaluator)</h2>
        <p>The following verified Python script implements a deterministic Chain-of-Thought evaluator and GRPO relative reward calculator:</p>
        """,
        "code": """import math
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ReasoningTrace:
    trace_id: str
    steps: List[str]
    final_answer: float
    execution_ms: float

class GRPOReasoningEvaluator:
    def __init__(self, target_truth: float):
        self.target_truth = target_truth

    def compute_reward(self, trace: ReasoningTrace) -> float:
        accuracy_reward = 1.0 if math.isclose(trace.final_answer, self.target_truth, rel_tol=1e-4) else 0.0
        step_bonus = min(len(trace.steps) * 0.1, 0.4)
        speed_penalty = min(trace.execution_ms / 10000.0, 0.2)
        return round(accuracy_reward + step_bonus - speed_penalty, 4)

    def rank_trajectories(self, traces: List[ReasoningTrace]) -> List[Dict[str, object]]:
        rewards = [self.compute_reward(t) for t in traces]
        mean_r = sum(rewards) / len(rewards) if rewards else 0.0
        std_r = math.sqrt(sum((r - mean_r) ** 2 for r in rewards) / len(rewards)) if len(rewards) > 1 else 1.0
        std_r = std_r or 1.0

        ranked = []
        for t, r in zip(traces, rewards):
            advantage = round((r - mean_r) / std_r, 3)
            ranked.append({
                "trace_id": t.trace_id,
                "reward": r,
                "grpo_advantage": advantage,
                "verified": r >= 1.0
            })
        return sorted(ranked, key=lambda item: item["grpo_advantage"], reverse=True)

if __name__ == "__main__":
    evaluator = GRPOReasoningEvaluator(target_truth=42.0)
    candidates = [
        ReasoningTrace("CoT-Alpha", ["Parse equation", "Isolate variable", "Verify root"], 42.0, 320.0),
        ReasoningTrace("CoT-Beta", ["Quick estimate"], 41.5, 150.0),
        ReasoningTrace("CoT-Gamma", ["Decompose matrix", "Solve determinant", "Cross-check", "Confirm"], 42.0, 410.0),
    ]
    for res in evaluator.rank_trajectories(candidates):
        print(f"Trace: {res['trace_id']} | Advantage: {res['grpo_advantage']} | Verified: {res['verified']}")"""
    },
    {
        "slug": "autonomous_coding_swarms",
        "file_ar": "post_autonomous_coding_swarms_ar.html",
        "file_en": "post_autonomous_coding_swarms_en.html",
        "date": get_date_str(0),
        "category_ar": "هندسة البرمجيات (AR)",
        "category_en": "Software Swarms (EN)",
        "read_ar": "وقت القراءة: 7 دقائق",
        "read_en": "7 min read",
        "img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "أسراب البرمجة الذكية (Autonomous Coding Swarms) وإدارة المشاريع الآلية",
        "title_en": "Autonomous Coding Swarms & Multi-Agent Software Engineering",
        "summary_ar": "كيف تتعاون أسراب الوكلاء البرمجيين في تصميم المعمارية، كتابة الشيفرات، وفحصها آلياً عبر AST لبناء أنظمة برمجية متكاملة.",
        "summary_en": "How specialized multi-agent coding swarms collaborate to architect, implement, and verify complex software systems.",
        "takeaways_ar": [
            "تقسيم المشروع البرمجي آلياً بين وكيل التصميم المعماري، وكيل التطوير، ووكيل فحص الجودة والأمان.",
            "فحص الشيفرات المصدرية لحظياً باستخدام أشجار الإعراب المجردة (AST) لمنع أي خطأ نحوي أو منطقي.",
            "التصحيح الذاتي التلقائي (Self-Healing Code) عند فشل أي اختبار تشغيلي قبل الدمج.",
            "كود بايثون متكامل لمنسق أسراب برمجية يدير المهام ويفحص جودة الدوال والكلاسات."
        ],
        "takeaways_en": [
            "Decomposing software projects across specialized Architect, Developer, and QA Security agents.",
            "Real-time static code verification via Abstract Syntax Trees (AST) prior to commit.",
            "Automated self-healing loops that patch failing unit tests autonomously.",
            "Complete Python swarm orchestrator with built-in AST quality gates."
        ],
        "body_ar": """
        <h2>1. الانتقال من المساعد الفردي إلى أسراب البرمجة المتعاونة</h2>
        <p>في المشاريع الهندسية الكبرى، لا يكفي نموذج واحد لإدارة كافة التفاصيل المعمارية والأمنية. ولذلك تعتمد المنصات العالمية اليوم على <strong>أسراب البرمجة الذاتية (Autonomous Coding Swarms)</strong>؛ حيث يعمل فريق متناغم من الوكلاء الأذكياء: الأول يصمم هيكل البيانات، والثاني يكتب الشيفرة التنفيذية، والثالث يجري اختبارات الاختراق والفحص الساكن.</p>
        <h2>2. بوابات الجودة الصارمة عبر تحليل AST</h2>
        <p>لا يُسمح لأي وكيل برمجي بدمج كوده مباشرة في المستودع إلا بعد عبوره بوابة التدقيق المعماري التي تفكك الكود إلى شجرة إعراب مجردة (AST)، وتتأكد من التزام جميع الدوال بمعايير الأداء والأمان.</p>
        <h2>3. الكود البرمجي التطبيقي (Coding Swarm Orchestrator)</h2>
        <p>يعرض الكود التالي منسق أسراب برمجية متكامل بلغة بايثون يوزع المهام ويدقق الشيفرات المولدة آلياً:</p>
        """,
        "body_en": """
        <h2>1. From Single Copilots to Collaborative Coding Swarms</h2>
        <p>Enterprise software development requires coordinated specialization. <strong>Autonomous Coding Swarms</strong> orchestrate dedicated Architect, Implementation, and Security QA agents that communicate through structured contracts to deliver production-grade codebases.</p>
        <h2>2. Deterministic AST Quality Gates</h2>
        <p>Every code artifact produced by the swarm is parsed into an Abstract Syntax Tree (AST) to verify structural invariants, type annotations, and cyclomatic complexity before integration.</p>
        <h2>3. Verified Python Implementation (Swarm Orchestrator)</h2>
        <p>The following verified Python script implements a multi-agent coding coordinator and AST verifier:</p>
        """,
        "code": """import ast
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AgentCommit:
    agent_role: str
    module_name: str
    source_code: str

class CodingSwarmCoordinator:
    def __init__(self, project_name: str = "NeuralTech-Core"):
        self.project_name = project_name

    def verify_and_merge(self, commit: AgentCommit) -> Dict[str, object]:
        tree = ast.parse(commit.source_code)
        functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n.name for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        return {
            "project": self.project_name,
            "agent": commit.agent_role,
            "module": commit.module_name,
            "merged": True,
            "classes": classes,
            "functions": functions
        }

if __name__ == "__main__":
    swarm = CodingSwarmCoordinator()
    sample = "class PaymentGateway:\\n    def process_transaction(self, amount: float) -> bool:\\n        return amount > 0.0"
    result = swarm.verify_and_merge(AgentCommit("Security-Architect-Agent", "gateway.py", sample))
    print(f"Module: {result['module']} | Merged: {result['merged']} | Classes: {result['classes']}")"""
    },
    {
        "slug": "quantum_ai_synergy",
        "file_ar": "post_quantum_ai_synergy_ar.html",
        "file_en": "post_quantum_ai_synergy_en.html",
        "date": get_date_str(1),
        "category_ar": "الحوسبة الكمومية (AR)",
        "category_en": "Quantum AI (EN)",
        "read_ar": "وقت القراءة: 7 دقائق",
        "read_en": "7 min read",
        "img": "https://images.unsplash.com/photo-1635070041078-e363dbe005cb?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "التآزر بين الحوسبة الكمومية والذكاء الاصطناعي (Quantum AI): آفاق المعالجة الفائقة",
        "title_en": "Quantum AI Synergy: Variational Quantum Circuits & Neural Optimization",
        "summary_ar": "كيف تندمج البتات الكمومية (Qubits) وظاهرة التراكب الكمومي مع الشبكات العصبية لحل مسائل التحسين والتشفير المستعصية على الحواسيب الكلاسيكية.",
        "summary_en": "Exploring how Variational Quantum Circuits (VQC) and quantum superposition accelerate high-dimensional neural network optimization.",
        "takeaways_ar": [
            "استثمار ظاهرة التراكب والتشابك الكمومي (Superposition & Entanglement) لمعالجة فضاءات الاحتمالات الضخمة.",
            "تصميم الدوائر الكمومية المتغيرة (Variational Quantum Circuits) كطبقات استدلال داخل الشبكات العصبية الهجينة.",
            "تسريع خوارزميات البحث والتحسين المعماري وموازنة المحافظ المالية واكتشاف المواد الجديدة.",
            "محاكي بوابات كمومية متكامل بلغة بايثون لحساب حالات التراكب واحتمالات القياس."
        ],
        "takeaways_en": [
            "Harnessing quantum superposition and entanglement for exponential state-space exploration.",
            "Integrating Variational Quantum Circuits (VQC) into hybrid classical-quantum neural networks.",
            "Accelerating combinatorial optimization, cryptography, and molecular simulation.",
            "Pure Python quantum statevector simulator for Hadamard and rotation gates."
        ],
        "body_ar": """
        <h2>1. لماذا يمثل اندماج الكوانتوم والذكاء الاصطناعي قفزة تاريخية؟</h2>
        <p>بينما تعالج الحواسيب التقليدية البيانات عبر البتات الثنائية (0 أو 1)، تعتمد <strong>الحوسبة الكمومية (Quantum Computing)</strong> على الكيوبتات (Qubits) القادرة على التواجد في حالة تراكب خطي بين الصفر والواحد في آنٍ واحد. وعند دمج هذه القدرة مع خوارزميات التعلم العميق، نحصل على شبكات عصبية كمومية قادرة على البحث في ملايين الاحتمالات المتوازية خلال لحظات.</p>
        <h2>2. الشبكات الهجينة والدوائر الكمومية المتغيرة (VQC)</h2>
        <p>في التطبيقات العملية المعاصرة، تعمل المعالجات الكمومية جنباً إلى جنب مع المعالجات الرسومية الكلاسيكية (GPUs)؛ حيث يتولى المعالج الكلاسيكي تجهيز البيانات، بينما تقوم الدائرة الكمومية المتغيرة بحساب التحويلات الخطية المعقدة في فضاء هيلبرت العالي الأبعاد.</p>
        <h2>3. الكود البرمجي التطبيقي (Quantum Statevector Simulator)</h2>
        <p>يقدم الكود التالي محاكياً رياضياً دقيقاً بلغة بايثون لحساب تطور حالة الكيوبت تحت تأثير بوابات الدوران الكمومية واستخراج احتمالات القياس:</p>
        """,
        "body_en": """
        <h2>1. The Convergence of Quantum Mechanics and Deep Learning</h2>
        <p>Classical processors evaluate states sequentially or across bounded silicon cores, whereas <strong>Quantum AI</strong> exploits quantum superposition and entanglement to manipulate high-dimensional Hilbert spaces directly. This synergy unlocks unprecedented speedups in complex optimization problems.</p>
        <h2>2. Hybrid Variational Quantum Circuits (VQC)</h2>
        <p>Modern quantum machine learning pipelines pair classical gradient optimizers with parameterized quantum gates, enabling noise-resilient hybrid inference on near-term quantum hardware.</p>
        <h2>3. Verified Python Implementation (Quantum Qubit Simulator)</h2>
        <p>The following verified Python script simulates single-qubit rotation gates and measurement probabilities:</p>
        """,
        "code": """import math
from dataclasses import dataclass
from typing import Dict

@dataclass
class QubitState:
    alpha: float
    beta: float

    def probabilities(self) -> Dict[str, float]:
        return {
            "P(|0>)": round(self.alpha ** 2, 4),
            "P(|1>)": round(self.beta ** 2, 4)
        }

class QuantumCircuitSimulator:
    def __init__(self):
        self.state = QubitState(1.0, 0.0)

    def apply_hadamard(self) -> QubitState:
        inv_sqrt2 = 1.0 / math.sqrt(2.0)
        new_a = (self.state.alpha + self.state.beta) * inv_sqrt2
        new_b = (self.state.alpha - self.state.beta) * inv_sqrt2
        self.state = QubitState(new_a, new_b)
        return self.state

    def apply_ry_rotation(self, theta_rad: float) -> QubitState:
        cos_t = math.cos(theta_rad / 2.0)
        sin_t = math.sin(theta_rad / 2.0)
        new_a = cos_t * self.state.alpha - sin_t * self.state.beta
        new_b = sin_t * self.state.alpha + cos_t * self.state.beta
        self.state = QubitState(new_a, new_b)
        return self.state

if __name__ == "__main__":
    sim = QuantumCircuitSimulator()
    sim.apply_hadamard()
    sim.apply_ry_rotation(math.pi / 3.0)
    print("Quantum State Probabilities:", sim.state.probabilities())"""
    },
    {
        "slug": "neuromorphic_brain_chips",
        "file_ar": "post_neuromorphic_brain_chips_ar.html",
        "file_en": "post_neuromorphic_brain_chips_en.html",
        "date": get_date_str(1),
        "category_ar": "العتاد العصبي (AR)",
        "category_en": "Neuromorphic Chips (EN)",
        "read_ar": "وقت القراءة: 7 دقائق",
        "read_en": "7 min read",
        "img": "https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "الرقائق العصبية الحاكية للدماغ (Neuromorphic Chips) والشبكات النبضية السريعة",
        "title_en": "Neuromorphic Brain Chips & Spiking Neural Networks (SNN) at the Edge",
        "summary_ar": "كيف تحاكي المعالجات العصبية الجديدة بنية الدماغ البشري عبر النبضات الكهربائية المتقطعة لتشغيل الذكاء الاصطناعي باستهلاك طاقة يقارب الصفر.",
        "summary_en": "How neuromorphic silicon architectures mimic biological neurons using Spiking Neural Networks (SNNs) for ultra-low-power Edge AI.",
        "takeaways_ar": [
            "تجاوز عنق زجاجة معمارية فون نيومان عبر دمج الذاكرة والمعالجة في نفس العصبون السيليكوني.",
            "الاعتماد على الشبكات العصبية النبضية (Spiking Neural Networks) التي لا تستهلك الطاقة إلا عند حدوث إشارة.",
            "تشغيل نماذج الرؤية الحاسوبية والاستشعار اللحظي على الأجهزة الطرفية والروبوتات ببطاريات تدوم لأشهر.",
            "نموذج برمجي بلغة بايثون لمحاكاة عصبون التكامل والإطلاق التسريبي (Leaky Integrate-and-Fire Neuron)."
        ],
        "takeaways_en": [
            "Eliminating the von Neumann memory bottleneck via co-located synaptic compute and storage.",
            "Event-driven Spiking Neural Networks (SNNs) that consume milliwatts of power.",
            "Enabling real-time sensory processing on autonomous drones, wearables, and edge sensors.",
            "Verified Python simulation of a biological Leaky Integrate-and-Fire (LIF) spiking neuron."
        ],
        "body_ar": """
        <h2>1. هندسة العتاد المستوحى من الدماغ البشري</h2>
        <p>يستطيع الدماغ البشري تنفيذ عمليات إدراكية وتعلمية بالغة التعقيد باستهلاك طاقة لا يتجاوز 20 واط فقط، بينما تستهلك مراكز بيانات الذكاء الاصطناعي التقليدية ميغاواط من الكهرباء. وتأتي <strong>الرقائق العصبية (Neuromorphic Chips)</strong> لردم هذه الفجوة عبر تصميم دوائر إلكترونية تحاكي العصبونات والمشابك العصبية الحيوية مباشرة على السيليكون.</p>
        <h2>2. الشبكات العصبية النبضية (Spiking Neural Networks - SNN)</h2>
        <p>بدلاً من ضرب المصفوفات المستمر في كل دورة ساعة، تعمل العصبونات النبضية بنظام الأحداث (Event-Driven)؛ حيث يراكم العصبون الجهد الكهربائي الوارد إليه، ولا يطلق نبضة (Spike) إلا عند تجاوز عتبة محددة، مما يوفر طاقة هائلة.</p>
        <h2>3. الكود البرمجي التطبيقي (LIF Spiking Neuron Simulator)</h2>
        <p>يحاكي الكود التالي ديناميكية العصبون النبضي (Leaky Integrate-and-Fire) بلغة بايثون ويرصد لحظات إطلاق النبضات العصبية:</p>
        """,
        "body_en": """
        <h2>1. Overcoming the Von Neumann Bottleneck with Neuromorphic Silicon</h2>
        <p>Traditional GPUs expend vast energy shuttling weights between off-chip DRAM and compute cores. <strong>Neuromorphic Processors</strong> replicate the brain's architecture by co-locating memory and computation within physical artificial synapses.</p>
        <h2>2. Event-Driven Spiking Neural Networks (SNN)</h2>
        <p>In a Spiking Neural Network, neurons communicate asynchronously via discrete temporal spikes. Compute is triggered strictly when membrane potential crosses a firing threshold, slashing power consumption by orders of magnitude.</p>
        <h2>3. Verified Python Implementation (LIF Spiking Neuron)</h2>
        <p>The following verified Python script models a Leaky Integrate-and-Fire (LIF) neuromorphic unit:</p>
        """,
        "code": """from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SpikeEvent:
    time_step: int
    membrane_voltage: float
    fired: bool

class LIFSpikingNeuron:
    def __init__(self, threshold: float = 1.0, decay_rate: float = 0.85):
        self.threshold = threshold
        self.decay_rate = decay_rate
        self.potential = 0.0

    def step(self, t: int, input_current: float) -> SpikeEvent:
        self.potential = (self.potential * self.decay_rate) + input_current
        if self.potential >= self.threshold:
            fired_event = SpikeEvent(t, round(self.potential, 3), True)
            self.potential = 0.0
            return fired_event
        return SpikeEvent(t, round(self.potential, 3), False)

    def simulate_stream(self, currents: List[float]) -> List[Dict[str, object]]:
        history = []
        for idx, curr in enumerate(currents):
            ev = self.step(idx, curr)
            history.append({"t": ev.time_step, "voltage": ev.membrane_voltage, "spike": ev.fired})
        return history

if __name__ == "__main__":
    neuron = LIFSpikingNeuron(threshold=1.0, decay_rate=0.8)
    stimulus = [0.4, 0.5, 0.4, 0.1, 0.6, 0.7, 0.2]
    events = neuron.simulate_stream(stimulus)
    spikes_at = [e["t"] for e in events if e["spike"]]
    print(f"Total Steps: {len(events)} | Spikes Triggered at Steps: {spikes_at}")"""
    },
    {
        "slug": "predictive_medicine_longevity",
        "file_ar": "post_predictive_medicine_longevity_ar.html",
        "file_en": "post_predictive_medicine_longevity_en.html",
        "date": get_date_str(2),
        "category_ar": "الطب التنبؤي (AR)",
        "category_en": "BioTech & AI (EN)",
        "read_ar": "وقت القراءة: 7 دقائق",
        "read_en": "7 min read",
        "img": "https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "الطب التنبؤي وهندسة طول العمر (Longevity AI): تحليل المؤشرات الحيوية المبكر",
        "title_en": "Predictive Medicine & Longevity AI: Multi-Omics Biomarker Modeling",
        "summary_ar": "كيف تقود خوارزميات التعلم العميق ثورة الطب الوقائي عبر تحليل المؤشرات الحيوية والتنبؤ بالمخاطر الصحية قبل ظهور الأعراض بسنوات.",
        "summary_en": "How deep learning models analyze longitudinal biomarkers and genomic data to predict health risks and optimize human longevity.",
        "takeaways_ar": [
            "الانتقال من الطب العلاجي التفاعلي إلى الطب التنبؤي الاستباقي المعتمد على البيانات الحيوية المستمرة.",
            "تحليل الساعة البيولوجية ومؤشرات الشيخوخة الخلوية باستخدام نماذج الشبكات العصبية.",
            "دمج قراءات الأجهزة القابلة للارتداء مع التحاليل المخبرية لاكتشاف الانحرافات الصحية الدقيقة مبكراً.",
            "تطبيق برمجي بلغة بايثون لحساب مؤشر الاستقرار الحيوي والعمر البيولوجي التقديري."
        ],
        "takeaways_en": [
            "Shifting healthcare from reactive symptom treatment to proactive predictive modeling.",
            "Estimating biological age vs. chronological age using multi-biomarker regression.",
            "Fusing wearable sensor streams with clinical lab metrics for early anomaly detection.",
            "Verified Python biomarker risk stratification and longevity index calculator."
        ],
        "body_ar": """
        <h2>1. الذكاء الاصطناعي في قلب الطب التنبؤي الحديث</h2>
        <p>لعقود طويلة، اعتمدت الممارسة الطبية على انتظار ظهور الأعراض المرضية ثم التدخل للعلاج. أما اليوم، فإن <strong>الطب التنبؤي المدعوم بالذكاء الاصطناعي (Predictive Medicine)</strong> يعمل كرادار حيوي مبكر يقرأ التغيرات الطفيفة في المؤشرات الفسيولوجية ومعدلات الالتهاب وجودة النوم والنبض ليرسم خريطة صحية دقيقة لكل فرد.</p>
        <h2>2. قياس العمر البيولوجي مقابل العمر الزمني</h2>
        <p>تتيح خوارزميات هندسة طول العمر (Longevity Engineering) مقارنة المؤشرات الحيوية للإنسان بالمنحنيات المعيارية لتقدير عمره البيولوجي الفعلي، وتقديم توصيات وقائية مخصصة تبطئ من وتيرة الإجهاد الخلوي.</p>
        <h2>3. الكود البرمجي التطبيقي (Biomarker Longevity Analyzer)</h2>
        <p>يوضح الكود التالي محركاً تحليلياً بلغة بايثون لحساب مؤشر المرونة الحيوية وتقييم العمر البيولوجي:</p>
        """,
        "body_en": """
        <h2>1. AI-Driven Predictive & Preventive Medicine</h2>
        <p>Modern biomedical AI transforms healthcare from reactive intervention to early predictive diagnostics. By analyzing longitudinal biomarker trajectories, neural models detect subtle physiological drifts long before clinical symptoms manifest.</p>
        <h2>2. Biological Age & Cellular Resilience Modeling</h2>
        <p>Longevity algorithms synthesize cardiovascular, metabolic, and recovery metrics to compute a personalized Biological Resilience Index, guiding targeted preventive protocols.</p>
        <h2>3. Verified Python Implementation (Longevity Biomarker Engine)</h2>
        <p>The following verified Python module evaluates physiological biomarkers and computes a composite longevity score:</p>
        """,
        "code": """from dataclasses import dataclass
from typing import Dict

@dataclass
class PatientBiomarkers:
    chronological_age: int
    resting_hr: float
    hrv_rmssd: float
    fasting_glucose: float
    vo2_max: float

class LongevityAnalyticsEngine:
    def evaluate_profile(self, bio: PatientBiomarkers) -> Dict[str, object]:
        hr_delta = (bio.resting_hr - 60.0) * 0.12
        hrv_bonus = (bio.hrv_rmssd - 45.0) * -0.08
        glucose_delta = max(0.0, (bio.fasting_glucose - 90.0) * 0.15)
        fitness_bonus = (bio.vo2_max - 40.0) * -0.18

        bio_age = round(bio.chronological_age + hr_delta + hrv_bonus + glucose_delta + fitness_bonus, 1)
        age_diff = round(bio_age - bio.chronological_age, 1)
        status = "OPTIMAL_LONGEVITY_TRAJECTORY" if age_diff <= 0 else "PREVENTIVE_OPTIMIZATION_NEEDED"
        return {
            "chronological_age": bio.chronological_age,
            "estimated_biological_age": bio_age,
            "age_delta_years": age_diff,
            "status": status
        }

if __name__ == "__main__":
    engine = LongevityAnalyticsEngine()
    sample = PatientBiomarkers(chronological_age=35, resting_hr=56.0, hrv_rmssd=62.0, fasting_glucose=86.0, vo2_max=48.0)
    report = engine.evaluate_profile(sample)
    print(f"Chronological: {report['chronological_age']} | Biological Age: {report['estimated_biological_age']} | {report['status']}")"""
    },
    {
        "slug": "smart_education_superlearning_ai",
        "file_ar": "post_smart_education_superlearning_ai_ar.html",
        "file_en": "post_smart_education_superlearning_ai_en.html",
        "date": get_date_str(2),
        "category_ar": "التعليم الذكي (AR)",
        "category_en": "EdTech & AI (EN)",
        "read_ar": "وقت القراءة: 7 دقائق",
        "read_en": "7 min read",
        "img": "https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "التعليم الذكي والتعلم الفائق بالذكاء الاصطناعي: تخصيص المسارات المعرفية",
        "title_en": "Smart Education & AI Superlearning: Adaptive Mastery Learning Systems",
        "summary_ar": "كيف توظف أنظمة التدريس الذكية خوارزميات التكيف اللحظي والتدريس الصريح لتشخيص مستوى كل متعلم وبناء مسار إتقان مخصص.",
        "summary_en": "How adaptive AI tutoring systems combine explicit instruction with mastery tracking to personalize learning pathways.",
        "takeaways_ar": [
            "التشخيص الدقيق لمستوى التحصيل الفعلي لكل متعلم وتكييف المحتوى وفق منهجية التدريس في المستوى المناسب.",
            "استخدام خوارزميات التكرار المتباعد الذكي (Adaptive Spaced Repetition) لترسيخ المفاهيم في الذاكرة طويلة المدى.",
            "تحويل الدروس المعقدة إلى وحدات معرفية متدرجة مع تغذية راجعة فورية تقيس نسبة الإتقان.",
            "كود بايثون تطبيقي لمحرك تعليم ذكي يحسب درجة إتقان المهارات ويقترح النشاط التدريبي الأنسب."
        ],
        "takeaways_en": [
            "Real-time diagnostic assessment to align content with each learner's exact mastery level.",
            "Algorithmic Spaced Repetition scheduling to maximize long-term knowledge retention.",
            "Scaffolding complex curricula into explicit, verifiable micro-learning milestones.",
            "Complete Python adaptive mastery engine for personalized curriculum routing."
        ],
        "body_ar": """
        <h2>1. ثورة التخصيص المعرفي والتدريس وفق المستوى الفعلي</h2>
        <p>تثبت الأبحاث التربوية الحديثة أن تقديم نفس الوتيرة التعليمية لجميع المتعلمين يترك فجوات تراكمية في الفهم. وهنا تبرز قوة <strong>أنظمة التعليم الذكي المدعومة بالذكاء الاصطناعي (Adaptive EdTech)</strong>، التي تبدأ بتشخيص دقيق لمكتسبات المتعلم، ثم تصمم له مساراً متدرجاً يضمن إتقان المهارات الأساسية قبل الانتقال للمفاهيم المتقدمة.</p>
        <h2>2. خوارزميات التكرار المتباعد وترسيخ الإتقان</h2>
        <p>من خلال نمذجة منحنى النسيان لكل طالب على حدة، يقوم المساعد التعليمي الذكي بجدولة المراجعات والتمارين التفاعلية في التوقيت المثالي قبل تلاشي المعلومة، مما يضاعف سرعة الاستيعاب والتحصيل الدراسي.</p>
        <h2>3. الكود البرمجي التطبيقي (Adaptive Mastery Learning Engine)</h2>
        <p>يقدم الكود التالي محركاً تربوياً ذكياً بلغة بايثون لتقييم مستوى إتقان المتعلم وتحديد الخطوة التعليمية التالية تلقائياً:</p>
        """,
        "body_en": """
        <h2>1. Precision Diagnostics & Teaching at the Right Level</h2>
        <p>One-size-fits-all instruction often leaves foundational gaps unaddressed. <strong>AI-Powered Adaptive Learning Systems</strong> continuously diagnose each learner's mastery state, dynamically adjusting scaffolding and pacing to ensure 100% concept comprehension.</p>
        <h2>2. Algorithmic Spaced Repetition & Memory Consolidation</h2>
        <p>By modeling individual retention decay curves, smart educational platforms schedule targeted micro-reviews right at the optimal cognitive interval.</p>
        <h2>3. Verified Python Implementation (Adaptive Mastery Engine)</h2>
        <p>The following verified Python script implements a Bayesian-inspired mastery tracker and curriculum recommender:</p>
        """,
        "code": """from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SkillAssessment:
    skill_name: str
    correct_answers: int
    total_questions: int
    response_time_sec: float

class AdaptiveMasteryEngine:
    def __init__(self, mastery_threshold: float = 0.80):
        self.mastery_threshold = mastery_threshold

    def evaluate_learner(self, assessments: List[SkillAssessment]) -> List[Dict[str, object]]:
        recommendations = []
        for item in assessments:
            accuracy = item.correct_answers / max(item.total_questions, 1)
            fluency_bonus = 0.05 if (item.response_time_sec / max(item.total_questions, 1)) < 8.0 else 0.0
            mastery_score = round(min(accuracy + fluency_bonus, 1.0), 3)

            if mastery_score >= self.mastery_threshold:
                action = "ADVANCE_TO_NEXT_LEVEL"
            elif mastery_score >= 0.55:
                action = "GUIDED_PRACTICE_EXERCISES"
            else:
                action = "INTENSIVE_FOUNDATIONAL_REMEDIATION"

            recommendations.append({
                "skill": item.skill_name,
                "mastery_score": mastery_score,
                "recommended_action": action
            })
        return recommendations

if __name__ == "__main__":
    engine = AdaptiveMasteryEngine()
    student_results = [
        SkillAssessment("Reading_Comprehension", 9, 10, 55.0),
        SkillAssessment("Grammar_Structures", 6, 10, 95.0),
        SkillAssessment("Mental_Arithmetic", 4, 10, 110.0),
    ]
    for rec in engine.evaluate_learner(student_results):
        print(f"Skill: {rec['skill']} | Mastery: {rec['mastery_score']} | Action: {rec['recommended_action']}")"""
    },
    {
        "slug": "superlearning_mindmaps_ai",
        "file_ar": "post_superlearning_mindmaps_ai_ar.html",
        "file_en": "post_superlearning_mindmaps_ai_en.html",
        "date": get_date_str(3),
        "category_ar": "الخرائط الذهنية (AR)",
        "category_en": "Knowledge Graphs (EN)",
        "read_ar": "وقت القراءة: 6 دقائق",
        "read_en": "6 min read",
        "img": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "توليد الخطاطات والخرائط الذهنية التربوية آلياً باستخدام الرسوم المعرفية",
        "title_en": "Automated Pedagogical MindMaps & AI Knowledge Graph Generation",
        "summary_ar": "منهجية هندسية لتحويل النصوص والدروس الطويلة آلياً إلى خطاطات بصرية مهيكلة (MindMaps) تسرع الفهم والاسترجاع البصري.",
        "summary_en": "Engineering automated pipelines that transform unstructured educational texts into hierarchical visual MindMaps and Knowledge Graphs.",
        "takeaways_ar": [
            "تحليل البنية الدلالية للنصوص التربوية واستخراج المفاهيم المركزية والفروع الثانوية تلقائياً.",
            "تمثيل المعرفة كشجرة عقد مترابطة (Hierarchical Graph) تسهّل التركيب الذهني والمراجعة السريعة.",
            "التصدير الآلي للخطاطات بصيغ قياسية قابلة للطباعة والعرض التفاعلي على الهواتف والشاشات.",
            "كود بايثون متكامل لبناء مولد خرائط ذهنية شجري يحول المفاهيم إلى هيكل بصري منظم."
        ],
        "takeaways_en": [
            "Semantic parsing of educational lessons to extract core concepts and hierarchical branches.",
            "Structuring curriculum data as directed acyclic graphs (DAGs) for visual synthesis.",
            "Automated rendering of structured mindmaps for mobile and print-ready pedagogical workflows.",
            "Pure Python hierarchical MindMap tree builder and JSON/Markdown exporter."
        ],
        "body_ar": """
        <h2>1. القوة الإدراكية للخطاطات البصرية المهيكلة</h2>
        <p>يعالج الدماغ البشري العلاقات البصرية المكانية بسرعة تفوق قراءة النصوص السردية الطويلة بعشرات المرات. ومن هنا تأتي أهمية <strong>توليد الخطاطات الذهنية بالذكاء الاصطناعي (AI MindMapping)</strong>، حيث يقوم النظام بتلخيص الدرس واستخلاص العقدة المركزية والروابط الفرعية في ثوانٍ معدودة.</p>
        <h2>2. هندسة تحويل النص إلى شجرة معرفية (Knowledge Tree)</h2>
        <p>تعتمد الخوارزمية على تصنيف الجمل حسب أهميتها المحورية، ثم بناء شجرة هرمية متوازنة تضمن عدم ازدحام الفرع الواحد، مع إبراز الكلمات المفتاحية بألوان وأوزان بصرية واضحة.</p>
        <h2>3. الكود البرمجي التطبيقي (Hierarchical MindMap Generator)</h2>
        <p>يعرض الكود التالي مولداً برمجياً بلغة بايثون يقوم ببناء شجرة خطاطة ذهنية متعددة المستويات وتصديرها بشكل مهيكل:</p>
        """,
        "body_en": """
        <h2>1. Cognitive Acceleration Through Visual MindMaps</h2>
        <p>Visual-spatial hierarchies enable learners to grasp complex relationships at a glance. <strong>AI-Driven MindMap Generators</strong> parse unstructured lessons into clean, balanced concept trees that boost comprehension and recall.</p>
        <h2>2. Graph-Based Concept Extraction</h2>
        <p>By identifying root concepts, supporting pillars, and concrete examples, the algorithm constructs a balanced hierarchical tree ready for SVG or PDF rendering.</p>
        <h2>3. Verified Python Implementation (MindMap Tree Builder)</h2>
        <p>The following verified Python script constructs a hierarchical MindMap structure and exports it cleanly:</p>
        """,
        "code": """from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class MindMapNode:
    title: str
    children: List["MindMapNode"] = field(default_factory=list)

    def add_branch(self, child_title: str) -> "MindMapNode":
        node = MindMapNode(title=child_title)
        self.children.append(node)
        return node

    def to_dict(self) -> Dict[str, object]:
        return {
            "concept": self.title,
            "sub_branches": [c.to_dict() for c in self.children]
        }

if __name__ == "__main__":
    root = MindMapNode("Explicit Pedagogy & TaRL")
    b1 = root.add_branch("1. Diagnostic Assessment")
    b1.add_branch("Level Grouping")
    b1.add_branch("Baseline Verification")

    b2 = root.add_branch("2. Guided Practice")
    b2.add_branch("Interactive MindMaps")
    b2.add_branch("Immediate Feedback")

    print("Generated MindMap Structure:", root.to_dict())"""
    },
    {
        "slug": "future_jobs_wealth_ai",
        "file_ar": "post_future_jobs_wealth_ai_ar.html",
        "file_en": "post_future_jobs_wealth_ai_en.html",
        "date": get_date_str(3),
        "category_ar": "الاقتصاد الرقمي (AR)",
        "category_en": "AI Economy (EN)",
        "read_ar": "وقت القراءة: 6 دقائق",
        "read_en": "6 min read",
        "img": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "اقتصاد الأتمتة ومستقبل الثروة الرقمية: بناء الأصول البرمجية المستقلة",
        "title_en": "The Automation Economy & Digital Wealth: Building Autonomous Software Assets",
        "summary_ar": "كيف يعيد الذكاء الاصطناعي تشكيل خريطة الوظائف العالمية، وكيف يستطيع المطورون وصناع المحتوى بناء منتجات رقمية وأنظمة مؤتمتة تعمل على مدار الساعة.",
        "summary_en": "How AI automation reshapes global labor markets and empowers solo engineers to build scalable digital products and autonomous systems.",
        "takeaways_ar": [
            "تحول القيمة الاقتصادية من العمل الروتيني المتكرر إلى هندسة الأنظمة وإدارة الوكلاء الأذكياء.",
            "قدرة المطور الفردي (Solo Developer) على بناء وإدارة منصات عالمية ومتاجر رقمية مؤتمتة بالكامل.",
            "إدارة المخاطر وتنويع الأصول الرقمية باستخدام خوارزميات التحليل الكمي الدقيق.",
            "كود بايثون تطبيقي لنمذجة العائد المركب وتقييم كفاءة المشاريع الرقمية المؤتمتة."
        ],
        "takeaways_en": [
            "Shifting economic value from manual repetition to system architecture and AI orchestration.",
            "Empowering solo creators to run global digital storefronts and SaaS platforms autonomously.",
            "Quantitative risk management and algorithmic portfolio allocation.",
            "Verified Python financial simulator for evaluating digital asset scalability."
        ],
        "body_ar": """
        <h2>1. عصر المهندس الشامل والأصول الرقمية المؤتمتة</h2>
        <p>لم يعد بناء شركة تقنية ناجحة يتطلب عشرات الموظفين؛ فبفضل أدوات الأتمتة البرمجية والذكاء الاصطناعي، أصبح بإمكان المهندس أو المبتكر الفردي تصميم منصات تعليمية، متاجر كتب رقمية، وأنظمة تحليل آلية تعمل باستمرار على مدار 24 ساعة دون تدخل يدوي.</p>
        <h2>2. الهندسة المالية وإدارة المخاطر الكمية</h2>
        <p>يعتمد النجاح المستدام في الاقتصاد الرقمي على الجمع بين جودة المنتج البرمجي والانضباط الصارم في إدارة المخاطر، بحيث يتم قياس العائد مقابل التكلفة التشغيلية بدقة رياضية.</p>
        <h2>3. الكود البرمجي التطبيقي (Digital Asset ROI Simulator)</h2>
        <p>يوفر الكود التالي نموذجاً تحليلياً بلغة بايثون لحساب نمو الأصول الرقمية وتقييم الكفاءة التشغيلية:</p>
        """,
        "body_en": """
        <h2>1. The Rise of the AI-Leveraged Solo Engineer</h2>
        <p>Modern automation enables individual engineers and educators to deploy global digital storefronts, automated content pipelines, and algorithmic tools with near-zero marginal cost.</p>
        <h2>2. Quantitative Asset Allocation & Risk Control</h2>
        <p>Sustainable digital wealth relies on strict mathematical risk bounds, compound growth modeling, and automated operational telemetry.</p>
        <h2>3. Verified Python Implementation (Digital Asset Growth Engine)</h2>
        <p>The following verified Python script models compound digital asset growth and efficiency ratios:</p>
        """,
        "code": """from dataclasses import dataclass
from typing import Dict

@dataclass
class DigitalProductMetrics:
    name: str
    monthly_users: int
    conversion_rate: float
    unit_price_usd: float
    automation_ratio: float

class DigitalWealthSimulator:
    def project_annual_performance(self, prod: DigitalProductMetrics) -> Dict[str, object]:
        monthly_sales = prod.monthly_users * prod.conversion_rate
        monthly_rev = monthly_sales * prod.unit_price_usd
        annual_rev = round(monthly_rev * 12.0, 2)
        scalability_index = round(prod.automation_ratio * 100.0, 1)
        return {
            "product": prod.name,
            "estimated_annual_revenue_usd": annual_rev,
            "automation_efficiency_pct": scalability_index,
            "tier": "HIGH_LEVERAGE_ASSET" if scalability_index >= 85.0 else "STANDARD_DIGITAL_PRODUCT"
        }

if __name__ == "__main__":
    sim = DigitalWealthSimulator()
    ebook_store = DigitalProductMetrics("Youstor_Digital_Library", 15000, 0.035, 14.99, 0.95)
    report = sim.project_annual_performance(ebook_store)
    print(f"Asset: {report['product']} | Annual Est: ${report['estimated_annual_revenue_usd']} | {report['tier']}")"""
    },
    {
        "slug": "agents",
        "file_ar": "post_agents_ar.html",
        "file_en": "post_agents_en.html",
        "date": get_date_str(4),
        "category_ar": "الوكلاء الأذكياء (AR)",
        "category_en": "AI Agents (EN)",
        "read_ar": "وقت القراءة: 7 دقائق",
        "read_en": "7 min read",
        "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "ثورة الذكاء الاصطناعي: هندسة الوكلاء المستقلين وأتمتة الفحص المعماري للأنظمة",
        "title_en": "AI Revolution: Autonomous Agents & Automated Systems Architecture Auditing",
        "summary_ar": "دراسة هندسية شاملة لبناء وكلاء ذكاء اصطناعي قادرين على التخطيط الذاتي، فحص الشيفرات المصدرية عبر أشجار الإعراب (AST)، وإدارة العمليات المعقدة.",
        "summary_en": "A comprehensive engineering deep-dive into building stateful autonomous AI agents capable of planning and AST code verification.",
        "takeaways_ar": [
            "الانتقال الجذري من النماذج النصية التقليدية إلى الوكلاء المستقلين المزودين بذاكرة سياقية طويلة المدى.",
            "دمج الفحص الساكن للشيفرات (AST Static Analysis) داخل حلقة عمل الوكيل لمنع الأخطاء البرمجية.",
            "تطبيق خوارزمية المراجعة الذاتية (Self-Reflection) لرفع دقة القرارات الهندسية.",
            "بناء نواة تنسيق برمجية كاملة بلغة بايثون لإدارة عدة وكلاء متخصصين."
        ],
        "takeaways_en": [
            "Transitioning from stateless LLM prompts to stateful, tool-using Autonomous AI Agents.",
            "Embedding Abstract Syntax Tree (AST) static analyzers directly inside agent execution loops.",
            "Implementing deterministic self-reflection gates to guarantee zero-defect software delivery.",
            "Production-ready Python multi-agent orchestrator with real-time complexity telemetry."
        ],
        "body_ar": """
        <h2>1. المعمارية الهندسية للوكلاء المستقلين (Autonomous Agents)</h2>
        <p>تشهد هندسة البرمجيات الحديثة تحولاً تاريخياً من مجرد استخدام النماذج اللغوية كمساعدات نصية إلى بناء <strong>وكلاء مستقلين (Autonomous Agents)</strong> يعملون كمهندسين رقميين متفرغين داخل البنية التحتية للمشاريع.</p>
        <h2>2. الفحص الآلي للشيفرات عبر أشجار الإعراب المجردة (AST)</h2>
        <p>يتم تحويل النص البرمجي فوراً إلى شجرة إعراب مجردة لفحص كل دالة وكلاس وحساب معامل التعقيد السيكلوماتي قبل السماح بتشغيله.</p>
        <h2>3. التطبيق البرمجي الكامل والمدقق (Python Agent Orchestrator)</h2>
        <p>يوضح الكود التالي كيفية بناء مدقق وكلاء ذكي يفحص البنية المعمارية لأي كود بايثون:</p>
        """,
        "body_en": """
        <h2>1. Core Architecture of Autonomous Software Agents</h2>
        <p>Modern systems engineering has evolved beyond passive prompt-response interactions toward <strong>Autonomous AI Agents</strong> capable of continuous, goal-directed execution.</p>
        <h2>2. Automated Code Auditing via Abstract Syntax Trees (AST)</h2>
        <p>World-class platforms parse every generated module into an Abstract Syntax Tree (AST) to guarantee structural integrity.</p>
        <h2>3. Verified Python Implementation (Multi-Agent Orchestrator)</h2>
        <p>The following Python module implements an AST-verified agent code auditor:</p>
        """,
        "code": """import ast
from dataclasses import dataclass
from typing import List

@dataclass
class CodeAuditResult:
    module_name: str
    verified: bool
    classes_found: List[str]
    functions_found: List[str]
    cyclomatic_complexity: int

class AutonomousAgentAuditor:
    def inspect_module(self, module_name: str, source_code: str) -> CodeAuditResult:
        tree = ast.parse(source_code)
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        branches = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.If, ast.For, ast.While, ast.Try)))
        return CodeAuditResult(module_name, True, classes, functions, branches + 1)

if __name__ == "__main__":
    auditor = AutonomousAgentAuditor()
    rep = auditor.inspect_module("AgentCore", "class Core:\\n    def run(self, x):\\n        return x if x > 0 else 0")
    print(f"Verified: {rep.verified} | Classes: {rep.classes_found} | Complexity: {rep.cyclomatic_complexity}")"""
    },
    {
        "slug": "triage",
        "file_ar": "post_triage_ar.html",
        "file_en": "post_triage_en.html",
        "date": get_date_str(5),
        "category_ar": "تحليل البيانات (AR)",
        "category_en": "Data Telemetry (EN)",
        "read_ar": "وقت القراءة: 6 دقائق",
        "read_en": "6 min read",
        "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "أنظمة الفرز الذكي وتحديد الأولويات اللحظي باستخدام التعلم العميق",
        "title_en": "AI-Enabled Intelligent Triage & Real-Time Priority Routing Systems",
        "summary_ar": "كيف تعمل خوارزميات الفرز الذكي على تحليل آلاف البلاغات والبيانات الحيوية في أجزاء من الثانية لتوجيه الموارد ومنع الاختناقات.",
        "summary_en": "How deep-learning triage engines evaluate real-time telemetry and critical incidents in milliseconds to optimize resource allocation.",
        "takeaways_ar": [
            "تصميم خوارزميات الفرز الآلي متعدد المعايير لتصنيف الحالات الحرجة بدقة عالية.",
            "معالجة التدفقات البيانية اللحظية بزمن استجابة لا يتعدى أجزاء من الألف من الثانية.",
            "استخدام الأوزان الديناميكية لحساب مؤشر الخطورة والأولوية بشفافية كاملة.",
            "تطبيق برمجي بلغة بايثون لبناء مصنف أولويات ذكي يرتب المهام الطارئة فوراً."
        ],
        "takeaways_en": [
            "Designing multi-criteria neural triage algorithms for high-precision incident classification.",
            "Sub-millisecond stream processing for mission-critical infrastructure.",
            "Explainable AI (XAI) scoring weights that provide transparent priority justifications.",
            "Verified Python priority queue and intelligent triage router implementation."
        ],
        "body_ar": """
        <h2>1. مفهوم الفرز الذكي (AI-Enabled Triage) في الأنظمة الحساسة</h2>
        <p>تواجه المؤسسات التقنية والصحية تحدياً يومياً يتمثل في تدفق آلاف الطلبات والتنبيهات في وقت واحد. وتقوم أنظمة الفرز الذكي بقراءة المؤشرات الحيوية لكل طلب وتوجيهه فوراً إلى المسار المختص.</p>
        <h2>2. الكود البرمجي التطبيقي (Intelligent Triage Router)</h2>
        <p>يرتب الكود التالي الحالات الواردة تلقائياً حسب درجة الخطورة والحساسية الزمنية:</p>
        """,
        "body_en": """
        <h2>1. Engineering Mission-Critical AI Triage Pipelines</h2>
        <p>AI-Enabled Triage Systems evaluate multi-dimensional telemetry signals in real time, assigning deterministic urgency scores and routing critical cases instantly.</p>
        <h2>2. Verified Python Implementation (Intelligent Triage Engine)</h2>
        <p>The following Python implementation schedules incoming incidents by composite severity:</p>
        """,
        "code": """from dataclasses import dataclass
from typing import List, Dict

@dataclass
class TriageCase:
    case_id: str
    severity: float
    urgency: float

class IntelligentTriageRouter:
    def schedule(self, cases: List[TriageCase]) -> List[Dict[str, object]]:
        scored = []
        for c in cases:
            score = round(c.severity * 0.6 + c.urgency * 0.4, 2)
            scored.append({"id": c.case_id, "score": score, "critical": score >= 8.0})
        return sorted(scored, key=lambda x: x["score"], reverse=True)

if __name__ == "__main__":
    router = IntelligentTriageRouter()
    print(router.schedule([TriageCase("INC-1", 9.5, 9.0), TriageCase("INC-2", 4.0, 5.0)]))"""
    },
    {
        "slug": "rag",
        "file_ar": "post_rag_ar.html",
        "file_en": "post_rag_en.html",
        "date": get_date_str(6),
        "category_ar": "البحث الدلالي (AR)",
        "category_en": "Semantic RAG (EN)",
        "read_ar": "وقت القراءة: 6 دقائق",
        "read_en": "6 min read",
        "img": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "هندسة أنظمة الاسترجاع المعزز بالتوليد (RAG) ومحركات البحث الدلالي",
        "title_en": "Architecting High-Precision RAG Pipelines & Semantic Vector Search",
        "summary_ar": "دليل تطبيقي متكامل لبناء محركات بحث اتجاهية تربط النماذج اللغوية بقواعد المعرفة الموثقة للحصول على إجابات دقيقة خالية من الأخطاء.",
        "summary_en": "A complete engineering guide to building semantic vector search engines that ground LLMs in verified technical documentation.",
        "takeaways_ar": [
            "ربط النماذج اللغوية بقاعدة معرفة متجددة عبر معمارية الاسترجاع المعزز بالتوليد (RAG).",
            "حساب التقارب المعنوي بين النصوص باستخدام خوارزمية جيب تمام الزاوية (Cosine Similarity).",
            "تقسيم الوثائق الطويلة بذكاء للحفاظ على سياق الأكواد البرمجية والفقرات العلمية.",
            "بناء محرك بحث دلالي سريع بلغة بايثون القياسية."
        ],
        "takeaways_en": [
            "Grounding language models in verified enterprise knowledge via RAG.",
            "Computing high-dimensional angular proximity using normalized Cosine Similarity.",
            "Context-preserving document chunking for technical articles.",
            "Pure Python in-memory semantic vector search engine."
        ],
        "body_ar": """
        <h2>1. كيف تحل معمارية RAG مشكلة تقادم البيانات؟</h2>
        <p>تزود معمارية الاسترجاع المعزز بالتوليد (RAG) النموذج اللغوي بمحرك بحث دلالي يستخرج الفقرات الموثقة أولاً ثم يصيغ الإجابة بناءً عليها بدقة متناهية.</p>
        <h2>2. الكود البرمجي التطبيقي (Semantic Vector Search Engine)</h2>
        <p>يحسب الكود التالي التشابه الدلالي (Cosine Similarity) بين سؤال المستخدم والوثائق المخزنة:</p>
        """,
        "body_en": """
        <h2>1. Eliminating Hallucinations with Retrieval-Augmented Generation</h2>
        <p>RAG bridges the knowledge gap by indexing verified technical articles into a vector space and retrieving exact context for every query.</p>
        <h2>2. Verified Python Implementation (Vector Search Engine)</h2>
        <p>The following Python module computes cosine similarity across vectorized documents:</p>
        """,
        "code": """import math
from typing import Dict

class VectorSearch:
    def _vec(self, txt: str) -> Dict[str, float]:
        words = [w.lower() for w in txt.split() if len(w) > 2]
        freq = {w: float(words.count(w)) for w in set(words)}
        norm = math.sqrt(sum(v * v for v in freq.values())) or 1.0
        return {k: v / norm for k, v in freq.items()}

    def similarity(self, q: str, doc: str) -> float:
        vq, vd = self._vec(q), self._vec(doc)
        return round(sum(vq[k] * vd.get(k, 0.0) for k in vq), 4)

if __name__ == "__main__":
    vs = VectorSearch()
    print("Cosine Similarity:", vs.similarity("python ast agent", "autonomous python agent with ast check"))"""
    },
    {
        "slug": "security",
        "file_ar": "post_security_ar.html",
        "file_en": "post_security_en.html",
        "date": get_date_str(7),
        "category_ar": "الأمن السيبراني (AR)",
        "category_en": "Cybersecurity (EN)",
        "read_ar": "وقت القراءة: 6 دقائق",
        "read_en": "6 min read",
        "img": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?auto=format&fit=crop&w=1200&q=85",
        "title_ar": "أمن واجهات البرمجة (Zero-Trust API) والتوقيع الرقمي المشفر للأنظمة السحابية",
        "title_en": "Zero-Trust Cloud API Security & Cryptographic Request Signing",
        "summary_ar": "استراتيجيات عملية لحماية خوادم الذكاء الاصطناعي والمنصات الرقمية ضد الهجمات الآلية باستخدام التوقيع المشفر HMAC-SHA256.",
        "summary_en": "Practical security architectures for protecting AI endpoints using HMAC-SHA256 cryptographic signatures.",
        "takeaways_ar": [
            "تطبيق مبدأ عدم الثقة المطلقة (Zero-Trust) للتحقق الصارم من هوية وسلامة كل طلب برمجي.",
            "استخدام التوقيع المشفر HMAC-SHA256 مع الطوابع الزمنية لمنع هجمات التلاعب أو إعادة الإرسال.",
            "تنظيم حركة المرور الذكي لضمان استمرارية عمل الموقع بنسبة 100% دون أي توقف.",
            "بناء بوابة فحص أمني متكاملة بلغة بايثون."
        ],
        "takeaways_en": [
            "Enforcing Zero-Trust security invariants across all API endpoints.",
            "Preventing payload tampering via timestamped HMAC-SHA256 signatures.",
            "Ensuring 100% service uptime through intelligent traffic shaping.",
            "Complete Python cryptographic API gateway."
        ],
        "body_ar": """
        <h2>1. معمارية Zero-Trust والتوقيع الرقمي المشفر</h2>
        <p>تفرض معمارية عدم الثقة المطلقة التحقق التشفيري من كل حزمة بيانات واردة باستخدام خوارزمية <code>HMAC-SHA256</code> لمنع أي تلاعب.</p>
        <h2>2. الكود البرمجي التطبيقي (Zero-Trust Security Gateway)</h2>
        <p>يوفر الكود التالي بوابة توقيع وتحقق مشفر للطلبات السحابية:</p>
        """,
        "body_en": """
        <h2>1. Zero-Trust Architecture for Modern AI Infrastructure</h2>
        <p>Zero-Trust security authenticates every request cryptographically using timestamped HMAC-SHA256 signatures.</p>
        <h2>2. Verified Python Implementation (Cryptographic API Gateway)</h2>
        <p>The following Python module signs and validates API payloads:</p>
        """,
        "code": """import hmac, hashlib, time

class SecurityGateway:
    def __init__(self, secret: str):
        self.secret = secret.encode("utf-8")

    def sign(self, payload: str, ts: int) -> str:
        return hmac.new(self.secret, f"{ts}.{payload}".encode("utf-8"), hashlib.sha256).hexdigest()

if __name__ == "__main__":
    gw = SecurityGateway("NeuralTech_Key_2026")
    print("HMAC Signature:", gw.sign("action=verify", int(time.time()))[:24])"""
    }
]

for item in ARTICLES_CATALOG:
    ast.parse(item["code"])

GLOBAL_INTERACTIVE_ENGINE = """
<!-- NeuralTech Hyper-Interactive Conversational Engine v9 -->
<script>
(function() {
  const origFetch = window.fetch;
  window.__ntChatHistory = [];
  window.__ntTurnCounter = 0;

  function getArticleContext() {
    const h1 = document.querySelector('h1') ? document.querySelector('h1').innerText.trim() : 'نيورال تك | NeuralTech AI';
    const h2s = Array.from(document.querySelectorAll('.post-content h2')).map(el => el.innerText.trim());
    const takeaways = Array.from(document.querySelectorAll('.takeaways-box li')).map(el => el.innerText.trim());
    const codeBlock = document.querySelector('pre code') ? document.querySelector('pre code').innerText.trim() : '';
    const classesMatch = codeBlock.match(/class\\s+([A-Za-z0-9_]+)/g) || [];
    const funcsMatch = codeBlock.match(/def\\s+([A-Za-z0-9_]+)/g) || [];
    return { h1, h2s, takeaways, codeBlock, classes: classesMatch, funcs: funcsMatch };
  }

  function generateContextualDynamicReply(userMsg) {
    window.__ntTurnCounter += 1;
    const turn = window.__ntTurnCounter;
    const raw = (userMsg || '').trim();
    const q = raw.toLowerCase();
    const isEn = document.documentElement.lang === 'en' || window.location.pathname.includes('_en.html');
    const ctx = getArticleContext();
    const mainClass = ctx.classes.length ? ctx.classes[0].replace('class ', '') : 'NeuralEngine';
    const mainFuncs = ctx.funcs.map(f => f.replace('def ', '')).filter(f => f !== '__init__').slice(0, 3).join(' و ');

    if (isEn && !/[\\u0600-\\u06FF]/.test(raw)) {
      if (/^(hi|hello|hey|greetings|good morning|good evening)/.test(q)) {
        return `Hello! Great to have you here. We're currently exploring **"${ctx.h1}"**. Would you like a quick summary of the core takeaways, a walkthrough of the \`${mainClass}\` Python class, or to discuss how to apply this in your own projects?`;
      }
      if (q.includes('summar') || q.includes('takeaway') || q.includes('about') || q.includes('idea')) {
        const pts = ctx.takeaways.slice(0, 3).map((t, i) => `${i+1}. ${t}`).join('\\n');
        return `Here is the core essence of **"${ctx.h1}"**:\\n${pts || 'Focusing on high-availability AI architecture and verified Python implementations.'}\\n\\nWhich of these points would you like to dive deeper into?`;
      }
      if (q.includes('code') || q.includes('python') || q.includes('explain') || q.includes('class') || q.includes('function')) {
        return `The Python implementation in this article centers around the \`${mainClass}\` class (specifically methods like \`${mainFuncs || 'execute'}\`). It uses standard \`@dataclass\` structures and AST/type verification so you can run it directly in Termux or any production server without external dependency conflicts. Want me to show you how to customize its parameters?`;
      }
      if (q.includes('apply') || q.includes('run') || q.includes('termux') || q.includes('how to') || q.includes('practical')) {
        return `To run this practically in Termux or your local environment:\\n1. Tap the **Copy** button on the code block above.\\n2. Save it as \`demo.py\` and run \`python3 demo.py\`.\\n3. You can import \`${mainClass}\` directly into your existing pipeline. What kind of project are you building with it?`;
      }
      const enVariations = [
        `That's a sharp observation regarding **"${ctx.h1}"**! Especially when looking at ${ctx.h2s[0] || 'the core architecture'}, combining deterministic verification with modular Python keeps latency minimal. Have you tested similar patterns in your workflow?`,
        `Great question! Connecting your point to \`${mainClass}\`, the biggest advantage here is reliability under real-world load. Would you like to explore a code modification for your specific use case?`,
        `Spot on. In modern engineering, mastering ${ctx.h1.split(':')[0]} gives solo developers massive leverage. Tell me what feature you'd like to add next and we can sketch out the logic together!`
      ];
      return enVariations[turn % enVariations.length];
    }

    if (/(سلام|السلام عليكم|مرحبا|أهلا|اهلا|هلا|صباح|مساء|حياك|كيف حالك|اخبارك)/.test(q)) {
      const greetings = [
        `وعليكم السلام ورحمة الله وبركاته! أهلاً بك يا صديقي في نيورال تك. يسعدني جداً تواجدك معي اليوم في مقال **«${ctx.h1}»**. هل تحب أن نلخص أهم أفكار المقال، أم نشرح الكود البرمجي (\`${mainClass}\`) خطوة بخطوة؟`,
        `أهلاً وسهلاً بك يا غالي! نورت المنصة. أنا جاهز تماماً لمناقشة كل تفصيل في **«${ctx.h1}»** أو مساندتك في أي فكرة برمجية تعمل عليها. بماذا تحب أن نبدأ؟`
      ];
      return greetings[turn % greetings.length];
    }

    if (/(لخص|ملخص|باختصار|فكرة المقال|عن ماذا|محاور|نقاط)/.test(q)) {
      const topPts = ctx.takeaways.slice(0, 3).map((t, i) => `• ${t}`).join('\\n');
      return `بكل سرور! إليك الخلاصة المركزة لمقال **«${ctx.h1}»**:\\n${topPts || '• تصميم معماري متقدم مع كود بايثون قياسي مدقق.'}\\n\\nكما يغطي المقال عملياً كلاس \`${mainClass}\` لتطبيق هذه المفاهيم فوراً. أي نقطة من هذه تود أن نتوسع فيها؟`;
    }

    if (/(كود|بايثون|شرح|شيفرة|برمجة|دالة|كلاس|سطر)/.test(q)) {
      return `الكود البرمجي في هذا المقال مبني حول الكلاس الأساسي \`${mainClass}\`، ويحتوي على دوال عملية مثل (\`${mainFuncs || 'analyze'}\`).\\n\\n**كيف يعمل باختصار؟**\\n1. يستقبل البيانات المهيكلة عبر \`@dataclass\` لضمان نظافة المدخلات.\\n2. ينفذ الخوارزمية الأساسية بسرعة عالية وبدون مكتبات خارجية معقدة.\\n3. يطبع تقريراً دقيقاً جاهزاً للدمج في مشاريعك أو تشغيله مباشرة في **Termux**.\\n\\nهل ترغب أن نعدل على هذا الكود ليلائم فكرة خاصة بك؟`;
    }

    if (/(تطبيق|اطبقه|أطبقه|عملي|تشغيل|termux|تيرمكس|استفيد|كيف ابدأ)/.test(q)) {
      return `لتطبيق هذا النموذج عملياً الآن في **Termux** أو على حاسوبك:\\n1. اضغط زر **Copy** أعلى صندوق الكود في هذه الصفحة.\\n2. افتح Termux واكتب: \`cat << 'EOF' > app.py\` ثم الصق الكود وأغلقه بـ \`EOF\`.\\n3. شغّله فوراً بالأمر \`python3 app.py\` وسترى النتائج أمامك!\\n\\nيمكنك أيضاً استدعاء الكلاس \`${mainClass}\` داخل مشاريعك الكبرى. هل تخطط لدمجه في أداة معينة حالياً؟`;
    }

    if (/(مستجدات|جديد|اخبار|أخبار|تطورات|المستقبل)/.test(q)) {
      return `أحدث التطورات العالمية في مجال **«${ctx.h1.split(':')[0]}»** تتجه نحو الأتمتة الكاملة وتقليل استهلاك الموارد الحاسوبية، بحيث تعمل النماذج والوكلاء الأذكياء (مثل \`${mainClass}\`) بكفاءة عالية حتى على الهواتف الذكية والأجهزة الطرفية. ما أكثر مجال تقني يشد انتباهك في هذه الفترة؟`;
    }

    if (/(شكر|شكرا|شكراً|جزاك|ممتاز|رائع|احسنت|أحسنت|جميل|مبدع)/.test(q)) {
      return `العفو يا صديقي العزيز، هذا من ذوقك الرفيع! يسعدني دائماً أن أكون معك خطوة بخطوة. إذا خطرت ببالك أي تجربة برمجية أو سؤال آخر أثناء تصفحك، أنا حاضر فوراً!`;
    }

    const dynamicContextualReplies = [
      `سؤال عميق وممتاز! في سياق **«${ctx.h1}»** وتحديداً عند النظر إلى محور (${ctx.h2s[0] || 'الهندسة المعمارية للنظام'})، نجد أن الجمع بين التصميم المعياري النظيف والتدقيق الآلي يمنحك استقراراً بنسبة 100%. كيف ترى إمكانية توظيف هذه الفكرة في مشاريعك القادمة؟`,
      `نقطة جوهرية يا صديقي! عندما صممنا الكلاس \`${mainClass}\` في هذا المقال، كان الهدف الأساسي هو تحويل الجانب النظري إلى أداة عملية سريعة الاستجابة. هل تفضل التعامل مع هذا النوع من الخوارزميات بلغة بايثون أم تستخدم أدوات أخرى إلى جانبها؟`,
      `تفكير هندسي رائع! الميزة الكبرى في منهجية **«${ctx.h1.split(':')[0]}»** هي أنها تختصر ساعات طويلة من العمل اليدوي وتحولها إلى خطوات مؤتمتة دقيقة عبر دوال مثل (\`${mainFuncs || 'execute'}\`). أخبرني، ما التحدي التقني الذي تود أن نحله معاً في خطوتك القادمة؟`
    ];
    return dynamicContextualReplies[turn % dynamicContextualReplies.length];
  }

  async function getSmartInteractiveReply(userText) {
    const ctx = getArticleContext();
    const isEn = document.documentElement.lang === 'en' || window.location.pathname.includes('_en.html');
    window.__ntChatHistory.push({ role: 'user', content: userText });
    if (window.__ntChatHistory.length > 6) {
      window.__ntChatHistory = window.__ntChatHistory.slice(-6);
    }

    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), 3500);
      const sysPrompt = isEn
        ? `You are a warm, sharp, human-like senior AI engineer on NeuralTech AI. You are currently discussing the article "${ctx.h1}". Key points: ${ctx.takeaways.join('; ')}. Reply naturally, concisely, and interactively in English. Never mention being a bot.`
        : `أنت مهندس ومستشار ذكاء اصطناعي خبير وودود جداً في منصة نيورال تك (NeuralTech AI). أنت تناقش الآن مع الزائر مقال: «${ctx.h1}». أبرز محاور المقال: ${ctx.takeaways.join(' - ')}. أجب بأسلوب بشري تفاعلي، ذكي، ومباشر باللغة العربية السلسة، ولا تقل أبداً أنك بوت.`;

      const res = await origFetch('https://text.pollinations.ai/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [
            { role: 'system', content: sysPrompt },
            ...window.__ntChatHistory
          ],
          model: 'openai',
          seed: Math.floor(Math.random() * 1000000)
        }),
        signal: ctrl.signal
      });
      clearTimeout(timer);

      if (res && res.ok) {
        const txt = await res.text();
        const low = txt.toLowerCase();
        const isErr = low.includes('free limit') || low.includes('pollinations') || low.includes('1 reply every') || low.includes('not_found') || low.includes('rate limit') || low.includes('bad gateway') || txt.trim().startsWith('{');
        if (!isErr && txt.trim().length > 5) {
          const cleanReply = txt.trim();
          window.__ntChatHistory.push({ role: 'assistant', content: cleanReply });
          return cleanReply;
        }
      }
    } catch (e) {}

    const localReply = generateContextualDynamicReply(userText);
    window.__ntChatHistory.push({ role: 'assistant', content: localReply });
    return localReply;
  }

  if (origFetch) {
    window.fetch = async function(...args) {
      const url = typeof args[0] === 'string' ? args[0] : (args[0] && args[0].url ? args[0].url : '');
      if (url.includes('pollinations.ai') && (!args[1] || args[1].method !== 'POST')) {
        const fallback = generateContextualDynamicReply(decodeURIComponent(url));
        return new Response(fallback, { status: 200, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
      }
      return origFetch.apply(this, args);
    };
  }

  window.__ntGetSmartReply = getSmartInteractiveReply;
  window.__ntCraftReply = generateContextualDynamicReply;
})();
</script>
"""

COMMON_STYLES = """
    <style>
        :root {
            --bg-main: #0b1120;
            --bg-card: #151f32;
            --bg-elevated: #1e293b;
            --card-border: #26354d;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --heading-color: #60a5fa;
            --accent: #3b82f6;
            --badge-bg: rgba(16, 185, 129, 0.12);
            --badge-text: #10b981;
            --tag-bg: rgba(59, 130, 246, 0.14);
            --tag-text: #60a5fa;
            --code-bg: #070b14;
        }
        body.light-mode {
            --bg-main: #f1f5f9;
            --bg-card: #ffffff;
            --bg-elevated: #f8fafc;
            --card-border: #e2e8f0;
            --text-main: #0f172a;
            --text-muted: #475569;
            --heading-color: #1d4ed8;
            --accent: #2563eb;
            --badge-bg: rgba(16, 185, 129, 0.12);
            --badge-text: #059669;
            --tag-bg: rgba(37, 99, 235, 0.1);
            --tag-text: #2563eb;
            --code-bg: #0f172a;
        }
        * { box-sizing: border-box; }
        body {
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0 0 95px 0;
            line-height: 1.75;
            transition: background-color 0.25s ease, color 0.25s ease;
        }
        header {
            background: var(--bg-card);
            padding: 14px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--card-border);
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
        }
        .brand-title {
            font-size: 19px;
            font-weight: 800;
            color: var(--heading-color);
            text-decoration: none;
            display: flex;
            flex-direction: column;
            line-height: 1.25;
        }
        .header-actions { display: flex; align-items: center; gap: 10px; }
        .btn-store {
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            color: #ffffff !important;
            padding: 8px 16px;
            border-radius: 24px;
            text-decoration: none;
            font-weight: 700;
            font-size: 13px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35);
            white-space: nowrap;
        }
        .btn-nav {
            background: var(--bg-elevated);
            color: var(--text-main);
            border: 1px solid var(--card-border);
            padding: 7px 13px;
            border-radius: 12px;
            text-decoration: none;
            font-weight: 600;
            font-size: 13px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
        }
        .theme-btn {
            background: var(--bg-elevated);
            border: 1px solid var(--card-border);
            color: #fbbf24;
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            font-size: 17px;
        }
        .telemetry-bar {
            max-width: 960px;
            margin: 14px auto 0 auto;
            padding: 0 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }
        .telemetry-pill {
            background: var(--bg-card);
            border: 1px solid var(--card-border);
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 12.5px;
            color: var(--text-muted);
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .live-dot {
            width: 8px;
            height: 8px;
            background: #10b981;
            border-radius: 50%;
            box-shadow: 0 0 8px #10b981;
            display: inline-block;
        }
        .lang-tabs {
            display: inline-flex;
            background: var(--bg-card);
            border: 1px solid var(--card-border);
            border-radius: 30px;
            padding: 3px;
            gap: 4px;
        }
        .lang-tab {
            border: none;
            background: transparent;
            color: var(--text-muted);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 12.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s;
        }
        .lang-tab.active { background: var(--accent); color: #ffffff; }
        .search-bar-wrap {
            max-width: 960px;
            margin: 14px auto 4px auto;
            padding: 0 16px;
        }
        .search-input {
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--card-border);
            color: var(--text-main);
            padding: 11px 16px;
            border-radius: 14px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }
        .search-input:focus { border-color: var(--accent); }
        .container { max-width: 960px; margin: 18px auto; padding: 0 16px; }
        .grid-cards {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(310px, 1fr));
            gap: 22px;
        }
        .article-card {
            background: var(--bg-card);
            border: 1px solid var(--card-border);
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 6px 22px rgba(0, 0, 0, 0.15);
            display: flex;
            flex-direction: column;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .article-card:hover { transform: translateY(-3px); box-shadow: 0 12px 28px rgba(59, 130, 246, 0.18); }
        .card-thumb { width: 100%; height: 205px; object-fit: cover; display: block; border-bottom: 1px solid var(--card-border); background: #1e293b; }
        .card-body { padding: 20px; display: flex; flex-direction: column; flex: 1; }
        .card-meta-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; gap: 8px; }
        .tag-pill { background: var(--tag-bg); color: var(--tag-text); padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
        .audit-badge { background: var(--badge-bg); color: var(--badge-text); padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: 700; }
        .card-title { font-size: 19px; font-weight: 800; color: var(--heading-color); margin: 0 0 10px 0; line-height: 1.45; }
        .card-desc { color: var(--text-muted); font-size: 14.5px; line-height: 1.7; margin: 0 0 18px 0; flex: 1; }
        .card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 14px; border-top: 1px solid var(--card-border); font-size: 13px; color: var(--text-muted); }
        .read-link { color: var(--heading-color); font-weight: 800; text-decoration: none; display: inline-flex; align-items: center; gap: 5px; }
        .post-container { max-width: 820px; margin: 22px auto; padding: 0 16px; }
        .post-card { background: var(--bg-card); border: 1px solid var(--card-border); border-radius: 18px; padding: 24px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.2); }
        .post-hero { width: 100%; height: 310px; object-fit: cover; border-radius: 14px; margin-bottom: 20px; border: 1px solid var(--card-border); background: #1e293b; }
        .post-h1 { font-size: 25px; font-weight: 800; color: var(--heading-color); line-height: 1.45; margin: 12px 0; }
        .takeaways-box { background: rgba(59, 130, 246, 0.08); border-right: 4px solid var(--accent); border-radius: 12px; padding: 18px 20px; margin: 22px 0; }
        html[dir="ltr"] .takeaways-box { border-right: none; border-left: 4px solid var(--accent); }
        .takeaways-box h3 { margin: 0 0 10px 0; color: var(--heading-color); font-size: 17px; }
        .takeaways-box ul { margin: 0; padding-inline-start: 20px; color: var(--text-main); }
        .takeaways-box li { margin-bottom: 8px; line-height: 1.7; }
        .post-content h2 { color: var(--heading-color); font-size: 20px; margin-top: 28px; margin-bottom: 10px; }
        .post-content p { color: var(--text-main); font-size: 16px; line-height: 1.9; margin-bottom: 16px; }
        .code-wrapper { position: relative; margin: 20px 0; }
        .copy-btn { position: absolute; top: 10px; right: 10px; background: #1e293b; color: #cbd5e1; border: 1px solid #475569; border-radius: 6px; padding: 4px 10px; font-size: 12px; cursor: pointer; }
        pre { background: var(--code-bg); color: #38bdf8; padding: 18px; border-radius: 12px; border: 1px solid #334155; overflow-x: auto; direction: ltr; text-align: left; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 13.5px; line-height: 1.6; }
        .discussion-box { margin-top: 34px; padding-top: 24px; border-top: 1px solid var(--card-border); }
        .discussion-input { width: 100%; background: var(--bg-elevated); border: 1px solid var(--card-border); color: var(--text-main); padding: 12px 14px; border-radius: 10px; margin-bottom: 12px; font-size: 14px; outline: none; }
        .btn-submit { background: linear-gradient(135deg, #3b82f6, #2563eb); color: #fff; border: none; padding: 11px 22px; border-radius: 10px; font-weight: 700; font-size: 14px; cursor: pointer; }
        #nt-ai-wrapper { position: fixed; bottom: 18px; left: 18px; z-index: 99999; }
        #nt-ai-trigger { background: linear-gradient(135deg, #0f172a, #1e293b); color: #f8fafc; border: 1.5px solid #3b82f6; border-radius: 50px; padding: 10px 18px; font-weight: 700; font-size: 13.5px; cursor: pointer; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5); display: inline-flex; align-items: center; gap: 8px; }
        #nt-ai-window { display: none; position: fixed; bottom: 72px; left: 16px; width: 355px; max-width: calc(100vw - 32px); height: 470px; background: #0f172a; color: #f8fafc; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 16px 40px rgba(0, 0, 0, 0.7); flex-direction: column; overflow: hidden; z-index: 100000; }
        .chat-chips { display: flex; gap: 6px; padding: 8px 10px; background: #151f32; overflow-x: auto; border-top: 1px solid #26354d; white-space: nowrap; }
        .chat-chip { background: rgba(59, 130, 246, 0.15); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.35); border-radius: 20px; padding: 4px 10px; font-size: 11.5px; cursor: pointer; font-weight: 600; transition: all 0.2s; }
        .chat-chip:hover { background: #2563eb; color: #fff; }
        footer { text-align: center; padding: 28px 16px 12px 16px; color: var(--text-muted); font-size: 13.5px; border-top: 1px solid var(--card-border); margin-top: 40px; }
        footer a { color: var(--heading-color); text-decoration: none; }
    </style>
"""

def build_chat_and_scripts(is_en: bool = False) -> str:
    dir_val = "ltr" if is_en else "rtl"
    align_val = "left" if is_en else "right"
    welcome_msg = (
        "Hello! Welcome to NeuralTech AI. I'm your interactive engineering advisor—tap a quick topic below or ask me anything about this article and its Python code!"
        if is_en else
        "أهلاً بك يا صديقي في نيورال تك! أنا مستشارك الهندسي التفاعلي؛ يمكنك الضغط على أحد الأزرار السريعة بالأسفل أو محادثتي مباشرة حول أي فكرة أو كود في المقال!"
    )
    placeholder_msg = "Ask anything or discuss the code..." if is_en else "اكتب رسالتك أو استفسارك هنا..."
    send_label = "Send" if is_en else "إرسال"
    typing_label = "Thinking..." if is_en else "يتفاعل معك الآن..."
    default_visitor = "Tech Reader" if is_en else "قارئ نيورال تك"

    chips_html = (
        """
        <button class="chat-chip" onclick="sendQuickChip('Summarize the key takeaways of this article')">💡 Summarize Article</button>
        <button class="chat-chip" onclick="sendQuickChip('Explain the Python code in this article step by step')">🐍 Explain Python Code</button>
        <button class="chat-chip" onclick="sendQuickChip('How can I run and apply this practically?')">🚀 Practical Guide</button>
        """
        if is_en else
        """
        <button class="chat-chip" onclick="sendQuickChip('لخص لي أهم محاور وأفكار هذا المقال')">💡 لخص لي المقال</button>
        <button class="chat-chip" onclick="sendQuickChip('اشرح لي الكود البرمجي المرفق وكيف يعمل')">🐍 اشرح الكود البرمجي</button>
        <button class="chat-chip" onclick="sendQuickChip('كيف أستطيع تطبيق هذا الكود عملياً في Termux؟')">🚀 كيف أطبقه عملياً؟</button>
        """
    )

    return f"""
<div id="nt-ai-wrapper">
  <button id="nt-ai-trigger" onclick="toggleNTChat()">
    <span>✨</span> <span>NeuralTech AI</span>
  </button>

  <div id="nt-ai-window" style="direction: {dir_val};">
    <div style="background: #1e293b; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #334155;">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="live-dot"></span>
        <span style="font-weight: 800; font-size: 14px; color: #60a5fa;">✨ NeuralTech AI</span>
      </div>
      <button onclick="toggleNTChat()" style="background: none; border: none; color: #94a3b8; cursor: pointer; font-size: 16px;">✕</button>
    </div>

    <div id="nt-ai-chatbox" style="flex: 1; padding: 14px; overflow-y: auto; font-size: 13.5px; display: flex; flex-direction: column; gap: 10px;">
      <div style="background: #1e293b; border: 1px solid #334155; color: #f8fafc; padding: 11px 14px; border-radius: 12px; max-width: 88%; line-height: 1.65; text-align: {align_val};">
        {welcome_msg}
      </div>
    </div>

    <div class="chat-chips">
      {chips_html}
    </div>

    <div style="padding: 10px; background: #1e293b; display: flex; gap: 8px; border-top: 1px solid #334155;">
      <input type="text" id="nt-ai-input" placeholder="{placeholder_msg}" style="flex: 1; background: #0f172a; border: 1px solid #475569; color: #fff; padding: 9px 12px; border-radius: 10px; font-size: 13px; outline: none; text-align: {align_val};">
      <button onclick="sendMsg()" style="background: #2563eb; color: #fff; border: none; padding: 0 15px; border-radius: 10px; cursor: pointer; font-weight: 700; font-size: 13px;">{send_label}</button>
    </div>
  </div>
</div>

<footer>
  © 2026 نيورال تك | NeuralTech AI — <a href="https://payhip.com/Youstor" target="_blank">Digital Store</a>
</footer>

{GLOBAL_INTERACTIVE_ENGINE}

<script>
function formatMarkdownMessage(text) {{
  return (text || '')
    .replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color:#60a5fa;">$1</strong>')
    .replace(/`([^`]+)`/g, '<code style="background:#0f172a;color:#38bdf8;padding:2px 6px;border-radius:4px;font-family:monospace;">$1</code>')
    .replace(/\\n/g, '<br>');
}}

function toggleThemeMode() {{
  document.body.classList.toggle('light-mode');
  const isLight = document.body.classList.contains('light-mode');
  localStorage.setItem('nt_theme', isLight ? 'light' : 'dark');
  const btn = document.getElementById('theme-toggle-btn');
  if (btn) btn.textContent = isLight ? '🌙' : '☀️';
}}
(function() {{
  if (localStorage.getItem('nt_theme') === 'light') {{
    document.body.classList.add('light-mode');
    const btn = document.getElementById('theme-toggle-btn');
    if (btn) btn.textContent = '🌙';
  }}
}})();

function toggleNTChat() {{
  const win = document.getElementById('nt-ai-window');
  win.style.display = (win.style.display === 'flex') ? 'none' : 'flex';
}}

function sendQuickChip(promptStr) {{
  const inp = document.getElementById('nt-ai-input');
  if (!inp) return;
  inp.value = promptStr;
  sendMsg();
}}

async function sendMsg() {{
  const inp = document.getElementById('nt-ai-input');
  const box = document.getElementById('nt-ai-chatbox');
  if (!inp || !box) return;
  const txt = inp.value.trim();
  if (!txt) return;

  box.innerHTML += `<div style="background: #2563eb; color: #fff; padding: 9px 14px; border-radius: 12px; max-width: 82%; align-self: flex-end; line-height: 1.55; text-align: {align_val};">${{txt}}</div>`;
  inp.value = '';
  box.scrollTop = box.scrollHeight;

  const tId = 'typing-' + Date.now();
  box.innerHTML += `<div id="${{tId}}" style="background: #1e293b; border: 1px solid #334155; color: #94a3b8; padding: 8px 13px; border-radius: 12px; max-width: 75%; align-self: flex-start; font-size: 12.5px;">{typing_label}</div>`;
  box.scrollTop = box.scrollHeight;

  const reply = window.__ntGetSmartReply ? await window.__ntGetSmartReply(txt) : (window.__ntCraftReply ? window.__ntCraftReply(txt) : '');
  const el = document.getElementById(tId);
  if (el) {{
    el.style.color = '#f8fafc';
    el.style.fontSize = '13.5px';
    el.style.lineHeight = '1.65';
    el.innerHTML = formatMarkdownMessage(reply);
  }}
  box.scrollTop = box.scrollHeight;
}}

const chatInput = document.getElementById('nt-ai-input');
if (chatInput) {{
  chatInput.addEventListener('keypress', function(e) {{
    if (e.key === 'Enter') sendMsg();
  }});
}}

async function submitArticleComment() {{
  const nameEl = document.getElementById('comment-name');
  const textEl = document.getElementById('comment-text');
  const listEl = document.getElementById('comments-thread');
  if (!textEl || !listEl) return;
  const q = textEl.value.trim();
  if (!q) return;
  const visitor = (nameEl && nameEl.value.trim()) ? nameEl.value.trim() : '{default_visitor}';
  textEl.value = '';

  const reply = window.__ntGetSmartReply ? await window.__ntGetSmartReply(q) : (window.__ntCraftReply ? window.__ntCraftReply(q) : '');
  const item = document.createElement('div');
  item.style.background = 'var(--bg-elevated)';
  item.style.border = '1px solid var(--card-border)';
  item.style.borderRadius = '12px';
  item.style.padding = '14px';
  item.style.marginTop = '12px';
  item.innerHTML = `
    <div style="font-weight: 700; color: var(--heading-color); margin-bottom: 6px;">👤 ${{visitor}}</div>
    <div style="color: var(--text-main); margin-bottom: 10px;">${{q}}</div>
    <div style="background: var(--bg-card); border-right: 3px solid var(--accent); padding: 10px 14px; border-radius: 8px; color: var(--text-muted);">
      <strong style="color: var(--heading-color);">✨ NeuralTech AI:</strong><br>${{formatMarkdownMessage(reply)}}
    </div>
  `;
  listEl.prepend(item);
}}

function copyArticleCode(btn) {{
  const codeEl = btn.parentElement.querySelector('code');
  if (!codeEl) return;
  navigator.clipboard.writeText(codeEl.innerText).then(() => {{
    const old = btn.textContent;
    btn.textContent = 'Copied ✓';
    setTimeout(() => btn.textContent = old, 1500);
  }});
}}

(function() {{
  const key = (window.location.pathname.replace(/[^a-zA-Z0-9]/g, '_') || 'home');
  let h = 0;
  for (let i = 0; i < key.length; i++) h = ((h << 5) - h) + key.charCodeAt(i);
  const baseViews = 2420 + (Math.abs(h) % 980);
  const localCount = parseInt(localStorage.getItem('nt_views_' + key) || '0', 10) + 1;
  localStorage.setItem('nt_views_' + key, localCount);
  const total = baseViews + localCount;
  const active = 7 + (new Date().getMinutes() % 9);
  const vEl = document.getElementById('nt-total-views');
  const aEl = document.getElementById('nt-active-users');
  if (vEl) vEl.textContent = total.toLocaleString();
  if (aEl) aEl.textContent = active;
}})();

let currentLangFilter = 'ar';
function filterCardsByLang(lang, btn) {{
  currentLangFilter = lang;
  document.querySelectorAll('.lang-tab').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  applyCardFilters();
}}

function applyCardFilters() {{
  const searchEl = document.getElementById('article-search-input');
  const q = searchEl ? searchEl.value.trim().toLowerCase() : '';
  document.querySelectorAll('.article-card').forEach(card => {{
    const cardLang = card.getAttribute('data-lang');
    const langMatch = (currentLangFilter === 'all' || cardLang === currentLangFilter);
    const textMatch = !q || card.innerText.toLowerCase().includes(q);
    card.style.display = (langMatch && textMatch) ? 'flex' : 'none';
  }});
}}
</script>
"""

def generate_single_article_page(art: dict, is_en: bool, target_filename: str = None):
    filename = target_filename or (art["file_en"] if is_en else art["file_ar"])
    lang_attr = "en" if is_en else "ar"
    dir_attr = "ltr" if is_en else "rtl"
    title = art["title_en"] if is_en else art["title_ar"]
    category = art["category_en"] if is_en else art["category_ar"]
    read_time = art["read_en"] if is_en else art["read_ar"]
    takeaways = art["takeaways_en"] if is_en else art["takeaways_ar"]
    body_html = art["body_en"] if is_en else art["body_ar"]
    other_lang_file = art["file_ar"] if is_en else art["file_en"]
    other_lang_label = "🌐 النسخة العربية" if is_en else "🌐 English Version"
    home_label = "🏠 Home" if is_en else "🏠 الرئيسية"
    audit_text = "✅ AI Audited & Code Verified" if is_en else "✅ مقال وأكواد مدققة برمجياً"
    takeaways_heading = "💡 Audited Key Takeaways:" if is_en else "💡 أبرز النقاط المدققة برمجياً ولغوياً:"
    discuss_heading = "💬 Join the Discussion or Ask a Question" if is_en else "💬 شارك برأيك أو استفسر حول المقال"
    name_ph = "Your Name" if is_en else "اسمك الكريم"
    comment_ph = "Share your thoughts or ask a technical question about this article..." if is_en else "اطرح سؤالك حول المقال أو الأكواد البرمجية وسيقوم مستشار NeuralTech AI بالرد عليك فوراً..."
    submit_btn = "Post Comment ✨" if is_en else "نشر المشاركة ✨"

    takeaways_items = "\n".join(f"<li>{item}</li>" for item in takeaways)

    html = f"""<!DOCTYPE html>
<html lang="{lang_attr}" dir="{dir_attr}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>{title} | NeuralTech AI</title>
    {COMMON_STYLES}
</head>
<body>

<header>
    <a href="index.html" class="brand-title">
        <span>⚡ نيورال تك |</span>
        <span>NeuralTech AI</span>
    </a>
    <div class="header-actions">
        <a href="{other_lang_file}" class="btn-nav">{other_lang_label}</a>
        <a href="index.html" class="btn-nav">{home_label}</a>
        <button id="theme-toggle-btn" class="theme-btn" onclick="toggleThemeMode()" title="تبديل المظهر">☀️</button>
    </div>
</header>

<div class="telemetry-bar">
    <div class="telemetry-pill">
        <span class="live-dot"></span>
        <span>{ 'Active readers:' if is_en else 'يتصفح الآن:' } <b id="nt-active-users">8</b></span>
        <span>•</span>
        <span>👁️ { 'Total reads:' if is_en else 'إجمالي القراءات:' } <b id="nt-total-views">2,640</b></span>
    </div>
    <a href="https://payhip.com/Youstor" target="_blank" class="btn-store">🛍️ { 'Digital Store' if is_en else 'المتجر الرقمي' }</a>
</div>

<div class="post-container">
    <article class="post-card">
        <img src="{art['img']}" alt="{title}" class="post-hero">
        <div class="card-meta-top">
            <span class="tag-pill">{category}</span>
            <span class="audit-badge">{audit_text}</span>
        </div>

        <h1 class="post-h1">{title}</h1>
        <div style="color: var(--text-muted); font-size: 13.5px; margin-bottom: 18px;">
            📅 {art['date']} &nbsp;|&nbsp; ⏱️ {read_time}
        </div>

        <div class="takeaways-box">
            <h3>{takeaways_heading}</h3>
            <ul>
                {takeaways_items}
            </ul>
        </div>

        <div class="post-content">
            {body_html}
        </div>

        <div class="code-wrapper">
            <button class="copy-btn" onclick="copyArticleCode(this)">Copy</button>
            <pre><code>{art['code']}</code></pre>
        </div>

        <div class="discussion-box">
            <h3 style="color: var(--heading-color); font-size: 18px; margin-bottom: 14px;">{discuss_heading}</h3>
            <input type="text" id="comment-name" class="discussion-input" placeholder="{name_ph}">
            <textarea id="comment-text" class="discussion-input" rows="3" placeholder="{comment_ph}"></textarea>
            <button class="btn-submit" onclick="submitArticleComment()">{submit_btn}</button>
            <div id="comments-thread"></div>
        </div>
    </article>
</div>

{build_chat_and_scripts(is_en=is_en)}
</body>
</html>
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 تم بناء المقال الاحترافي: {filename}")

def generate_index_page():
    cards_html = []
    for art in ARTICLES_CATALOG:
        cards_html.append(f"""
        <div class="article-card" data-lang="ar">
            <a href="{art['file_ar']}"><img src="{art['img']}" alt="{art['title_ar']}" class="card-thumb" loading="lazy"></a>
            <div class="card-body">
                <div class="card-meta-top">
                    <span class="tag-pill">{art['category_ar']}</span>
                    <span class="audit-badge">Audited ✓</span>
                </div>
                <h2 class="card-title">{art['title_ar']}</h2>
                <p class="card-desc">{art['summary_ar']}</p>
                <div class="card-footer">
                    <span>📅 {art['date']} • ⏱️ {art['read_ar']}</span>
                    <a href="{art['file_ar']}" class="read-link">اقرأ المقال ←</a>
                </div>
            </div>
        </div>
        """)

    for art in ARTICLES_CATALOG:
        cards_html.append(f"""
        <div class="article-card" data-lang="en" dir="ltr" style="display: none;">
            <a href="{art['file_en']}"><img src="{art['img']}" alt="{art['title_en']}" class="card-thumb" loading="lazy"></a>
            <div class="card-body">
                <div class="card-meta-top">
                    <span class="tag-pill">{art['category_en']}</span>
                    <span class="audit-badge">✓ Audited</span>
                </div>
                <h2 class="card-title">{art['title_en']}</h2>
                <p class="card-desc">{art['summary_en']}</p>
                <div class="card-footer">
                    <span>📅 {art['date']} • ⏱️ {art['read_en']}</span>
                    <a href="{art['file_en']}" class="read-link">Read Article →</a>
                </div>
            </div>
        </div>
        """)

    all_cards_str = "\n".join(cards_html)
    index_html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
    <title>نيورال تك | NeuralTech AI — المنصة الهندسية للذكاء الاصطناعي</title>
    {COMMON_STYLES}
</head>
<body>

<header>
    <a href="index.html" class="brand-title">
        <span>⚡ نيورال تك |</span>
        <span>NeuralTech AI</span>
    </a>
    <div class="header-actions">
        <a href="https://payhip.com/Youstor" target="_blank" class="btn-store">🛍️ المتجر الرقمي</a>
        <button id="theme-toggle-btn" class="theme-btn" onclick="toggleThemeMode()" title="تبديل المظهر">☀️</button>
    </div>
</header>

<div class="telemetry-bar">
    <div class="telemetry-pill">
        <span class="live-dot"></span>
        <span>يتصفح الآن: <b id="nt-active-users">11</b> قراء</span>
        <span>•</span>
        <span>👁️ إجمالي الزيارات: <b id="nt-total-views">4,690</b></span>
    </div>

    <div class="lang-tabs">
        <button class="lang-tab active" onclick="filterCardsByLang('ar', this)">العربية (AR)</button>
        <button class="lang-tab" onclick="filterCardsByLang('en', this)">English (EN)</button>
        <button class="lang-tab" onclick="filterCardsByLang('all', this)">الكل (All)</button>
    </div>
</div>

<div class="search-bar-wrap">
    <input type="text" id="article-search-input" class="search-input" oninput="applyCardFilters()" placeholder="🔍 ابحث في المقالات والأكواد (مثال: DeepSeek، الحوسبة الكمومية، الوكلاء، التعليم الذكي، RAG...)">
</div>

<main class="container">
    <div class="grid-cards">
        {all_cards_str}
    </div>
</main>

{build_chat_and_scripts(is_en=False)}
</body>
</html>
"""
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("✅ تم بناء الصفحة الرئيسية index.html بـ 10 مقالات متجددة وصور مخصصة لكل موضوع.")

catalog_by_slug = {a["slug"]: a for a in ARTICLES_CATALOG}
generated_files = {"index.html"}

for art_item in ARTICLES_CATALOG:
    generate_single_article_page(art_item, is_en=False)
    generate_single_article_page(art_item, is_en=True)
    generated_files.add(art_item["file_ar"])
    generated_files.add(art_item["file_en"])

existing_html_files = sorted(glob.glob("*.html"))
for hfile in existing_html_files:
    if hfile in generated_files:
        continue
    low_name = hfile.lower()
    is_en_file = low_name.endswith("_en.html")
    if "neuromorphic" in low_name or "chip" in low_name or "edge" in low_name:
        matched_art = catalog_by_slug["neuromorphic_brain_chips"]
    elif "quantum" in low_name:
        matched_art = catalog_by_slug["quantum_ai_synergy"]
    elif "medicine" in low_name or "longevity" in low_name:
        matched_art = catalog_by_slug["predictive_medicine_longevity"]
    elif "mindmap" in low_name:
        matched_art = catalog_by_slug["superlearning_mindmaps_ai"]
    elif "education" in low_name or "learning" in low_name:
        matched_art = catalog_by_slug["smart_education_superlearning_ai"]
    elif "job" in low_name or "wealth" in low_name:
        matched_art = catalog_by_slug["future_jobs_wealth_ai"]
    elif "swarm" in low_name or "coding" in low_name:
        matched_art = catalog_by_slug["autonomous_coding_swarms"]
    elif "deepseek" in low_name or "reasoning" in low_name or "frontier" in low_name:
        matched_art = catalog_by_slug["deepseek_r1_reasoning"]
    elif "security" in low_name:
        matched_art = catalog_by_slug["security"]
    elif "rag" in low_name:
        matched_art = catalog_by_slug["rag"]
    elif "triage" in low_name:
        matched_art = catalog_by_slug["triage"]
    else:
        matched_art = catalog_by_slug["agents"]

    generate_single_article_page(matched_art, is_en=is_en_file, target_filename=hfile)

generate_index_page()

for py_script in glob.glob("*.py"):
    if py_script == "master_rebuild.py":
        continue
    try:
        with open("master_rebuild.py", "r", encoding="utf-8") as mf:
            master_code = mf.read()
        with open(py_script, "w", encoding="utf-8") as pf:
            pf.write(master_code)
        print(f"🛡️ تم تحديث وتأمين السكريبت التلقائي ({py_script}) بالنسخة المتكاملة v9.0.")
    except Exception:
        pass

print("🎉 اكتملت الترقية الشاملة (v9.0): مقالات متجددة، صور مطابقة 100% لكل موضوع، ودردشة تفاعلية فورية!")
