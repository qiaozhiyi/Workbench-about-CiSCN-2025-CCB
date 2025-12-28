# ECDSA 题目 Write-Up

## 1. 题目分析

本题提供了三个文件：
- `task.py`: 签名生成脚本，揭示了私钥和随机数 $k$ (nonce) 的生成逻辑。
- `public.pem`: 公钥。
- `signatures.txt`: 60 组消息与其对应的 ECDSA 签名。

### 核心代码逻辑

1. **私钥生成**：
   私钥 $d$ 是由固定字符串 `b"Welcome to this challenge!"` 的 SHA512 哈希值对曲线阶 $n$ 取模得到的。
   ```python
   digest_int = int.from_bytes(sha512(b"Welcome to this challenge!").digest(), "big")
   priv_int = digest_int % curve_order
   ```

2. **随机数 (Nonce) 生成**：
   签名使用的 $k$ 是根据消息索引 $i$ 确定的：
   ```python
   def nonce(i):
       seed = sha512(b"bias" + bytes([i])).digest()
       k = int.from_bytes(seed, "big")
       return k
   ```
   这意味着对于 `signatures.txt` 中的每一条签名，其使用的 $k$ 都是**已知且可预测的**。

3. **签名参数**：
   - 曲线：`NIST521p` (P-521)。
   - 签名哈希：经过对 `signatures.txt` 的数据进行碰撞测试，确定签名时对消息使用的哈希算法是 **SHA1**。

## 2. 漏洞利用思路

在 ECDSA 签名算法中，签名方程为：
$$s \equiv k^{-1}(z + r \cdot d) \pmod n$$

其中 $r, s$ 是签名值，$k$ 是随机数，$z$ 是消息哈希，$d$ 是私钥。如果随机数 $k$ 泄露，则私钥 $d$ 可以通过下式直接计算：
$$d \equiv r^{-1}(s \cdot k - z) \pmod n$$

本题中，$k$ 可以根据索引直接构造，$z$ 可以通过对消息求 SHA1 得到，$r$ 和 $s$ 从 `signatures.txt` 中提取。因此，我们可以直接恢复出私钥。

## 3. 解题步骤

1. **计算 $k$**：根据 `task.py` 中的 `nonce(0)` 函数计算出第一条签名使用的随机数。
2. **提取 $r, s$**：从 `signatures.txt` 第一行提取 $r$ 和 $s$（在 P-521 中，两者各占 66 字节）。
3. **计算消息哈希 $z$**：对第一条消息 `message-\x00` 计算 SHA1。
4. **计算私钥 $d$**：代入公式计算。
5. **获取 Flag**：恢复出的私钥 $d$ 的十六进制字符串即为 Flag。

## 4. 利用脚本

已编写 `exp.py` 脚本，运行即可获取私钥。

```bash
python3 exp.py
```

## 5. 总结

本题是 ECDSA **Known Nonce**（已知随机数）攻击的典型案例。在 ECDSA 协议中，随机数 $k$ 的机密性与私钥同等重要，任何关于 $k$ 的泄露（无论是完全泄露还是部分偏置）都会导致私钥被迅速破解。
