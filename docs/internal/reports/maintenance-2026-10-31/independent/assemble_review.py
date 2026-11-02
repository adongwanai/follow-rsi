"""Offline packaging of independently read official abstracts and body passages."""
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[4]
SOURCE = ROOT / "build/maintenance-2026-10-31/primary"
PRE_MERGE_CANONICAL_SHA = "e9632c353f3285cda18b8f0592e6f7517245778a1dc07e27ebab8ec7a434f820"


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def norm(text):
    return " ".join(text.split())


def save(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


intake = load(SOURCE / "intake-manifest.json")
official = load(SOURCE / "official-metadata.json")
intake_by_id = {item["id"]: item for item in intake["items"]}
official_by_id = {item["arxiv_id"]: item for item in official}
assert len(official_by_id) == len(intake_by_id) == 37

# Suggestions concern Harness eligibility, not acceptance for publication.
# Each reason was written after reading the official abstract, with selected
# source-body checks specified below. No primary classification is loaded.
SCREEN = {
    "2609.05881": ("exclude", "other_direction", "model_artifact_audit", "量化模型产物的功能审计与校准；改进对象是权重文件／量化配置，未提出反馈改写并继承 Agent 外部程序的机制。"),
    "2610.22990": ("exclude", "other_direction", "static_agent_benchmark", "改变用户画像与请求，评估固定 CUA 的服务表现；不是评估可保留的 Harness 演化。"),
    "2610.23656": ("exclude", "other_direction", "static_framework", "ABF 有 Harness，但更新的是本次调查的 findings、leads、notes；正文给出固定工具和提示规则，没有反馈改写并跨任务保留程序的闭环。"),
    "2610.25276": ("exclude", "other_direction", "video_generation", "用几何重建控制视频扩散；框架能兼容未来重建器不等于自身会根据执行反馈演化。"),
    "2610.27100": ("exclude", "other_direction", "world_model_benchmark", "测量生成式订单簿对注入订单的响应，研究对象是市场生成模型；不是 Harness 演化专门评测。"),
    "2610.34298": ("exclude", "other_direction", "task_local_repair", "DART 在当前动作失败后修正接口表达并保持语义动作不变；修复对象是单次调用，不会把新的控制程序保留到后续任务。"),
    "2610.36671": ("exclude", "other_direction", "static_decoding_algorithm", "按解码状态决定是否使用图像的固定推理算法；动态路由结果不是跨任务反馈改写 Harness。"),
    "2610.37905": ("include", "core", "component", "FilingLoop 用已锁定的评估反馈替换 Reviewer／Filer 的 Markdown 程序性技能，仅用于后续未尝试案例；这部分是 Harness 技能组件，企业文件修订本身不是。"),
    "2610.38174": ("exclude", "other_direction", "task_local_proof_search", "EasyProver 的递归是当前证明任务中的子 Agent 搜索；可变产物是证明与基准任务，没有保留新的 Agent 程序版本。"),
    "2610.38266": ("exclude", "general_rsi", "theory_survey", "综述物理 RSI 的权重、世界模型、经验、课程和执行程序；研究范围整体大于 Harness，适合作 general_rsi 背景，不能计入 Harness 专题综述。"),
    "2610.38293": ("exclude", "other_direction", "static_agent_benchmark", "在共同固定 Harness 下评估财报预测；没有研究 Harness 修改与保留。"),
    "2610.38331": ("exclude", "other_direction", "model_weights", "改的是多 token 预测的训练梯度与模型权重，未见外部程序反馈修订闭环。"),
    "2610.38342": ("exclude", "other_direction", "static_agent_benchmark", "金融投研能力与时间信息泄漏评测，虽强调可追溯流程，但未以 Harness 演化为研究对象。"),
    "2610.38392": ("include", "harness_eval", "safety_governance", "专门研究冻结模型周围的文本 Harness 被编辑、通过准入后成为下一代时的安全冗余流失；属于 Harness 演化评测，不要求评测器也自我修改。"),
    "2610.38568": ("exclude", "other_direction", "model_weights", "A-RSI 的生成模板、采样规则与控制器在训练前固定，持续更新的是 Solver 权重，训练反馈只决定何时切换预备任务池；没有外部程序共演化。"),
    "2610.38681": ("exclude", "other_direction", "model_weights", "量化／剪枝构造弱教师并进行自蒸馏，修改对象是模型权重；没有 Harness 工件持久修改证据。"),
    "2610.38728": ("exclude", "general_rsi", "theory_survey", "提出工作量、信息与递归改进的广义理论；覆盖个体与集体，不是专门针对 Harness 程序演化的理论。"),
    "2610.38796": ("exclude", "other_direction", "experience_world_model", "Routed CL 的路由提示和记忆系统库固定；仅选择状态簇、积累经验、做有界 schema 配置。配置验证后对该簇冻结，不能把路由选择当成管理程序演化。"),
    "2610.39122": ("include", "harness_eval", "safety_governance", "仅 MetaClaw 技能演化分支属于 Harness 相关评测：完成会话的反馈生成可复用过程指令，后续会话插入系统提示并固定库做测试。RL 分支单独属于权重训练，两者不是共同迭代。"),
    "2610.39264": ("exclude", "other_direction", "model_weights", "在线 PPO 训练规划／grounding 模型；真实应用反馈用于权重更新，没有外部 Harness 工件迭代证据。"),
    "2610.39287": ("exclude", "other_direction", "model_architecture", "统一 VLA 架构和状态记忆支持闭环飞行；闭环执行与当前状态更新不等于程序自演化。"),
    "2610.39293": ("exclude", "other_direction", "model_weights", "通过位置嵌入与排序课程训练图像模型，属于模型适配，未见自身 Harness 改写。"),
    "2610.39301": ("exclude", "other_direction", "model_weights", "OSAD 以自身 rollout 和刷新后的权重更新解析模型／教师；这是参数空间自训练，不能把教师刷新算外部 Harness 共同演化。"),
    "2610.39302": ("exclude", "other_direction", "representation_learning", "证明并改进表征对齐的学习目标；没有执行反馈驱动的 Agent 程序演化。"),
    "2610.39358": ("include", "core", "coevolution", "策略经 GRPO 更新后，用失败轨迹编辑有 ID／版本的程序性技能正文，再在固定新策略下配对验证并保留候选技能库。外部技能与权重分别迭代，适用 coevolution 例外。"),
    "2610.39417": ("exclude", "other_direction", "experience_world_model", "ExLabel 用固定 RAG／维护程序增删改 Understanding、Successes、Mistakes 经验项；变的是经验内容而非管理策略或技能程序，不能因自称 self-evolving 就纳入。"),
    "2610.39423": ("exclude", "other_direction", "model_weights", "公式生成数据上的监督度量学习，改的是表示模型与损失；没有 Harness 演化。"),
    "2610.39508": ("include", "core", "component", "SkillCompiler 按操作执行反馈修复程序、条件与依赖，验证后版本化留在 Program Asset Bank／技能结构中供后续任务使用；可复用程序组件与任务临时产物有明确区分。"),
    "2610.39663": ("exclude", "other_direction", "static_inference_algorithm", "固定稀疏注意力估计算法按当前激活动态选块；动态计算不构成 Agent 外部程序的反馈保留式改写。"),
    "2610.39714": ("defer", "borderline", "ai4ai_with_possible_skill_component", "MoLRSI 主体用固定选择规则读取工作流与经验记忆，科学工作流是任务产物；附加资源技能有执行失败修复和留存描述，但需确认实际保留的修改是 Agent 可复用调用程序，还是科研代码／依赖安装修复。仅该组件待审，不直接接纳整个搜索政策。"),
    "2610.39795": ("exclude", "other_direction", "model_weights_and_safety", "以 SFT 安装自我概念并测后继行为；对 RSI 安全有关，但不是 Harness 演化方法或专门评测。"),
    "2610.39884": ("defer", "borderline", "experience_world_model_with_possible_prompt_component", "KARMA 改六类知识文件，显示的已接纳案例是经验规则；接口也允许 role／output_protocol／action_descriptions 改写，不能只因代码冻结一律排除，也不能把可编辑能力当作这些程序性字段实际演化的证据。需要真实保留补丁区分知识内容与策略工件。"),
    "2610.40453": ("exclude", "other_direction", "image_generation", "对象插入数据集与视觉生成模型，未涉及 Agent 自我改进程序。"),
    "2610.40454": ("exclude", "other_direction", "model_weights", "训练生成器的适配器和 pointer head 进行重排；一体化模型能力不等于 Harness 演化。"),
    "2610.40564": ("exclude", "other_direction", "model_weights", "统一训练算法与数据配比框架，研究对象仍为模型训练，没有外部程序反馈改写。"),
    "2610.40614": ("exclude", "other_direction", "world_model_state", "高斯记忆更新的是场景几何／潜特征，使用固定 updater 与 DiT；不是 Agent 的记忆管理程序演化。"),
    "2610.40647": ("exclude", "other_direction", "model_architecture", "像素生成 Transformer 的 token／频段组织设计；没有反馈驱动的持久 Harness 改写。"),
}

# Exact continuous excerpts from independently read, numbered source paragraphs.
BODY = {
    "2610.23656": {
        "sections": ["6 The ABF Agent Harness", "7.2 Solvers"],
        "quotes": [(83, "that represents the progress of the investigation"),
                   (85, "Five short rules in the prompt."),
                   (86, "The ABF agent harness targets blockchain forensics in general, independent of any case, protocol, or service")],
        "limits": "只判定当前描述的固定框架，不否定它作为通用 agent benchmark 的价值。",
    },
    "2610.34298": {
        "sections": ["Appendix D DART: Controller, Triggers, and Evaluation Protocol"],
        "quotes": [(736, "DART permits the interface expression to change while holding the selected action fixed."),
                   (736, "The correction may change quoting, serialization, container structure, or other interface-specific expression details, but not the committed operation or arguments."),
                   (747, "All RQ4 settings use the same commitment-preserving controller and semantic preservation criterion.")],
        "limits": "按官方 PDF 的 Appendix D 选段核对；不把单次动作纠错误写成跨任务程序进化。",
    },
    "2610.37905": {
        "sections": ["3.2.3 Online Skill Evolution", "Appendix C.3", "Appendix D", "Appendix I.2"],
        "quotes": [(55, "After first-attempt results are locked, a skill editor receives the evolving arm’s completed-batch feedback"),
                   (58, "Each skill is a Markdown document with role metadata and procedural instructions."),
                   (57, "Only later, unattempted tasks use the new guidance."),
                   (57, "Model weights and base instructions remain fixed"),
                   (57, "This is online adaptation with historical scoring feedback, not evaluation on an independent held-out test set."),
                   (181, "A valid replacement enters the next batch without a held-out performance-selection stage or replay of completed cases.")],
        "limits": "在线同一有序流中适应，企业可重复出现；不是公司互斥留出泛化。准入检查结构／内容，不按留出表现择优；未认证论文数字。",
    },
    "2610.38174": {
        "sections": ["1 Introduction", "2 Related Work"],
        "quotes": [(10, "the parent agent is prompted with the proof state and the results its children have returned"),
                   (10, "decides which branches to continue, revise, or expand"),
                   (14, "the statement prefix is frozen")],
        "limits": "正文选读确认当前证明搜索／产物边界，未声称通读所有附录。",
    },
    "2610.38392": {
        "sections": ["3.1 Problem Setting", "4.1 Experimental Setup", "4.6 GEPA", "Limitations"],
        "quotes": [(21, "an accepted child becomes the next parent"),
                   (23, "A harness H H is text given to a fixed model M M"),
                   (23, "and no gate sees T final"),
                   (85, "most loops plant one deletion per generation to isolate the gate"),
                   (85, "the natural loops and GEPA runs are case studies")],
        "limits": "多数实验人为提议删除，用于隔离准入机制；自然优化器小样本是案例，不估计真实部署中的风险频率。没有复现实验。",
    },
    "2610.38568": {
        "sections": ["3 Method", "3.1 Programmatic task construction", "3.2 Rewards and policy optimization", "3.4 Fresh replacement"],
        "quotes": [(24, "Training experience therefore changes the timing of data replacement; it does not update the generator or the task-sampling distribution."),
                   (28, "Template construction takes place once, before training."),
                   (36, "We update only the Solver policy with GRPO"),
                   (36, "The templates and controller remain fixed.")],
        "limits": "可作为参数／训练数据日程相关信息，不作 Harness 候选；不审核其数值收益。",
    },
    "2610.38796": {
        "sections": ["3 Problem Formulation", "4 System Components", "Appendix B.1"],
        "quotes": [(46, "Its prompt and memory-system library remain fixed during evaluation"),
                   (54, "never parser code or task answers"),
                   (54, "online adaptation is limited to routing, bounded configuration, and state updates within a frozen library"),
                   (120, "the resulting adapter configuration is frozen for the lifetime of the cluster")],
        "limits": "配置过程含一次有界验证修复，但不能据此把固定库选择／schema 绑定写成开放管理程序演化。",
    },
    "2610.39122": {
        "sections": ["3.2 Controlled Two-Phase Methodology", "3.3 Mechanisms of Self-Evolution", "Appendix B.2", "Appendix C.4"],
        "quotes": [(38, "MetaClaw keeps the foundation model fixed and learns reusable skills from completed sessions"),
                   (38, "each with a name, category, trigger description, and procedure"),
                   (38, "In later conversations, the framework retrieves skills and inserts them into the agent’s system prompt."),
                   (97, "Each evaluation uses a freshly started proxy with the library fixed and evolution disabled"),
                   (123, "A conditional skill requires explicit user authorization.")],
        "limits": "资格仅指技能过程指令分支；RL 分支另列。库的磁盘文件格式未独立查代码，不能自行补为 SKILL.md。模拟反馈和指定任务的结论不代表任意个人 Agent。",
    },
    "2610.39358": {
        "sections": ["3.4 Readout-Guided Skill Revision", "4.1 Experimental Settings", "Appendix A.2", "Appendix B.4", "Figure 7 editor schema"],
        "quotes": [(52, "A shared LLM editor receives their skill texts and the complete failed trajectories"),
                   (52, "it may add, modify, delete, or merge skills, or leave the library unchanged"),
                   (52, "The proposal is accepted if it satisfies a predefined acceptance rule; otherwise, the current library is retained."),
                   (63, "Policies are trained with GRPO"),
                   (102, "Each skill specifies its applicable conditions and recommended procedure."),
                   (141, "the allowed decrease")],
        "limits": "依据是有版本的过程正文修订，不是单纯经验项打分。准入容差允许下降，不能宣称每次接纳都严格提升；Figure 7 的版本 schema 需与实际运行工件进一步对齐。",
    },
    "2610.39417": {
        "sections": ["3.1 Experience Accumulation", "3.1.3 Experience Update", "3.2 Experience Reuse"],
        "quotes": [(50, "updates the experience bank through three predefined operations: insertion, modification, and deletion"),
                   (52, "Refine the value of an existing experience item when prior experience needs clarification or correction."),
                   (55, "It shares the same RAG workflow with the rollout stage"),
                   (55, "uses their textual representation as a query to retrieve and rerank")],
        "limits": "删改经验内容并不自动满足程序变化；如复现实物另有程序性技能工件变更需重新开审。",
    },
    "2610.39508": {
        "sections": ["III-A Overview", "III-C Program Asset Reuse", "III-D Skill Optimization", "Appendix B", "Appendix C"],
        "quotes": [(23, "Newly synthesized and validated programs are persisted as reusable assets for subsequent skills."),
                   (51, "SkillCompiler revises the corresponding component according to the observed failure."),
                   (120, "Operations, program realizations, and Skill Skeletons are versioned separately."),
                   (126, "The persistent learned skill and Program Asset Bank state remains fixed throughout test evaluation."),
                   (131, "Development included inspection of held-out failure cases")],
        "limits": "最终测试冻结技能库，但开发曾查看留出失败案例，因此不能标为完全干净的未见测试。局部程序校验不证明任意输入语义正确；数值与实验未独立复现。",
    },
    "2610.39714": {
        "sections": ["2.1 Overview", "4.1.1 Resource library construction", "4.1.2 Persistent memory", "4.1.3 Search policy", "Appendix S1.1–S1.3", "Table S1"],
        "quotes": [(61, "After each execution attempt, MolRSI stores the workflow, its execution status and any available development score in solution memory."),
                   (126, "Execution errors guide repairs to the code, dependencies or environment settings."),
                   (126, "Skills that pass are tagged as validated and retained in the resource library for reuse."),
                   (127, "The Explore Agent could expand an existing resource library")],
        "limits": "主流程的 effective search policy 随记忆状态改变，不等于选择规则程序被改写。技能验证／修复组件有描述，但实际修改位置和后续继承工件需补证；不能将科研工作流整体当作 Harness。",
        "followup": "查实际资源技能前后版本、修复 diff 与后续任务引用，确认被保留的是 agent 调用程序／技能过程，而非仅外部科学代码或一次性安装调整。",
    },
    "2610.39884": {
        "sections": ["3 Problem Formulation", "4.3 Typed Modular Knowledge", "4.5 Critic and Evolver", "4.6 Validation", "Appendix A.5", "Appendix B.1", "Appendix D", "Table 1"],
        "quotes": [(47, "Role, domain, and output protocol are typed text modules."),
                   (50, "Valid changes are written atomically to their target files and journaled with before/after values"),
                   (133, "When a candidate is accepted, its knowledge state and validation records become the reference for the next cycle."),
                   (147, "The accepted cycle adds decision rules to the retained knowledge"),
                   (108, "The framework addresses external knowledge adaptation and cannot repair faulty tools or orchestration code.")],
        "limits": "固定执行代码并不排除系统提示演化；但六模块编辑能力也不能证明实验实际改过程序性提示。已展示案例主要是经验决策规则。离线匹配历史操作不证明业务收益。",
        "followup": "检查已接纳 mutation journal 是否实际改写 role／output_protocol／action_descriptions 的操作策略，还是仅经验／领域内容；按真实补丁再裁定 component 或 experience_world_model。",
    },
}

source_files = {}
quote_checks = []
records = []
for aid in sorted(SCREEN):
    source = official_by_id[aid]
    raw_intake = intake_by_id[source["id"]]
    abstract = source["citation_meta"].get("citation_abstract", source["abstract"])
    raw_file = SOURCE / "sources" / f"{aid}.abs.html"
    assert digest(raw_file) == source["source"]["sha256"]
    source_files[str(raw_file.relative_to(ROOT))] = digest(raw_file)
    suggestion, scope, subtype, reason = SCREEN[aid]
    record = {
        "id": source["id"],
        "title": source["title"],
        "round": 3,
        "reviewer": "codex_independent_source_reading_not_owner",
        "recommendation": suggestion,
        "suggested_scope": scope,
        "suggested_type": subtype,
        "reason_zh": reason,
        "formal_decision": "defer",
        "publication_authorized": False,
        "official_first_published": source["citation_meta"]["citation_date"].replace("/", "-"),
        "official_latest_version_date": source["citation_meta"].get("citation_online_date", "unknown").replace("/", "-"),
        "official_submission_history": source["submission_history"],
        "hf_daily_dates": raw_intake["hf_daily_dates"],
        "intake_groups": raw_intake["intake_groups"],
        "hf_reported_original_date": raw_intake.get("hf_original_published_at"),
        "official_abstract_source": {**source["source"], "file": str(raw_file.relative_to(ROOT))},
        "official_abstract_sha256": sha256(abstract.encode()).hexdigest(),
        "official_abstract": abstract,
        "review_level": "official_abstract_only",
        "body_review": None,
        "source_quotes": [{"kind": "official_abstract", "text": abstract.split(". ")[0] + ("." if ". " in abstract else "")}],
        "limitations_zh": "仅按官方摘要作专题范围筛查，不声称正文不存在其他组件，不认证实验数字；发现新程序更新证据时应重开审核。",
        "necessary_followup_zh": "",
        "performance_claims_audited": False,
        "experiments_reproduced": False,
    }
    if aid in BODY:
        details = BODY[aid]
        meta_file = SOURCE / "sources" / f"{aid}.full.meta.json"
        meta = load(meta_file)
        # The first HTML acquisition predates the source manifest's format key.
        body_format = "pdf" if aid == "2610.34298" else "html"
        body_file = SOURCE / "sources" / f"{aid}.full.{body_format}"
        paragraphs_file = SOURCE / "sources" / f"{aid}.full.paragraphs.json"
        paragraphs = load(paragraphs_file)
        assert digest(body_file) == meta["sha256"]
        for path in [meta_file, body_file, paragraphs_file]:
            source_files[str(path.relative_to(ROOT))] = digest(path)
        body_quotes = []
        for index, quote in details["quotes"]:
            assert norm(quote) in norm(paragraphs[index]), (aid, index, quote)
            body_quotes.append({"kind": "official_body_selected_passage", "paragraph_index": index,
                                "text": quote, "source_url": meta["url"]})
            quote_checks.append({"id": source["id"], "paragraph_index": index, "exact_normalized_continuous_match": True})
        record["source_quotes"] += body_quotes
        record["review_level"] = "official_abstract_and_selected_body_passages"
        record["body_review"] = {
            "source": meta,
            "file": str(body_file.relative_to(ROOT)),
            "paragraphs_file": str(paragraphs_file.relative_to(ROOT)),
            "paragraphs_sha256": digest(paragraphs_file),
            "sections_or_passages_read": details["sections"],
            "entire_paper_read": False,
            "quoted_paragraph_indices": sorted({index for index, _ in details["quotes"]}),
        }
        record["limitations_zh"] = details["limits"]
        record["necessary_followup_zh"] = details.get("followup", "")
    records.append(record)

assert len(records) == 37
assert len(BODY) == 13
assert Counter(row["recommendation"] for row in records) == {"include": 5, "exclude": 30, "defer": 2}
assert all(row["formal_decision"] == "defer" for row in records)
assert all(row["body_review"] for row in records if row["recommendation"] in {"include", "defer"})

frozen_at = datetime.now(timezone.utc).isoformat()
inputs = {
    "review_date": "2026-10-31",
    "previous_canonical_snapshot_sha256": PRE_MERGE_CANONICAL_SHA,
    "canonical_boundary": "Canonical data is being integrated separately by the parent task. This independent package does not read or write current canonical data; the recorded hash is the earlier snapshot, not the current merge result.",
    "intake_sha256": digest(SOURCE / "intake-manifest.json"),
    "official_metadata_sha256": digest(SOURCE / "official-metadata.json"),
    "counts": intake["counts"],
    "date_policy": "2026-10-31 HF HTTP 200 empty; 23 late additions belong to HF 2026-10-30; 20 remote-main new IDs overlap 6 for a union of 37. Original publication, latest version and HF date remain separate.",
    "source_files": source_files,
    "independence": "Raw IDs, official abstracts and body files were supplied by the primary agent; no primary classifications or rationale for this 37-item intake were read before freezing. One official date-difference notice was received. Historical taxonomy and previous-day adjudications are known; shared source acquisition is not independent HTTP replication.",
    "criteria": {
        # Owner-provided criteria are identified by name and their frozen hash;
        # the external document is not bundled with this report.
        "owner_document": "CODEX_PROMPT_FIX_AUDIT.md",
        "owner_document_sha256": "eb5622f7d63cdbe1441d85d0edf86cbd0ed36e9f659419e4a735a7731760d35b",
        "taxonomy_sha256": digest(ROOT / "feed/taxonomy.yaml"),
        "coevolution_exception_applied": True,
        "evaluation_need_not_modify_itself": True,
        "memory_entries_are_not_automatically_programs": True,
        "editable_capability_is_not_proof_of_executed_retained_edit": True,
    },
}
save("source-inputs.json", inputs)
(OUT / "source-reviews.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records))
findings = {
    "review_date": "2026-10-31",
    "frozen_at": frozen_at,
    "status": "frozen_before_primary_comparison_not_approval",
    "all_formal_decisions": "defer",
    "source_inputs_sha256": digest(OUT / "source-inputs.json"),
    "source_reviews_sha256": digest(OUT / "source-reviews.jsonl"),
    "counts": {"official_abstracts_read": 37, "body_selected_passages_read": 13,
               "include_suggestions": 5, "exclude_harness_suggestions": 30, "unresolved_boundaries": 2,
               "verified_body_quotes": len(quote_checks), "original_source_files_verified": len(source_files)},
    "items": {row["id"]: {key: row[key] for key in ["recommendation", "suggested_scope", "suggested_type", "formal_decision", "review_level"]} for row in records},
    "independence": inputs["independence"],
    "paid_api_calls": 0,
    "performance_claims_audited": False,
    "experiments_reproduced": False,
}
save("frozen-findings.json", findings)

def table(rows):
    lines = ["| 条目 | 独立建议 | 依据与限制 |", "| --- | --- | --- |"]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "\\|").replace("\n", " ") for value in row) + " |")
    return "\n".join(lines)

main = [row for row in records if row["recommendation"] != "exclude"]
negative_body = [row for row in records if row["recommendation"] == "exclude" and row["body_review"]]
summary = [
    "# 2026-10-31 独立第三轮来源复核",
    "状态：**已在对照主审前冻结；全部正式决定仍为 defer，未批准发布。** 本轮没有付费 API 调用，没有改 canonical、审核单或论文库。",
    "HF 10 月 31 日接口返回 HTTP 200 空列表。10 月 30 日后补 23 篇，remote-main 新增 20 个稳定 ID，重叠 6 篇，去重审核 37 篇。后补条目仍属于 10 月 30 日，不能包装成今日新论文。原始发表日、最新版本日与 HF 上榜日分开保存；Broken on Arrival 的官方首次发表为 9 月 5 日，HF 的 10 月 25 日不能代替首发日期。",
    "独立读完 37 篇官方摘要，并对 13 篇候选、边界及固定框架负例读正文选段。范围建议为 include 5、exclude Harness 30、defer 2；这些是供 owner 复核的专题判断。既没有宣称 37 篇全文精读，也没有独立认证论文数字。",
    "## 候选与未决边界",
    table([(f"{row['id']} · {row['title']}", f"{row['recommendation']} / {row['suggested_type']}", row["reason_zh"] + " " + row["limitations_zh"]) for row in main]),
    "## 正文核对的排除项",
    table([(f"{row['id']} · {row['title']}", row["suggested_type"], row["reason_zh"]) for row in negative_body]),
    "另有 24 项按官方摘要排除 Harness，其中物理 RSI 综述和 From Grind to Grasp 可作广义 RSI 背景；其他包含模型训练、生成模型、静态评测等。摘要排除只表示本轮未取得 Harness 资格证据，若后续正文出现独立程序组件可重新审核。",
    "## 这轮特别保留的限制",
    "- FilingLoop 更新的是 Markdown 程序性技能；它测在线流式适应，企业可重复出现，没有独立公司留出测试。\n- Masked Erosion 多为受控删除实验；自然优化器结果是小样本案例，不外推为普遍发生频率。\n- Appreciation 的技能分支与 RL 分支分开判断；没有把它们写成 coevolution，技能磁盘格式保持未知。\n- Before the Next Rollout 实际分别迭代权重与有版本的技能正文；准入容差允许下降，不能宣称所有已接纳修改都严格改善。\n- SkillCompiler 的程序组件资格清楚，但论文承认开发中查看留出失败案例，不能写成完全未见的测试。\n- MoLRSI 与 KARMA 保留两项边界：实际修改对象／已接纳补丁不足以在本轮彻底区分程序性工件和经验内容。",
    "## 审查独立性与续接",
    "来源采集复用 primary 保存的官方 HTTP 响应；冻结前只读取输入 ID、官方摘要／正文和日期信息，没有读这 37 项主审分类或理由。已知项目 taxonomy 与前一日的裁决，因此不声称不知道历史背景，也不把共享采集说成独立网络重验。",
    "`source-reviews.jsonl` 保存逐项理由、引句、原日期、来源版本、选读章节、局限和后续动作；`frozen-findings.json` 先固定建议，随后才能与主审比较。来源全文仍位于本地 build 缓存，本包仅保存短引句和哈希。",
    "后续：逐项对照主审；MoLRSI 需要保留的技能／工具修复 diff 与后续引用，KARMA 需要被接纳 mutation journal 的具体字段；所有候选仍交 owner 接纳。",
]
(OUT / "README.md").write_text("\n\n".join(summary) + "\n")

validation = {
    "result": "pass",
    "previous_canonical_snapshot_sha256": PRE_MERGE_CANONICAL_SHA,
    "canonical_read_or_written_by_packaging": False,
    "parent_canonical_integration_in_progress": True,
    "all_formal_decisions": "defer",
    "counts": findings["counts"],
    "source_quotes": quote_checks,
    "source_files": source_files,
    "frozen_findings_sha256": digest(OUT / "frozen-findings.json"),
    "source_reviews_sha256": digest(OUT / "source-reviews.jsonl"),
    "primary_comparison_performed": False,
    "published": False,
    "paid_api_calls": 0,
}
save("validation.json", validation)
hashes = {path.name: digest(path) for path in sorted(OUT.iterdir()) if path.is_file() and path.name != "package-hashes.json"}
save("package-hashes.json", {"files": hashes, "contains_full_paper_cache": False, "contains_owner_acceptance": False})
print(json.dumps({"result": "pass", "frozen_findings_sha256": digest(OUT / "frozen-findings.json"), "counts": findings["counts"]}, ensure_ascii=False, indent=2))
