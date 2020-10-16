# OpenSSL 生成证书

### 常用文件类型

* .key: 私有密钥
* .csr: 证书请求文件,用于申请证书
* .crt: CA 认证后的证书文件

### 用户证书生成步骤:

1. 生成私钥 (.key)

   ```bash
   # 生成 CA 密钥
   openssl genrsa -out ca.key 2048
   
   # 生成 CA 证书, days 参数以天为单位设置证书的有效期. 本过程中会要求输入证书的所在地、公司名、站点名等
   openssl req -x509 -new -nodes -key ca.key -days 365 -out ca.crt
   ```

2. 生成证书请求 (.csr)

   ```sh
   # 生成服务器证书 RSA 的密钥对
   openssl genrsa -out server.key 2048
   
   # 生成服务器端证书 CSR, 本过程中会要求输入证书所在地、公司名、站点名等
   openssl req -new -key server.key -out server.csr
   ```

3. 用 CA 根证书签名得到证书 (.crt)

   ```shell
   # 生成服务端证书 ca.crt
   openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
   ```