# MCP 接入、额度与计费方案

状态：设计方案，尚未实现或部署。资料核对日期：2026-10-28。

## 群里发一个链接，能不能每人独立限量？

可以共用同一个入口，但服务必须先识别使用者。只有无认证的地址，无法可靠区分每个人；IP、客户端名称和 MCP 会话 ID 都不能替代个人身份。

推荐公开推广时采用 **同一服务地址 + OAuth 登录 + 每个账号独立额度**：

1. 运营者在群里发送介绍页，页面提供使用说明和 MCP 地址。
2. 使用者在支持远程 MCP 与 OAuth 的客户端中添加地址。
3. 客户端引导其登录并授权，服务据此识别账号。
4. 每个账号独立计量；额度耗尽后停止免费检索，说明重置时间。

OAuth 的访问 Token 由客户端管理，运营者不必逐个手动发送。

另一种适合小范围测试的方式是 **个人 API Token**：每人领取一串随机密钥，在客户端配置 `Authorization: Bearer <个人密钥>`。服务仅保存密钥哈希，可撤销、过期和单独限额。客户端必须支持自定义认证头；不支持时需要兼容的接入方式。Token 相当于访问凭证，拿到它的人可以消耗对应额度，不能放在群公告或公共仓库。

## 推荐的第一阶段限制

以下数字是试运行建议，不是现有服务承诺：

| 控制项 | 初始建议 |
| --- | --- |
| 个人短时调用频率 | 每分钟 6 次有成本的工具调用 |
| 个人每日检索额度 | 每日 30 次底层 AI Search 请求 |
| 服务全局检索上限 | 每日 500 次，每月 10,000 次底层请求，任一用尽即停止检索 |
| 个人阅读额度 | 每日 100 次上下文或文章分页读取 |
| 服务全局阅读上限 | 每日 2,000 次；另限制响应长度和单次读取量 |
| 失效行为 | 身份无效、额度不足或计量服务异常时，在访问 AI Search / R2 前拒绝 |

**计量点放在每一次底层请求之前。** 一次 MCP 工具调用可能包含多个查询和检索回退；多角度搜索也会放大实际调用次数。只数 `tools/call` 无法准确约束成本。连接初始化、工具列表查询与实际检索分别处理，不应因客户端正常握手反复扣除搜索额度。

短时防刷可以用 Workers Rate Limiting。它按 Cloudflare 节点近似计数，不能承担严格的全球总额度。个人与全局的日／月额度需要持久化、原子扣减的计量服务，例如 Durable Objects；全局扣减失败时不允许继续检索。缓存命中可以减少底层检索，但 HTTP 请求仍可能产生 Worker 费用。

个人账号对应的是账号额度，不是不可绕过的自然人身份。批量注册、密钥分享和未认证流量仍需要额外控制；为昂贵的后端调用设置全局上限，可以缩小成本影响。该上限也不等同于整个 Cloudflare 账户的账单硬上限。

## Cloudflare 成本如何估算

官方说明 AI Search 从 **2026-11-01** 开始计费。每个账号每月包含 1,000 次语义查询和 1,000 次全文关键词查询；超出后，语义／向量／混合查询为 **$0.75 / 千次**，全文关键词查询为 **$0.10 / 千次**。Workers AI 的嵌入与重排包含在 AI Search 价格中，生成回答、查询改写及外部模型用量另计。[AI Search 官方定价](https://developers.cloudflare.com/ai-search/platform/limits-pricing/)

例如一个月发生 10,000 次语义查询，假设账号的 1,000 次包含额度全部可用于本项目，则查询部分约为 `(10,000 - 1,000) / 1,000 × $0.75 = $6.75`。这不包含索引摄取、存储、Worker、R2、计量服务等费用，也不是完整账单预测；同账号其他项目会共用包含额度。

Workers 的请求与 CPU、R2 的存储与读取需分别考虑。限制 CPU 时间只能限制单次计算，不能替代总请求和下游检索额度。[Workers 定价](https://developers.cloudflare.com/workers/platform/pricing/)、[R2 定价](https://developers.cloudflare.com/r2/pricing/)

## 按量收费：计量、付款与内容权限

个人 Token 或 OAuth 解决「这是谁的额度」；付款系统解决「如何付钱」。可以在同一个账号体系下先给免费额度，再用预付费余额购买调用次数，服务端逐次扣减。

**x402** 是另一条路线：服务提出付款要求，支持 x402 的客户端通过钱包签署付款授权，服务验证付款后执行工具。它适合具备钱包和支付能力的 Agent，可以按工具调用收费；普通 MCP 客户端不会仅因添加服务地址，就自动具备钱包或扣款能力。

Cloudflare Agents SDK 提供收费 MCP 工具和付款客户端的集成方案。面向普通客户端仍需验证兼容性，必要时提供本地支付桥接；需要公开价格、用户支出授权、失败处理与付款防重放机制。[收费 MCP 工具](https://developers.cloudflare.com/agents/tools/payments/x402/charge-for-mcp-tools/)、[付款客户端](https://developers.cloudflare.com/agents/tools/payments/x402/pay-from-agents-sdk/)

Cloudflare 的托管 **Monetization Gateway** 与自行在 Worker 中实现 x402 是两种方案。核对资料时，托管网关仍为封闭测试，并要求买卖双方位于美国，不能假定任何账户都能直接启用。[Monetization Gateway](https://developers.cloudflare.com/monetization-gateway/)

**Cloudflare Wallets** 属于付款端的钱包产品规划，包括人管理的 Account Wallet 和供 Agent 使用的 Virtual Wallet。核对时官方文档明确：目前可预约钱包名称，但预约名称尚不能收款、付款或持有资金。因此不能把它当作已经普遍可用的收款账户或 Agent 银行卡。银行卡或钱包提供付款能力，服务端仍需实现价格、计量和支付验证。[Cloudflare Wallets](https://developers.cloudflare.com/wallets/)

建议先完成 OAuth 免费体验与成本上限，验证真实使用量后，再决定提供预付费额度还是 x402 付费工具。收费接口只能开放具有相应使用与商业分发授权的内容。

## 上线验收条件

验证个人身份隔离、无凭证拒绝、撤销生效、并发下的个人与全局额度、跨节点总量、查询扩展计费、月度重置和计量失败时的拒绝行为。所有内容读取工具均需执行同一权限检查；仅在搜索参数中要求 `free` 不能阻止直接按文章 ID 读取受限内容。

从目标客户端实测「添加地址 → 登录或配置密钥 → 搜索 → 阅读 → 额度耗尽」完整流程后，再把入口写入公开 README。

相关文档：[MCP OAuth 授权](https://developers.cloudflare.com/agents/model-context-protocol/protocol/authorization/)、[Workers 限流与严格总量限制](https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/)
