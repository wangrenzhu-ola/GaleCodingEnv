# GaleCodingEnv v1 骨架

## 背景

GaleCodingEnv 需要作为公司内部 AI Coding 环境的外层工程，持续吸收上游 GStack，同时叠加 Gale 品牌层、OpenSpec 规范层与 HKT-memory 记忆层。

当前仓库已经具备最基础的上游同步与品牌替换脚本，但还缺少一个可提交、可扩展、可验证的首版骨架，使团队能围绕固定目录、固定脚本和固定集成入口继续建设。

## 目标

- 提供一个可提交到公司仓库的 GaleCodingEnv 首版骨架
- 明确上游仓、品牌工作区、OpenSpec 变更目录与 HKT-memory 集成入口
- 让团队能够通过统一脚本完成上游同步、品牌生成与环境自检

## 非目标

- 本轮不改造 GStack 内核实现
- 本轮不把 HKT-memory 重写为 Node.js 服务
- 本轮不实现多租户、权限系统和完整评估面板

## ADDED Requirements

### Requirement: 首版仓库骨架

系统必须提供 GaleCodingEnv 的最小可运行仓库骨架。

#### Scenario: 目录结构可识别
- **WHEN** 开发者打开仓库根目录
- **THEN** 能看到上游同步配置、品牌脚本、OpenSpec 变更目录与 HKT-memory 集成脚本

#### Scenario: 仓库可以直接提交
- **WHEN** 开发者执行 Git 状态检查
- **THEN** 仓库内容仅包含 GaleCodingEnv 外层骨架文件
- **AND** 不包含生成出的上游镜像与品牌工作区

### Requirement: 上游同步与品牌生成

系统必须支持从本地上游仓同步并生成品牌工作区。

#### Scenario: 一条命令完成刷新
- **WHEN** 开发者执行工作区刷新命令
- **THEN** 系统先同步上游代码
- **AND** 再生成 Gale 品牌工作区

#### Scenario: 默认不暴露 gstack 对外命令
- **WHEN** 开发者查看对外 npm scripts
- **THEN** 对外命令应使用 upstream 或 workspace 语义
- **AND** 不直接暴露 gstack 前缀

### Requirement: HKT-memory 集成入口

系统必须提供面向 HKT-memory 的统一桥接入口。

#### Scenario: 可验证 HKT-memory 依赖
- **WHEN** 开发者执行 HKT-memory 验证命令
- **THEN** 系统返回仓库路径、脚本路径与运行时可用性

#### Scenario: 可透传记忆检索与存储
- **WHEN** 开发者通过 GaleCodingEnv 调用记忆桥接脚本
- **THEN** 系统能够向 HKT-memory 转发 retrieve 与 store 命令

### Requirement: OpenSpec 规范入口

系统必须内置 GaleCodingEnv 的 OpenSpec 变更目录。

#### Scenario: 首版 change 可作为后续开发基线
- **WHEN** 团队开始下一轮功能迭代
- **THEN** 能基于仓库内已存在的 OpenSpec change 继续扩展

### Requirement: 自检能力

系统必须提供仓库级 doctor 检查。

#### Scenario: 自检输出关键依赖状态
- **WHEN** 开发者执行仓库自检命令
- **THEN** 系统返回上游仓、品牌目录、OpenSpec 目录与 HKT-memory 状态
