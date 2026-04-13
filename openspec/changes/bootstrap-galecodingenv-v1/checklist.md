# GaleCodingEnv v1 评审清单

## 范围

- [x] 首版只做外层骨架，不改写 GStack 内核
- [x] 首版只提供 HKT-memory 集成入口，不做深度服务化
- [x] 首版保留双仓结构：`GStack` 上游仓 + `GaleCodingEnv` 公司仓

## 命名

- [x] 对外 npm scripts 不出现 gstack 前缀
- [x] 品牌工作目录使用 GaleEnv 语义
- [x] 上游语义只保留在配置和仓库边界内

## 集成

- [x] 已存在上游同步脚本
- [x] 已存在品牌工作区生成脚本
- [x] 已存在 HKT-memory 桥接脚本
- [x] 已存在仓库级 doctor 脚本

## 验证

- [x] `refresh:workspace` 可以执行
- [x] `verify:hkt-memory` 可以执行
- [x] `verify:repo` 可以输出关键依赖状态

## 提交前

- [ ] 远端已配置为公司仓库
- [ ] 首版骨架已提交
- [ ] 主分支已推送
