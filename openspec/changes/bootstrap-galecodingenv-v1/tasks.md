# GaleCodingEnv v1 任务

## 1. 仓库骨架

- [x] 1.1 初始化 GaleCodingEnv Git 仓库
- [x] 1.2 建立 `.gitignore`、`package.json`、`galeenv.config.json`
- [x] 1.3 建立 `scripts/` 目录

## 2. 上游与品牌层

- [x] 2.1 实现上游同步脚本
- [x] 2.2 实现品牌工作区生成脚本
- [x] 2.3 收敛对外命令命名，避免暴露 gstack 前缀

## 3. HKT-memory 集成

- [x] 3.1 建立 HKT-memory 路径解析能力
- [x] 3.2 提供 verify / retrieve / store 桥接命令
- [x] 3.3 将 HKT-memory 检查接入 npm scripts

## 4. OpenSpec 规范层

- [x] 4.1 建立首版 OpenSpec change
- [x] 4.2 补齐 spec / tasks / checklist

## 5. 自检与验证

- [x] 5.1 实现仓库级 doctor 脚本
- [x] 5.2 验证 `verify:upstream`
- [x] 5.3 验证 `refresh:workspace`
- [x] 5.4 验证 `verify:hkt-memory`
- [x] 5.5 验证 `verify:repo`

## 6. 提交与远端

- [ ] 6.1 配置 GaleCodingEnv 远端仓库
- [ ] 6.2 提交首版骨架
- [ ] 6.3 推送到主仓
