# Case Studies

6个来自电商订单修改/退款系统的真实 bug 案例，作为抽象反模式的具象示例。

## Case 1: 多态字段陷阱

`reference_id` 根据 `reference_type` 持有不同的 ID，简化后的代码忽略支付场景导致退款 ID 返回错误。

## Case 2: 锁作用域缺口

分布式锁只保护 retry 路径（status=PROCESSING），而首次进入（status=PENDING）未受保护——导致重复退款执行。

## Case 3: 终态顺序问题

在资源清理前标记 status=FINISH，当清理 RPC 超时时导致永久死锁。

## Case 4: 假设的幂等 RPC

`ReleaseResourceLock` 假设幂等，但 SQL 有 `WHERE lock_status=1` 约束——第二次调用的 WHERE 子句不匹配。

## Case 5: 异步缓存竞争

`persistSuccessResult` 在 commit 后在 goroutine 中运行，创建了一个窗口期，立即重试会错过缓存并触发不安全的 fallback 逻辑。

## Case 6: 文档漂移

代码的操作顺序随着多次修复改变了，但设计文档未更新——导致后来的开发者在错误顺序添加新功能。

---

*文档强调："人类记住**故事**远比抽象规则好"——这些具体案例作为团队的 bug 博物馆。*