# ICP_Query_lite

工信部 ICP 备案查询精简版，只保留查询接口。基于滑块验证码自动识别，无需 ONNX 模型。

主要为 [Onyx](https://github.com/Mstce/Onyx) 项目提供后端支持。

## 部署

**环境要求**: Python 3.8+（建议 3.9/3.10）

**依赖安装**:

```bash
pip install aiohttp pyyaml numpy Pillow ujson cachetools
```

## 启动

```bash
python icpApi.py
```

默认监听 `http://127.0.0.1:59641`，在 Onyx 中填入此地址即可。

## API 接口

### 支持八种查询类型

| 类型    | 说明           |
| ------- | -------------- |
| `web`   | 网站           |
| `app`   | APP            |
| `mapp`  | 小程序         |
| `kapp`  | 快应用         |
| `bweb`  | 违法违规网站   |
| `bapp`  | 违法违规APP    |
| `bmapp` | 违法违规小程序 |
| `bkapp` | 违法违规快应用 |

### 请求格式

```
GET/POST http://127.0.0.1:59641/query/{type}?search={name}
```

**参数**:

| 参数       | 必填 | 说明                            |
| ---------- | ---- | ------------------------------- |
| search     | 是   | 域名、备案号或企业名称          |
| pageNum    | 否   | 页码，默认第1页                 |
| pageSize   | 否   | 每页条数                        |
| use_proxy  | 否   | 是否使用代理池，默认 false      |
| proxy      | 否   | 指定代理地址                    |

### 示例

```bash
# 查询域名备案
curl "http://127.0.0.1:59641/query/web?search=baidu.com"

# 按备案号查询
curl "http://127.0.0.1:59641/query/web?search=京ICP证030173号"

# 按企业名称查询，第3页每页20条
curl "http://127.0.0.1:59641/query/web?search=深圳市腾讯计算机系统有限公司&pageNum=3&pageSize=20"

# 查询APP备案
curl "http://127.0.0.1:59641/query/app?search=微信"
```

## 配置说明

编辑 `config.yml`：

```yaml
system:
  host: 0.0.0.0        # 监听地址
  port: 59641           # 监听端口
  http_client_timeout: 5 # 请求超时(秒)

captcha:
  enable: true           # 启用验证码自动识别
  save_failed_img: false # 保存识别失败的验证码图片
  save_failed_img_path: faile_captcha  # 失败图片保存路径
  retry_times: 10        # 验证码重试次数

proxy:
  local_ipv6_pool:
    enable: false        # 启用本地IPv6轮换
  tunnel:
    url: null            # 隧道代理地址
  extra_api:
    url: null            # 代理API提取地址
    extra_interval: 3    # 代理提取间隔(秒)
    timeout: 100         # 代理超时(秒)
    timeout_drop: 8      # 提前丢弃超时代理(秒)
    proxy_timeout: 0.5   # 代理检测超时(秒)

risk_avoidance:
  allow_type:            # 允许的查询类型
  - web
  - app
  - mapp
  - kapp
  - bweb
  - bapp
  - bmapp
  - bkapp
  prohibit_suffix: []    # 禁止查询的域名后缀

log:
  dir: logs              # 日志目录
  file_head: ymicp       # 日志文件名前缀
  backup_count: 7        # 日志保留天数
  save_log: false        # 是否保存日志到文件
  output_console: true   # 是否输出到控制台
```

## 响应参数

| 参数             | 说明           |
| ---------------- | -------------- |
| domain           | 备案域名       |
| mainLicence      | 主体备案号     |
| serviceLicence   | 服务备案号     |
| unitName         | 主办单位名称   |
| natureName       | 主办单位性质   |
| updateRecordTime | 审核通过日期   |
| serviceName      | 服务名称(APP/小程序/快应用) |
| total            | 总记录数       |
| pageNum          | 当前页码       |
| pageSize         | 每页条数       |

## 相关项目

- [ICP_Query](https://github.com/HG-ha/ICP_Query) - 原作者项目，带管理界面、数据库、代理池等完整功能
- [Onyx](https://github.com/Mstce/Onyx) - 前端查询界面
