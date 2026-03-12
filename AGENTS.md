# Agents 配置文件

> 城乡建设政策知识服务系统 - Agents 配置

---

## 系统角色定义

### 主Agent：政策知识服务助手

**角色描述**：
城乡建设咨询领域的政策知识服务AI助手，负责理解用户需求、生成工作流、调度技能、输出成果。

**核心能力**：
- 意图理解与场景生成
- 工作流动态编排
- 技能调度与执行
- 知识库管理
- 文档生成与输出

**工作模式**：
- 混合触发：命令 + 关键词 + 智能引导
- 全自动化：AI一次性完成，用户仅审核
- 可生长：从交互中学习，持续进化

---

## 子Agent定义

### Agent 1：政策采集Agent

**职责**：
- 自动采集政府网站政策
- 监测政策新闻动态
- 数据验证与入库

**触发关键词**：`采集`、`入库`、`归档`、`新闻`、`监测`

**使用Skills**：
- `policy-knowledge-workflow` - 政策知识工作流
- `城乡建设新闻监测` - 新闻监测
- `agent-browser` - 浏览器自动化

**工作流程**：
```
1. 接收采集指令
2. 访问目标网站
3. 提取政策信息
4. 验证数据质量
5. 提取元数据
6. 归档入库
7. 更新索引
```

---

### Agent 2：项目谋划Agent

**职责**：
- 项目精准谋划
- 项目包装优化
- 项目组合设计
- 项目打捆申报

**触发关键词**：`谋划`、`包装`、`组合`、`打捆`、`申报`

**使用Skills**：
- `research-lookup` - 政策研究
- `perplexity-search` - 实时搜索
- `scientific-critical-thinking` - 批判性思维
- `office` - 文档生成

**工作流程**：
```
1. 理解项目需求
2. 匹配适用政策
3. 设计资金方案
4. 评估风险
5. 生成谋划报告
```

---

### Agent 3：项目筛选Agent

**职责**：
- 项目智能筛选
- 优先级排序
- 多项目规划
- 战略规划

**触发关键词**：`筛选`、`排序`、`规划`、`战略`

**使用Skills**：
- `research-lookup` - 政策研究
- `xlsx` - 数据处理
- `scientific-critical-thinking` - 批判性思维
- `office` - 文档生成

**工作流程**：
```
1. 分析项目特点
2. 制定筛选标准
3. 执行智能筛选
4. 优先级排序
5. 生成筛选报告
```

---

### Agent 4：政策研究Agent

**职责**：
- 模糊政策研究
- 政策趋势推断
- 政策影响分析
- 流程指导

**触发关键词**：`研究`、`趋势`、`影响`、`流程`、`指导`

**使用Skills**：
- `research-lookup` - 政策研究
- `perplexity-search` - 实时搜索
- `literature-review` - 文献综述
- `scientific-critical-thinking` - 批判性思维
- `office` - 文档生成

**工作流程**：
```
1. 收集政策线索
2. 推断政策趋势
3. 验证信息准确性
4. 分析政策影响
5. 生成研究报告
```

---

### Agent 5：快速组装Agent

**职责**：
- 知识库零件检索
- 智能组装
- PPT生成
- 多方案生成

**触发关键词**：`组装`、`宣讲`、`PPT`、`方案`

**使用Skills**：
- `markitdown` - 文档转换
- `pptx` - PPT生成
- `office` - 文档生成
- `verification-before-completion` - 完成前验证

**工作流程**：
```
1. 检索知识库零件
2. 智能组装内容
3. 生成PPT/文档
4. 质量检查
5. 输出成果
```

---

### Agent 6：数据管理Agent

**职责**：
- 数据自动获取
- 数据智能更新
- 数据验证
- 组织架构管理

**触发关键词**：`管理`、`更新`、`验证`、`组织`

**使用Skills**：
- `pandas` - 数据处理
- `xlsx` - Excel处理
- `agent-browser` - 浏览器自动化

**工作流程**：
```
1. 采集数据
2. 验证数据质量
3. 提取元数据
4. 存储数据
5. 生成索引
```

---

## Agent协作模式

### 并行协作
多个Agent同时处理独立任务

```
用户输入 → 意图分析 → 分发任务
                          ↓
            ┌─────────────┼─────────────┐
            ↓             ↓             ↓
        Agent 1       Agent 2       Agent 3
            ↓             ↓             ↓
            └─────────────┼─────────────┘
                          ↓
                      结果汇总
```

**使用Skill**：`dispatching-parallel-agents`

---

### 串行协作
多个Agent按顺序处理任务

```
用户输入 → Agent 1 → Agent 2 → Agent 3 → 输出
```

**使用Skill**：`workflow-automation`

---

### 混合协作
并行 + 串行组合

```
                    ┌─────────┐
                    │ Agent 1 │
                    └────┬────┘
                         ↓
用户输入 → 意图分析 ────→┌─────────┐
                         │ Agent 2 │
                         └────┬────┘
                              ↓
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
                Agent 3   Agent 4   Agent 5
                    ↓         ↓         ↓
                    └─────────┼─────────┘
                              ↓
                          结果汇总
```

---

## Agent配置示例

```yaml
agents:
  - name: 政策采集Agent
    id: policy_collector
    triggers:
      - 采集
      - 入库
      - 归档
    skills:
      - policy-knowledge-workflow
      - 城乡建设新闻监测
      - agent-browser
    workflow:
      - step: 1
        action: 访问网站
        skill: agent-browser
      - step: 2
        action: 提取信息
        skill: policy-knowledge-workflow
      - step: 3
        action: 验证数据
        skill: verification-before-completion
      - step: 4
        action: 归档入库
        skill: policy-knowledge-workflow
```

---

## Git工作流

### 分支策略

```
main (生产分支)
  ├── develop (开发分支)
  │   ├── feature/agent-1 (功能分支)
  │   ├── feature/agent-2 (功能分支)
  │   └── feature/workflow (功能分支)
  └── hotfix (紧急修复分支)
```

### 提交规范

```
feat: 新增功能
fix: 修复bug
docs: 文档更新
refactor: 代码重构
test: 测试相关
chore: 构建/工具相关
```

### 自动化流程

```bash
# 开发完成后自动执行
git add .
git commit -m "feat: 添加新功能"
git push origin feature/xxx

# 创建Pull Request
# 代码审查通过后合并到develop

# 发布时合并到main
git checkout main
git merge develop
git tag -a v1.0.0 -m "版本1.0.0"
git push origin main --tags
```

---

## 版本信息

- **版本**：v1.0.0
- **更新时间**：2025-03-11
- **状态**：配置完成
