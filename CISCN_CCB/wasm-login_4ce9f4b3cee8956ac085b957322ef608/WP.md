### Web 安全登录 Demo 题目分析与 Write-Up

#### 1. 题目背景
题目描述了一个开发者在 2025 年 12 月第三个周末（周日深夜到周一凌晨）编写了一个 Web 安全登录 Demo。开发者忘记了成功登录时的确切时间戳，需要通过已知的验证逻辑找回该时间戳对应的 `check` 值。

- **目标**：找回成功登录时的 32 位 MD5 `check` 值。
- **线索**：
    - 时间范围：2025 年 12 月 21 日（周日）深夜至 22 日（周一）凌晨。
    - 验证逻辑：`MD5(JSON.stringify(authData))` 的前 16 位为 `ccaf33e3512e31f3`。
    - 关键文件：`index.html`（前端逻辑）、`build/release.wasm`（核心认证逻辑）。

#### 2. 关键代码分析

**前端逻辑 (`index.html`)**：
在 `index.html` 中，登录逻辑调用了 WebAssembly 的 `authenticate` 函数：
```javascript
const authResult = authenticate(username, password);
const authData = JSON.parse(authResult);

// 模拟服务器验证
const check = CryptoJS.MD5(JSON.stringify(authData)).toString(CryptoJS.enc.Hex);
if (check.startsWith("ccaf33e3512e31f3")){
    resolve({ success: true });
}
```
这表明我们需要找到一个时间戳，使得 WASM 生成的 `authData` 的 MD5 值匹配目标前缀。

**Wasm 逻辑 (`build/release.js`)**：
通过分析生成的胶水代码 `release.js`，发现 WASM 模块导入了 `Date.now()`：
```javascript
"Date.now"() {
    return Date.now();
}
```
这意味着 `authenticate` 函数内部依赖当前系统时间戳来生成签名或加密数据。

#### 3. 解题思路
由于时间范围较小（仅几个小时），我们可以通过 Node.js 环境模拟时间戳并进行暴力破解。

1.  **确定时间范围**：
    2025 年 12 月第三个周末的周一凌晨，大约是 `2025-12-21 23:00:00` 到 `2025-12-22 03:00:00`。
2.  **Mock 时间函数**：
    在 Node.js 中重写 `globalThis.Date.now`，使其返回我们枚举的时间戳。
3.  **WASM 处理**：
    注意题目提供的 `release.wasm` 可能是 WAT（文本格式），如果是文本格式，需要先用 `wat2wasm` 工具转换成二进制格式才能被 Node.js 加载。
4.  **爆破脚本**：
    遍历毫秒级时间戳，计算 MD5 值并比对。

#### 4. 爆破脚本 (Node.js)

```javascript
import crypto from "node:crypto";
import { authenticate } from "./build/release.js";

const targetPrefix = "ccaf33e3512e31f3";
// 设定搜索范围：2025-12-21 23:00 到 2025-12-22 04:00 (CST)
const start = new Date("2025-12-21T23:00:00+08:00").getTime();
const end   = new Date("2025-12-22T04:00:00+08:00").getTime();

for (let t = start; t <= end; t++) {
    // 劫持 Date.now 使得 WASM 获取到的是我们枚举的时间戳
    globalThis.Date.now = () => t;
    
    try {
        const authResult = authenticate("admin", "admin");
        const authData = JSON.parse(authResult);
        const md5 = crypto.createHash("md5").update(JSON.stringify(authData)).digest("hex");
        
        if (md5.startsWith(targetPrefix)) {
            console.log("找到匹配时间戳:", t);
            console.log("完整 MD5:", md5);
            console.log("Flag: flag{" + md5 + "}");
            break;
        }
    } catch (e) {
        // 忽略可能的异常
    }
}
```

#### 5. 结果
经过运行脚本，在时间戳 `1766334550699`（北京时间 2025/12/22 00:29:10）处找到匹配项。

- **成功登录时的 Auth 数据**：
  `{"username":"admin","password":"L0In602=","signature":"LxZiwA05Y9h7wX1CI0gUitOE2LBy9y8McoBqWgKIdDo="}`
- **对应的完整 MD5 (check 值)**：
  `ccaf33e3512e31f36228f0b97ccbc8f1`

**Final Flag**:
`flag{ccaf33e3512e31f36228f0b97ccbc8f1}`
