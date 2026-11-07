# Medium 修改手册 · UC04 增补「State does not inject itself」

> 文章：https://medium.com/@pinxiong.cn/it-remembers-across-restarts-and-forgets-mid-conversation-1a27f5d6b782
> 日期：2026-11-07 ｜ 性质：已发布文章的手动增补（主站 / BC / Dev.to 已同步）
> 原因：读者 Reid 指出 state 通道问题后实测确认——1.63.0 里 `agent.state` 只存取、不会自动进 prompt，必须自己写钩子注入。这一点要补进正文。

共 4 处改动：1 个新节 + 3 处小改。预计 10 分钟。

---

## 第 1 步：插入新节「State does not inject itself」

**插入位置**：找到 F1 图（三条泳道机制图，alt 是 "Three stacked lanes joined by downward arrows..."），
新节插在这张图**之后**、标题 **"Summarizing, but only at the cliff" 之前**。

**粘贴以下内容**（标题用 Heading 2；python 代码块和 text 输出块各自单独设成代码块）。

> 下面每个自然段都是**一整行**，这是故意的：Medium 会把段内换行变成硬换行，如果按源码那样
> 在 95 字符处折行，粘上去就会出现一句一断的锯齿。整段粘完再按需 `Option+Shift+↑/↓` 调。

---

## State does not inject itself

The third lane has a gap of its own. In 1.63.0, `agent.state` is written to `agent.json` and restored on the next invocation, but nothing in the prompt path ever reads it. `FileSessionManager` hands it to `SessionAgent.from_agent` (`state=agent.state.get()`, `types/session.py:145`【链接1】) and reloads it at `repository_session_manager.py:262`【链接2】; `SnapshotSessionManager` goes through `take_snapshot` and `load_snapshot` instead (`agent/agent.py:2262`【链接3】, `:2304`). And `system_prompt` is a value, typed `str | list[SystemContentBlock] | None` (`agent/agent.py:243`【链接4】), not a callable. So a fact in state is durable and invisible at the same time: the same failure the window produced, out of a different store.

If the model has to see it, the injection is yours to write. The smallest working version is a `BeforeInvocationEvent` hook (`hooks/events.py:39`【链接5】) plus the `system_prompt` setter (`agent/agent.py:812`【链接6】):

```python
BASE_PROMPT = "You are a concise assistant."

def inject_manifest(event: BeforeInvocationEvent) -> None:
    manifest = json.dumps(agent.state.get(), sort_keys=True)
    agent.system_prompt = f"{BASE_PROMPT}\n\n<manifest>\n{manifest}\n</manifest>"

agent.add_hook(inject_manifest, BeforeInvocationEvent)
```

Same setup as the sliding-window run, with one addition: the codename goes into both the first user message and `agent.state`, and the hook rewrites the system prompt on every invocation. Turn seven now answers with the codename, even though it left the window at turn four:

```text
ORION_IN_MESSAGES_BEFORE_ASK: False
TURN 7 ask     | msgs= 6 stored=14 | ORION
ORION_IN_SYSTEM_PROMPT: True
```

The hook fires before every invocation, not once at construction, so the manifest tracks state as it changes. The channel is not free either: it repeats the serialized state in the prompt on every call, which is a fair price for an invariant and a bad one for a log. Which restates the original rule with the machinery filled in. Messages are for the model, state is for your code, and the bridge between them is a hook you write yourself.

---

**挂链接**：上面 6 个【链接N】标注处，选中对应的 `文件名:行号` 文本，Cmd+K 粘贴：

| 标注 | 选中的文本 | URL |
|---|---|---|
| 链接1 | `types/session.py:145` | https://github.com/strands-agents/sdk-python/blob/main/src/strands/types/session.py |
| 链接2 | `repository_session_manager.py:262` | https://github.com/strands-agents/sdk-python/blob/main/src/strands/session/repository_session_manager.py |
| 链接3 | `agent/agent.py:2262` | https://github.com/strands-agents/sdk-python/blob/main/src/strands/agent/agent.py |
| 链接4 | `agent/agent.py:243` | https://github.com/strands-agents/sdk-python/blob/main/src/strands/agent/agent.py |
| 链接5 | `hooks/events.py:39` | https://github.com/strands-agents/sdk-python/blob/main/src/strands/hooks/events.py |
| 链接6 | `agent/agent.py:812` | https://github.com/strands-agents/sdk-python/blob/main/src/strands/agent/agent.py |

（链接 3/4/6 指向同一个文件，只是行号不同，挂同一个 URL 即可。）

---

## 第 2 步：改「When not to use this」里的一句话

**找到原句**（在这一节第三段开头）：

```text
If a fact has to survive compression, put it in state or in the system prompt, not in the hope that the summarizer keeps it.
```

**替换为**：

```text
If a fact has to survive compression, put it in state and inject it as above, or write it into the system prompt directly, not in the hope that the summarizer keeps it.
```

---

## 第 3 步：Try it yourself 加一条命令

在代码块里找到这一行：

```text
python src/sliding_window.py           # fourteen stored, six visible
```

在它**下面**加一行：

```text
python src/state_manifest.py           # same window, codename returns via the manifest
```

---

## 第 4 步：Takeaways 加一条

在 `- \`agent.state\` refuses a non-JSON value the moment you set it...` 这一条**之后**插入：

```text
Stored is not surfaced: `agent.state` reaches the model only if you inject it, and a `BeforeInvocationEvent` hook rewriting the system prompt is the smallest bridge.
```

（Medium 里作为列表项添加，行内代码用 ` 反引号样式。）

---

## 第 5 步：发布更新

右上角 **⋯ → Edit story** 改完后点 **Publish**（或 Save and publish），
然后刷新线上页核对三件事：

1. F1 图和 "Summarizing" 标题之间出现新节；
2. 新节里的 python 代码块和 3 行输出块显示为代码样式；
3. Takeaways 里多出 "Stored is not surfaced" 这一条。

**不要动**：标题、副标题、封面、canonical（已指向 xiongpin.dev）。
