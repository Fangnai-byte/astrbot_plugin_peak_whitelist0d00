from astrbot.api import AstrBotConfig
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.event.filter import EventMessageType
from astrbot.api.star import Context, Star, register
from datetime import datetime, time


def parse_time(s: str) -> time | None:
    """解析 'HH:MM' 为 time，失败返回 None"""
    try:
        h, m = s.strip().split(":")
        return time(int(h), int(m))
    except Exception:
        return None


@register(
    "astrbot_plugin_peak_whitelist",
    "绫地宁宁",
    "高峰白名单：指定时段内仅白名单成员可触发bot（省token）",
    "1.3.0",
)
class PeakWhitelist(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    def _in_window(self, now: datetime) -> bool:
        """判断当前时间是否在配置的时间窗内"""
        windows = self.config.get("time_windows") or ["08:00-12:00", "14:00-18:00"]
        for w in windows:
            if "-" not in str(w):
                continue
            start_s, end_s = str(w).split("-", 1)
            start_t = parse_time(start_s)
            end_t = parse_time(end_s)
            if start_t and end_t and start_t <= now.time() < end_t:
                return True
        return False

    @filter.event_message_type(EventMessageType.GROUP_MESSAGE)
    async def peak_whitelist_check(self, event: AstrMessageEvent):
        # 仅处理配置的群
        group_ids = self.config.get("group_ids") or []
        if event.get_group_id() not in group_ids:
            return
        # 黑名单成员一律拦截（最高优先级，无论时段、无论是否白名单/管理员）
        blacklist = self.config.get("blacklist") or []
        if str(event.get_sender_id()) in blacklist:
            event.stop_event()
            return
        now = datetime.now()
        # 工作日限制
        if self.config.get("weekday_only", True) and now.weekday() >= 5:
            return
        # 时间窗限制
        if not self._in_window(now):
            return
        # 白名单成员放行
        whitelist = self.config.get("whitelist") or []
        if str(event.get_sender_id()) in whitelist:
            return
        # 管理员放行
        if getattr(event, "role", None) == "admin":
            return
        # 其余成员拦截
        event.stop_event()
