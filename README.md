# 几何动态图库 · geo-figs

> **看动图请点这里 → https://popcorn-cdc.github.io/geo-figs/**
>
> GitHub 仓库页面里点 `*.html` 只会显示**源代码**，不会运行页面。要看成图，请用上面的 Pages 地址（手机/iPad Safari 也能直接开）。

## 站内导航

| 链接 | 内容 |
|---|---|
| [首页](https://popcorn-cdc.github.io/geo-figs/) | 全部年级/考试入口 |
| [七上 · 期中](https://popcorn-cdc.github.io/geo-figs/g07a/mid/) | 2026 清华附中朝阳 26③ 数轴跳跃点 |
| [九上 · 期中](https://popcorn-cdc.github.io/geo-figs/g09a/mid/) | 2026 二中 / 四中 / 北京中学 |
| [九上 · 期末](https://popcorn-cdc.github.io/geo-figs/g09a/final/) | 2025 海淀 第 8 题 |

## 目录约定

```
g07a g07b g08a g08b g09a g09b   年级+学期
mid final yuekao kaixue          期中/期末/月考/开学考
2026 2025 ...                    年份（按卷子年份，不是学年）
key ord                          重点校 / 普通校
<学校短码>/                       中文全名写在 _name.txt
  26-3.html                      题号-小问
  _动图.json                      {"26-3.html": "26题③-数轴跳跃点"}  ← 中文名
```

URL 一律 ASCII（短码），中文名只写在 `_name.txt` / `_动图.json`，索引页会自动读出来显示。

## 新增一份动图

```bash
# 1) 放到对应目录，文件名用题号短码
cp 动图.html g09a/mid/2026/key/4z/27-3.html
# 2) 同目录写中文名
echo '{"27-3.html": "27题(3)-△ACM面积最大值"}' > g09a/mid/2026/key/4z/_动图.json
# 3) 生成索引并发布
python3 build_index.py . && git add -A && git commit -m "收录 xxx" && git push
# 4) 镜像回菁师帮（中文文件名）
python3 ~/scripts/sync_geo_to_jsb.py
```

Pages 发布有 40–90 秒延迟；判断是否真上线要比**字节数**，只看 200 不够（旧缓存也 200）。
