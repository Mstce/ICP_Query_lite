# ICP_Query_lite

此项目是精简后的代码，只保留了查询接口，修复了原项目不能查询的问题，主要是提供给https://github.com/Mstce/Onyx   项目使用。

### 源码部署

```shell
Python 3.8+（建议 3.9/3.10）
依赖安装（与原项目一致）：
pip install -r requirements.txt
```

## 启动服务

在 `ICP_Query_lite` 目录下运行：

```bash
python icpApi.py
```

### 🔍使用API查询接口

#### 支持八种类型查询：

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

#### 示例请求

##### GET请求

- **URL格式**: `http://0.0.0.0:16181/query/{type}?search={name}`

- **示例1**: 查询域名 `baidu.com` 备案信息
  ```
  curl http://127.0.0.1:16181/query/web?search=baidu.com
  ```

- **示例2**: 根据网站的备案号 `京ICP证030173号` 查询备案信息
  ```
  curl http://127.0.0.1:16181/query/web?search=京ICP证030173号
  ```

- **示例3**: 根据企业名称查询备案信息
  ```
  curl http://127.0.0.1:16181/query/web?search=深圳市腾讯计算机系统有限公司
  ```

- **示例4**: 根据企业名称查询备案信息，每页20条数据，查询第3页
  ```
  curl http://127.0.0.1:16181/query/web?search=深圳市腾讯计算机系统有限公司&pageNum=3&pageSize=20
  ```

## 📊 响应参数说明

| 参数             | 说明                                                         |
| ---------------- | ------------------------------------------------------------ |
| lastPage         | 据查询数量有多少页                                           |
| pages            | 据查询数量有多少页                                           |
| pageSize         | 每页几条数据                                                 |
| pageNum          | 第几页                                                       |
| nextPage         | 下一页的页面序号                                             |
| total            | 据查询数量有多少页                                           |
| domain           | 备案的域名                                                   |
| domainId         | 域名id                                                       |
| limitAccess      | 是否限制接入                                                 |
| mainLicence      | ICP备案主体许可证号                                          |
| natureName       | 主办单位性质                                                 |
| serviceLicence   | ICP备案服务许可证号                                          |
| unitName         | 主办单位名称                                                 |
| updateRecordTime | 审核通过日期                                                 |
| contentTypeName  | 服务前置审批项                                               |
| cityId           | 城市ID                                                       |
| countyId         | 区县ID                                                       |
| contentTypeName  | 内容类型                                                     |
| mainUnitAddress  | 主体地址                                                     |
| serviceName      | 服务名称(APP、小程序或快应用名称)                            |
| version          | 服务版本                                                     |
| blackListLevel   | 威胁等级，表示是否为违法违规应用，目前获得的等级为2时，表示暂无违法违规信息 |

## 🔗 原项目链接

- [🔗 完整版ICP_Query](https://github.com/HG-ha/ICP_Query)
