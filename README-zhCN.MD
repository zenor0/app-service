# Xianju-admin-service

该仓库包含了使用 Flask 框架实现的管理后端服务。该服务主要提供了 API 接口，并可以使用 Docker 或手动部署。本 README 文件提供了该仓库的介绍和部署说明。

xianju-admin-frontend 仓库中提供了闲橘的后台管理。

详细信息请参阅 API 文档：https://www.apifox.cn/apidoc/shared-75b228ec-c55b-4115-84c1-9dbcdb11ed5b

## 特性

+ RESTful
+ API 版本控制
+ API 角色权限控制

## 部署

### 默认 `.env` 内容

```shell
DATABASE_BASE_URI=<必填>
APP_DATABASE_BASE_URI=<必填>
FLASK_APP=admin-service.py
FLASK_PORT=3000
SECRET_KEY='testing'
FLASK_DEBUG=1
SALT = 'SALT'
```

### Docker 部署

> 注意：用 `< >` 括起来的标签请替换为自定义内容。

按照以下步骤使用 Docker 部署服务：

1. 确保您的系统上已安装 Docker。您可以从官方网站下载 Docker：[https://www.docker.com](https://www.docker.com)。

2. 克隆此仓库到您的本地机器：

   ```shell
   git clone https://github.com/west2-xianju/admin-service
   ```

3. 进入项目目录：

   ```shell
   cd admin-service
   ```

4. 构建 Docker 镜像：

   ```shell
   docker build -t <自定义标签名> .
   ```

5. 运行 Docker 容器：

   ```shell
   docker run -p <外部端口>:3000 <自定义标签名>
   ```

   后端服务现在会在 `http://localhost:<外部端口>` 上运行。

### 手动部署

按照以下步骤手动部署 Python Flask 后端服务：

1. 克隆此仓库到您的本地机器：

   ```shell
   git clone https://github.com/west2-xianju/admin-service
   ```

2. 进入项目目录：

   ```shell
   cd admin-service
   ```

3. 创建虚拟环境：

   ```shell
   python -m venv env
   ```

4. 激活虚拟环境：

   - 在 macOS 和 Linux 上：

     ```shell
     source env/bin/activate
     ```

   - 在 Windows 上：

     ```shell
     .\env\Scripts\activate
     ```

5. 安装所需的依赖项：

   ```shell
   pip install -r requirements.txt
   ```

6. 调整配置：

   您可以根据需要设置 `config.py` 和 `.env` 文件。

   在大多数情况下，您需要在 `.env

` 文件中将 `DATABASE_BASE_URL` 配置为您正在运行的数据库的基本 URL。

7. 启动后端服务：

   ```shell
   python admin-service.py
   ```

   后端服务现在会在 `http://localhost:3000` 上运行（默认端口为 3000，您可以在 `.env` 文件中更改）。

## 使用方法

部署后端服务后，您可以访问 API 端点与服务进行交互。使用 cURL、Postman 或任何 HTTP 客户端库等工具向所需的端点发送请求。可在源代码中找到可用的端点及其功能，或单独记录文档。

还有一些集成的功能可能会用到。

要初始化数据库并填充一些虚拟数据，可以运行以下命令：

```powershell
flask fill-db
```

要清空数据库，可以运行以下命令：

```powershell
flask clean-db
```

要运行服务，请运行以下命令：

```powershell
python chat-service.py
```

## 联系方式

如果您有任何问题、建议或反馈，请随时通过 [zenor0@outlook.com](mailto:zenor0@outlook.com) 联系我们。