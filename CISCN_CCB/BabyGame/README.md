# BabyGame - Godot 游戏逆向分析 Writeup

这是一个关于 Godot 引擎游戏的逆向挑战。玩家需要分析游戏逻辑，提取加密密钥，并最终解密出隐藏的 Flag。

## 1. 题目信息
- **游戏名称**: BabyGame
- **文件组成**: `BabyGame.exe` (程序主体), `game.pck` (资源包)
- **技术栈**: Godot Engine, GDScript

---

## 2. 解题流程

### 第一步：资源提取与初步观察
1. **识别引擎**: 观察到 `.exe` 和 `.pck` 文件，确认是 Godot 引擎开发的游戏。
2. **提取资源**: 使用 `GDRE Tools` (Godot RE Tools) 加载 `game.pck`。
3. **获取源码**: 通过工具将提取出的 `.gdc` (已编译的字节码) 反编译为 `.gd` (GDScript 源码)。

### 第二步：核心逻辑分析
分析反编译后的脚本（重点关注 `game_manager.gd` 和 `flag.gd`）：
1. **初始密钥**: 发现一个初始字符串 `FanAglFanAglOoO!`。
2. **动态变化**: 游戏逻辑中包含“金币收集”机制，每收集一个金币，密钥会发生特定字符的替换（例如：`A` 替换为 `B`，`B` 替换为 `C`）。
3. **加密算法**: 发现程序使用 AES 算法（ECB 模式）对一段 Hex 字符串进行加密。

### 第三步：密钥推导与爆破
由于密钥随游戏进度（金币数量）变化，可以通过编写 Python 脚本模拟这一变化过程：
- 使用 `brute_key.py` 模拟 10 轮以内的字符替换。
- 对目标密文 `d458af702a680ae4d089ce32fc39945d` 进行循环尝试解密。
- 观察解密结果，当出现 `flag{...}` 格式的字符串时，即为正确密钥。

### 第四步：最终解密
在深入分析或通过内存取证获取到最终的 256 位密钥后，使用 `solve_flag.py` 进行标准 AES 解密，直接获取 Flag。

---

## 3. 脚本说明
- **`brute_key.py`**: 模拟密钥字符递增替换逻辑，用于在规律不完全明确时进行自动化尝试。
- **`solve_flag.py`**: 生产环境解密脚本，使用已确定的 32 字节密钥进行 AES-ECB 解密。

---

## 4. 工具使用补充

| 工具名称 | 用途 | 下载/参考地址 |
| :--- | :--- | :--- |
| **GDRE Tools** | Godot 资源提取与 GDScript 反编译 (最推荐) | [GitHub - bruvzg/gdtls](https://github.com/bruvzg/gdtls) |
| **gde-packer** | 用于解压和重新打包 Godot `.pck` 文件 | [GitHub 搜索相关项目] |
| **Python 3** | 运行解密脚本 | [python.org](https://www.python.org/) |
| **pycryptodome** | Python 加密库，用于处理 AES 算法 | `pip install pycryptodome` |

---

## 5. 总结
本题考察了对 Godot 游戏结构的了解以及对简单动态密钥变化逻辑的还原能力。关键点在于：
1. 正确使用工具反编译 GDScript。
2. 理解代码中密钥变化的替换规律。
3. 能够编写 Python 脚本调用加密库完成最后的解密步骤。
