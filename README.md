# Peak Whitelist (高峰白名单)

![logo](logo.png)

一个 [AstrBot](https://github.com/Soulter/AstrBot) 插件：**工作日指定时段**在**指定群**只允许**白名单成员**触发 bot，省 token。

## 功能

- 高峰时段（默认工作日 08:00-12:00 与 14:00-18:00，支持多时段）非白名单成员的消息会被拦截，不触发 bot
- 白名单成员、群管理员自动放行
- 目标群、白名单、时段全部**可配置**（WebUI 插件配置面板，修改即时生效）
- 可设置仅工作日生效（周末不拦截）

## 安装

将插件目录放入 AstrBot 的 `data/plugins/` 下，或在 WebUI 插件管理 → 从 Git 仓库安装：

```
https://github.com/Fangnai-byte/astrbot_plugin_peak_whitelist0d00
```

启用即可，无需指令。

## 配置项

| 配置项 | 说明 | 默认值 |
| --- | --- | --- |
| `group_ids` | 生效群号列表（如 `123456789`） | 空 |
| `whitelist` | 白名单成员 QQ 列表 | 空 |
| `time_windows` | 生效时间段，支持多个（如 `08:00-12:00`、`14:00-18:00`） | `08:00-12:00`、`14:00-18:00` |
| `weekday_only` | 仅工作日生效 | `true` |

配置修改**即时生效**，无需重启。

## 说明

- 拦截 = `event.stop_event()`，消息不会进入 AstrBot 后续处理流程（不消耗 LLM token）
- 高峰时段外、周末、非目标群：一律放行，不影响正常使用

## License

MIT License
