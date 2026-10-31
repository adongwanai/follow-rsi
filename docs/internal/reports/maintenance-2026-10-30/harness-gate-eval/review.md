# 2026-10-30 Harness gate 固定样本复核

45/45 评估完整；0 metadata、身份、API 或 schema 错误。质量门槛未通过：召回率 24/28 = 85.71%，低于 90%。退出码 1 表示质量失败，不是运行中断。

| 子集 | 样本 | TP | FP | FN | TN | Precision | Recall |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| full_45 | 45 | 24 | 2 | 4 | 15 | 0.9231 | 0.8571 |
| owner_25 | 25 | 7 | 2 | 1 | 15 | 0.7778 | 0.8750 |
| library_20 | 20 | 17 | 0 | 3 | 0 | 1.0000 | 0.8500 |
| without_prompt_examples_35 | 35 | 19 | 2 | 4 | 10 | 0.9048 | 0.8261 |
| owner_without_prompt_examples_15 | 15 | 2 | 2 | 1 | 10 | 0.5000 | 0.6667 |
| prompt_examples_10 | 10 | 5 | 0 | 0 | 5 | 1.0000 | 1.0000 |

全体 precision 虽超过 0.85，owner 子集 precision 仅 0.7778、recall 仅 0.8750。20 个预选 library 样本全为正例，不能用其精确率证明负例排除能力，也不能让它们掩盖 owner 子集问题。

10 个案例已经出现在 gate prompt 中，因此不是盲测。去掉它们后仍只是排除已知 prompt 校准案例的子集，不声称严格独立留出集。library 标签是预选评估目标，未替代全文审查；HARBOR 的已知 scope 歧义继续保留。

relevance/classify 使用 deepseek-flash；gate 使用 deepseek-v4-pro，每项 1 个 gate 样本。此评估不等同三轮来源复核。60 个输入和代码文件的 SHA-256 在结束后全部一致；45 个固定标签未变，报告逐项输出与独立保存的 case-results 一致，指标另行复算一致。

六个固定标签误判：

- TokenEconomizer：原 owner 为 Harness；相关性模型 include，但 gate 认为摘要未充分明确反馈驱动修改，降为 borderline。固定标签记 FN，不据此改写 owner 判断。
- CarryOn：原 owner 为 borderline；模型把“when refined skills are reused”解读为跨任务持久性而准入。逐字引用存在，但不能单靠逐字匹配消除语义边界。固定标签记 FP。
- Δτ-Bench：原 owner 为其他方向 evaluation_benchmark；gate 通过 Harness 专项评测支路准入。原摘要提到技能维护，模型将此扩大为 Harness 演化专项证据。固定标签记 FP，保留 owner 标签。
- HARBOR：预选 library 正例；相关性阶段缺少持久性引句，保持 borderline，即使后续 gate 样本原始输出 harness。原有 owner scope 歧义仍存在，保留预选标签计 FN。
- Bad Genius：原 gate 样本为 harness，但反馈引句把源文公式 $B_{\mathrm{rel}}$ 改为 B_rel，逐字 guard 无法匹配，最终反馈字段 unclear、gate borderline。记 FN；不削弱 guard 或重跑改善分数。
- Co-Evolving Harnesses and Models：预选 library 协同演化正例；相关性 include，gate 认为摘要未明确 Harness 的反馈修改而给 borderline。协同演化例外未稳定被识别；不是仅因 model_frozen=no 自动排除。固定标签记 FN。

这次只跑当前 45-case gate；未运行旧 105/107 evaluator，未修改 labels、prompts、canonical 数据或发布文件，也未为提升分数重复调用模型。逐字引用匹配只能核验文本存在，不能证明语义充分。

详细证据见 `gate-report.json`、`verification.json` 和 `input-manifest.json`。所有结论为审核建议，不是 owner accept 或发布授权。
