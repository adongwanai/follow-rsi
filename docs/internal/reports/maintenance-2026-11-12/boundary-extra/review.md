# ReTrace / NCP 独立边界复审

时间：2026-11-12T06:45:16.757131+00:00。未读取root及第三轮agent裁定；依据当前feed/taxonomy.yaml与归档正文。

## ReTrace: Distilling Tool-Using Agents into Planner-Free Workflows

建议：exclude。在当前taxonomy的“Agent自己Harness”边界下排除。ReTrace的真实反馈修复和跨新输入复用都成立；但输出是一份逐SOP构建、用来取代原Agent执行该业务任务的独立程序，未展示将该程序作为原Agent的可复用技能/工具或对其共享Harness实施持久改写。不能因名称有workflow自动纳入，也不能因planner-free自动排除；决定性证据是产物的任务角色与作者明确的replace-the-agent定位。

限制：
- 不能写成“一次生成、没有反馈、没有跨任务复用”；附录D有前后依赖的真实修复轮。
- 不以LLM是否继续规划作为唯一边界；模型调用仍可作为工具存在。
- 仅见同一SOP的新输入评测，不是新程序族迁移。
- SOP-Bench修复反馈包含训练标签，不能与未修复方法当作同反馈预算比较。
- 企业场景未运行反馈修复；构建/无规划调用检查不证明任务正确。

证据：
- S1.p3.1 [artifact_role_replaces_agent](https://arxiv.org/html/2611.14492v1#S1.p3.1)：Replacing the agent with a workflow, however, requires knowing when each tool should be called and where each of its inputs comes from.
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455
- S3.SS1.p2.1 [artifact_per_procedure_cross_input_reuse](https://arxiv.org/html/2611.14492v1#S3.SS1.p2.1)：built once per procedure and reused on new inputs. At run time, code chooses the next step without calling an LLM; this is what we mean by planner-free . Individual tools may still call models.
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455
- S3.SS2.SSS0.Px3.p2.1 [real_feedback_repair_not_static_generation](https://arxiv.org/html/2611.14492v1#S3.SS2.SSS0.Px3.p2.1)：Where the benchmark can be re-executed offline, the workflow can also be repaired from its failures on training inputs: an LLM revises the code, and the IR is left unchanged (Appendix C ).
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455
- A4.SS0.SSS0.Px6.p1.1 [dependent_repair_rounds_and_heldout](https://arxiv.org/html/2611.14492v1#A4.SS0.SSS0.Px6.p1.1)：Each repair round runs the workflow on the training inputs and uses its failures to revise it. The traces, tasks, feedback, workflow-generation model, and stopping rule are fixed, and test inputs are evaluated only after the last round. Each version depends on the previous repair, so these results do not average independent generations as the main comparison does.
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455
- S7.p1.1 [no_transfer_to_new_procedures](https://arxiv.org/html/2611.14492v1#S7.p1.1)：We evaluate new inputs to the same procedures, not transfer to new procedures, and a change to an SOP or its tools may require rebuilding the workflow.
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455
- S7.p1.1 [limited_correctness_guarantees](https://arxiv.org/html/2611.14492v1#S7.p1.1)：Our construction checks confirm that generated code loads and contains no planning calls and, where re-execution is available, count how many logged steps it reproduces; they do not show that the recovered conditions are correct.
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455
- S5.SS1.SSS0.Px2.p1.1 [repair_evaluation_boundary](https://arxiv.org/html/2611.14492v1#S5.SS1.SSS0.Px2.p1.1)：There the feedback shows each failed input’s label, so the comparison with unrepaired methods is not like-for-like.
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455
- A4.SS0.SSS0.Px6.p2.1 [enterprise_no_repair](https://arxiv.org/html/2611.14492v1#A4.SS0.SSS0.Px6.p2.1)：We do not run repair on Internal : the platform provisions each workflow, and we currently cannot re-execute candidates offline during construction.
  HTML SHA256: f927fdf1429f6458252b825e3c16fee546938300ee70ca5f7ba94af2c5af0455

## NCP: Verifier-Guided Optimization of Weight-Space Control Policies

建议：include。可按Harness专项框架/评测限定收录，不能当作已证实的成功自改方法。持久优化对象是外部match-action规则表、规则程序和准入状态；权重写入是逐请求的执行手段，结束恢复，并非持续权重训练。论文真实执行了反馈候选生成、候选/基线比较、拒绝与跨进程归档重用，不是只有单元测试。但真实SmolLM实验全部拒绝，活动规则始终空；只有受控测试展示晋升路径，不能据此声称实现了实证的持久有效Harness改进。

限制：
- 真实实验只含九题手写架构微基准，3开发/3验证/3最终测试；不是广泛任务收益评测。
- 全部候选因纠正答案数未达阈值而拒绝；降低重复这一辅助指标不能称整体能力进步。
- 真实活动表不变、最终输出与基线相同；论文的多进程重跑/恢复是同结果复现，不是多轮改进。
- 25测试的晋升分支不能替代真实任务上的候选采纳。
- 收录应显式标框架/准入负结果，不把设计中的accepted规则持久化写成真实实验已发生。
- 临时修改权重不自动排除Harness，持久外部控制规则也不自动证明共演化；这里没有持久模型训练。

证据：
- S1.p3.1 [candidate_generation_from_task_feedback](https://arxiv.org/html/2611.13236v1#S1.p3.1)：The system observes task outcomes and output-token telemetry, extracts an activation direction associated with development failures, and constructs explicit match-action candidates. A verifier compares the current policy with the policy that would result from admitting each candidate.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S4.SS2.p2.1 [persistent_external_rule_object_and_temporary_weights](https://arxiv.org/html/2611.13236v1#S4.SS2.p2.1)：Accepted rule definitions persist in the table. Their weight effects remain temporary and are reconstructed during matching requests. The runtime holds a shared model lock, applies the selected program, performs generation using a fresh KV cache, and restores the request-entry weights.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S1.p5.1 [designed_future_feedback_cycles_not_empirical_success](https://arxiv.org/html/2611.13236v1#S1.p5.1)：An admitted rule changes the behavior observed in later requests, which changes subsequent telemetry and candidate generation. The implemented loop uses a deterministic synthesizer and an explicit verifier, making each proposed policy transition inspectable.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S4.SS2.p1.1 [admission_provenance_and_stale_evidence](https://arxiv.org/html/2611.13236v1#S4.SS2.p1.1)：Promotion requires accepted evidence for the rule’s fingerprint and the current active-table version. Changes to the active policy invalidate evidence measured against an earlier version.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S7.SS1.p2.1 [actual_bounded_microbenchmark](https://arxiv.org/html/2611.13236v1#S7.SS1.p2.1)：The nine-question handwritten fixture is an architectural microbenchmark of telemetry, candidate generation, admission and persistence. It contains three development, three validation, and three final-test questions with disjoint IDs and prompts.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S7.SS3.p2.1 [real_all_reject_result](https://arxiv.org/html/2611.13236v1#S7.SS3.p2.1)：All three candidates met the configured perplexity budget. The corrected-answer threshold was one; the active table consequently remained at zero rules.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S7.SS3.p4.1 [real_final_outputs_unchanged](https://arxiv.org/html/2611.13236v1#S7.SS3.p4.1)：With the active policy unchanged, the final outputs matched the baseline policy.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S7.SS4.p3.1 [controlled_tests_are_not_real_promotion_results](https://arxiv.org/html/2611.13236v1#S7.SS4.p3.1)：The NCP suite contains 25 passing tests. Controlled fixtures exercise both promotion and rejection through actual W-ISA parameter writes.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S7.SS4.p4.1 [real_and_controlled_transition_separation](https://arxiv.org/html/2611.13236v1#S7.SS4.p4.1)：with three evaluated candidates added to the archive. The controlled promotion fixtures exercise the complementary active-table transition.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S8.p1.1 [repeat_resume_not_new_improvement](https://arxiv.org/html/2611.13236v1#S8.p1.1)：In the measured cycle the archive grew by three candidates and the active table stayed empty. On the next cycle, deterministic candidate identifiers retrieved the existing decisions. Saved-table resumption retained the same search state across process boundaries.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08
- S8.p2.1 [task_progress_not_auxiliary_metric](https://arxiv.org/html/2611.13236v1#S8.p2.1)：The corrected-answer count remained zero, so the rule was archived under the one-correction admission criterion. This decision illustrates how the configured objective determines a policy transition rather than treating every change in an auxiliary signal as an improvement.
  HTML SHA256: 9f57f71b9853dcb227494d2e31a96a9aff2a313d1e69d70d8733003d70143a08

共19段引句逐段定位、正文hash与v1版本已核对；没有付费API或生产修改。
